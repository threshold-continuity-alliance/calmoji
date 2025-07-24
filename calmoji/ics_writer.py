# calmoji/ics_writer.py

import os
from typing import TextIO
import datetime
from typing import List, Optional

from calmoji.ebi48 import get_emoji_for_time
from calmoji.types import Event, Phase
from calmoji.utils import (
    slugify,
    format_datetime,
    generate_uid,
    get_first_weekday_of_year,
    fold_ics_line,
)
from calmoji.generator import get_all_events
from calmoji.ics_writer import create_ics_header, create_ics_footer, fold_lines
from calmoji.types import Event


def create_ics_header(
    calname: str = "🧿 calmoji calendar", version: str = "", comments: Optional[list[str]] = None
) -> list[str]:
    full_name = f"{calname} {version}".strip()
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "CALSCALE:GREGORIAN",
        "PRODID:-//Threshold Continuity Alliance//calmoji//EN",
        f"NAME:{full_name}",
        f"X-WR-CALNAME:{full_name}",
        "X-WR-TIMEZONE:UTC",
        "METHOD:PUBLISH",
    ]
    if comments:
        lines += [f"COMMENT:{comment}" for comment in comments]
    return lines


def create_ics_footer() -> list[str]:
    return ["END:VCALENDAR"]


def fold_lines(lines: list[str]) -> str:
    """Fold lines per RFC 5545 using CRLF and space continuation."""
    return "\r\n".join(fold_ics_line(line) for line in lines)


def write_events_to_ics(events: list[Event], filename: str, header: bool = True, footer: bool = True) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        if header:
            f.write(fold_lines(create_ics_header()) + "\r\n")

        for i, event in enumerate(events):
            try:
                f.write(fold_lines(event.to_ics()) + "\r\n")
            except Exception as e:
                raise ValueError(f"Failed to render event at index {i}: {event}") from e

        if footer:
            f.write(fold_lines(create_ics_footer()) + "\r\n")


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
    """
    Write the EBI48 symbolic emoji layer as an .ics file.

    Parameters:
        target_path (str): Output ICS file path.
        year (int): Anchor year for recurring or expanded scheduling.
        recurring (bool): If True, write weekly-recurring events.
        expanded (bool): If True, write all 52 individual week instances.
    """
    assert not (recurring and expanded), "Choose either recurring or expanded mode, not both."

    ref_day = get_first_weekday_of_year(year, weekday=5)  # Saturday as weekly anchor

    header = create_ics_header(
        calname=f"🧿 calmoji EBI48 Clock — Canonical Emoji Time (UTC Only) v{year}",
        comments=[
            "EBI48 is a deterministic, symbolic emoji-based time layer.",
            "It recurs weekly and does not shift with local time.",
            "See: https://ebi48.org/",
        ],
    )

    footer = create_ics_footer()

    with open(target_path, "w", encoding="utf-8") as f:
        # Write VCALENDAR header
        f.write("\n".join(header) + "\n")

        # Add symbolic cadence key for this year's schedule
        glyph_key_event = Event(
            start=ref_day,
            end=ref_day + datetime.timedelta(days=1),
            summary="Glyph Key for th⚯n is week",
            description="This symbolic marker encodes cadence glyph key for th⚯n is week.",
            emoji="🗝️",
            all_day=True,
            uid=generate_uid(dt=ref_day, label="glyph-key", namespace="ebi48"),
        )
        f.write("\n".join(glyph_key_event.to_ics()) + "\n")

        # Loop through each canonical EBI48 slot
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
                        f.write("\n".join(event.to_ics()) + "\n")
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
                    f.write("\n".join(event.to_ics()) + "\n")

        # Close VCALENDAR
        f.write("\n".join(footer) + "\n")


def write_focus_blocks(
    phases: List[Phase],
    output_path: str,
    glyph_key: bool = True,
    include_header: bool = True,
    include_footer: bool = True,
) -> None:
    """
    Generate a .ics file containing focus blocks for the given phases.

    Parameters:
    - phases: List of Phase objects with computed start/end datetimes
    - output_path: Path to output .ics file
    - glyph_key: If True, include one glyph key summary event
    - include_header: If True, write VCALENDAR header
    - include_footer: If True, write VCALENDAR footer
    """

    events = []

    # Per-phase, per-week event generation
    for phase in phases:
        if not phase.start or not phase.end:
            raise ValueError(f"Phase {phase.name} is missing start or end dates.")

        phase_start = phase.start
        phase_end = phase.end

        current = phase_start
        while current <= phase_end:
            week_start = current
            week_end = min(week_start + timedelta(days=6), phase_end)

            iso_year, iso_week, _ = week_start.isocalendar()
            label = f"Glyph Test Phase {iso_year}-W{iso_week:02d} Focus Block {week_start.day % 12 + 1} 🗝️"

            events.append(
                Event(
                    start=week_start,
                    end=week_end + timedelta(days=1),  # all-day exclusive DTEND
                    summary=label,
                    description="This symbolic marker encodes cadence glyph key for th’n in this week.",
                    emoji="🗝️",
                    all_day=True,
                    uid=generate_uid(week_start, label, namespace="focus-block"),
                )
            )

            current += timedelta(days=7)

    # Add global glyph key event if enabled
    if glyph_key:
        earliest = min(phase.start for phase in phases if phase.start)
        label = f"Glyph Key — {earliest.year} canonical focus glyph encoding"
        events.append(
            Event(
                start=earliest,
                end=earliest + timedelta(days=1),
                summary=label,
                description="This symbolic marker encodes the focus glyph key for the calendar year.",
                emoji="🗝️",
                all_day=True,
                uid=generate_uid(earliest, label, namespace="glyph-key"),
            )
        )

    # Output to .ics file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        if include_header:
            f.write("BEGIN:VCALENDAR\n")
            f.write("VERSION:2.0\n")
            f.write("CALSCALE:GREGORIAN\n")
            f.write("PRODID:-//Threshold Continuity Alliance//calmoji//EN\n")
            f.write("NAME:🧿 calmoji focus blocks\n")
            f.write("X-WR-CALNAME:🧿 calmoji focus blocks\n")
            f.write("X-WR-TIMEZONE:UTC\n")
            f.write("METHOD:PUBLISH\n")

        for event in events:
            lines = event.to_ics()
            folded_lines = [fold_ics_line(line) for line in lines]
            f.write("\n".join(folded_lines) + "\n")

        if include_footer:
            f.write("END:VCALENDAR\n")


def generate_ics_file(start: datetime, output: TextIO) -> None:
    """
    Generate a full .ics calendar stream from a datetime-normalized starting point.
    
    Args:
        start (datetime): The beginning of the calendar year.
        output (TextIO): A writable stream to write .ics content to.
    """
    events = get_all_events(start)

    output.write(fold_lines(create_ics_header()) + "\r\n")

    for i, event in enumerate(events):
        try:
            output.write(fold_lines(event.to_ics()) + "\r\n")
        except Exception as e:
            raise ValueError(f"Failed to render event at index {i}: {event}") from e

    output.write(fold_lines(create_ics_footer()) + "\r\n")
