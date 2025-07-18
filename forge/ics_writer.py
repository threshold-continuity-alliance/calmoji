import datetime
from typing import Optional

from forge.ebi48 import get_emoji_for_time
from forge.utils import (
    slugify,
    format_datetime,
    generate_uid,
    get_first_weekday_of_year,
)
from forge.types import Event, Phase

def create_ics_header(
    calname: str = "🧿 Meetmoji Calendar", version: str = "", comments: Optional[list[str]] = None
) -> str:
    full_name = f"{calname} {version}".strip()
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "CALSCALE:GREGORIAN",
        "PRODID:-//Threshold Continuity Alliance//Meetmoji Forge//EN",
        f"NAME:{full_name}",
        f"X-WR-CALNAME:{full_name}",
        "X-WR-TIMEZONE:UTC",
        "METHOD:PUBLISH",
    ]
    if comments:
        lines += [f"COMMENT:{comment}" for comment in comments]
    return "\n".join(lines) + "\n"

def create_event(event: Event) -> str:
    lines = ["BEGIN:VEVENT"]
    full_summary = f"{event.emoji} {event.summary}" if event.emoji else event.summary
    uid = event.uid or generate_uid(event.start, event.summary)
    lines.append(f"UID:{uid}")
    lines.append(f"SUMMARY:{full_summary}")
    if event.description:
        lines.append(f"DESCRIPTION:{event.description}")

    if event.all_day:
        lines.append(f"DTSTART;VALUE=DATE:{event.start.strftime('%Y%m%d')}")
        lines.append(f"DTEND;VALUE=DATE:{(event.end + datetime.timedelta(days=1)).strftime('%Y%m%d')}")
    else:
        lines.append(f"DTSTART:{format_datetime(event.start)}")
        lines.append(f"DTEND:{format_datetime(event.end)}")

    if event.recurrence:
        lines.append(f"RRULE:{event.recurrence}")
    if event.private:
        lines.append("CLASS:PRIVATE")
    if event.transparent:
        lines.append("TRANSP:TRANSPARENT")

    lines.append("END:VEVENT")
    return "\n".join(lines) + "\n"

def create_ics_footer() -> str:
    return "END:VCALENDAR\n"

def write_events_to_ics(events: list[Event], filename: str, header: bool = True, footer: bool = True) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        if header:
            f.write(create_ics_header())
        for i, event in enumerate(events):
            try:
                f.write(create_event(event))
            except Exception as e:
                raise ValueError(f"Failed to render event at index {i}: {event}") from e
        if footer:
            f.write(create_ics_footer())

def write_semester_blocks(phases: list[Phase], filename: Optional[str] = None) -> None:
    if not filename:
        anchor_year = phases[0].start.year if phases and phases[0].start else "unknown"
        filename = f"output/semester_phases_{anchor_year}.ics"

    events = [
        Event(
            start=phase.start,
            end=phase.end,
            summary=phase.name,
            description=f"{phase.emoji} {phase.name} block",
            emoji=phase.emoji,
            all_day=True,
        )
        for phase in phases
    ]
    write_events_to_ics(events, filename)

def write_ebi48_layer(target_path: str, year: int, recurring: bool = True, expanded: bool = False) -> None:
    assert not (recurring and expanded), "Choose either recurring or expanded mode, not both."

    ref_day = get_first_weekday_of_year(year, weekday=5)  # Saturday

    header = create_ics_header(
        calname=f"🧿 Meetmoji EBI48 Clock — Canonical Emoji Time (UTC Only) v{year}",
        comments=[
            "EBI48 is a deterministic, symbolic emoji-based time layer.",
            "It recurs weekly and does not shift with local time.",
            "See: https://ebi48.org/",
        ],
    )

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(header)

        for hour in range(24):
            for minute in (5, 35):
                base_start = ref_day.replace(hour=hour, minute=minute)
                base_end = base_start + datetime.timedelta(minutes=25)
                emoji, label = get_emoji_for_time(base_start)
                summary = f"{emoji} {label} — EBI48"
                description = (
                    f"{emoji} {label} — Canonical EBI48 time at {hour:02d}:{minute:02d} UTC\n"
                    f"This slot is part of the EBI48 symbolic clock.\n"
                    f"🕒 UTC only — times do not shift with local time.\n"
                    f"v{year} — https://ebi48.org"
                )

                if expanded:
                    for week in range(52):
                        inst_start = base_start + datetime.timedelta(weeks=week)
                        inst_end = base_end + datetime.timedelta(weeks=week)
                        event = Event(
                            start=inst_start,
                            end=inst_end,
                            summary=summary,
                            description=description,
                            emoji=emoji,
                            uid=generate_uid(inst_start, summary),
                        )
                        f.write(create_event(event))
                else:
                    event = Event(
                        start=base_start,
                        end=base_end,
                        summary=summary,
                        description=description,
                        emoji=emoji,
                        recurrence="RRULE:FREQ=WEEKLY;COUNT=52" if recurring else None,
                        uid=generate_uid(base_start, summary),
                    )
                    f.write(create_event(event))

        f.write(create_ics_footer())
