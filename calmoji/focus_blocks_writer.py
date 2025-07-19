# calmoji/focus_blocks_writer.py

from datetime import datetime, timedelta, date, time
from calmoji.focus_blocks_config import FOCUS_BLOCKS, ACTIVE_WEEKDAYS
from calmoji.types import Phase, Event
from calmoji.utils import group_phase_days_by_week, slugify
from calmoji.ics_writer import write_events_to_ics


def generate_focus_block_events_for_days(days: list[datetime]) -> list[Event]:
    """Generate focus block events for a list of datetime days."""
    events = []
    for day in days:
        if day.weekday() not in ACTIVE_WEEKDAYS:
            continue
        for index, (_, sh, sm, eh, em, emoji) in enumerate(FOCUS_BLOCKS):
            start = day.replace(hour=sh, minute=sm)
            end = day.replace(hour=eh, minute=em)
            block_emoji = "⛩️" if index == len(FOCUS_BLOCKS) - 1 else emoji
            events.append(Event(
                start=start,
                end=end,
                summary=f"{block_emoji} Focus Block",
                description=f"Focus block at {start.strftime('%H:%M')} UTC",
                emoji=block_emoji,
            ))
    return events


# def generate_focus_block_glyph_key_event(day: datetime) -> Event:
#     """Return a single all-day event on Saturday with emoji reference key."""

#     if isinstance(day, date) and not isinstance(day, datetime):
#         # Convert to datetime if necessary (won't affect all-day flag, but keeps type clean)
#         day = datetime.combine(day, datetime.min.time())
        
#     emoji_lines = [f"{emoji}  {desc}" for (_, _, _, _, _, emoji), desc in zip(FOCUS_BLOCKS, [
#         "Deep Thinking", "Writing", "Reading", "Technical", "Admin",
#         "Comms", "Reflect", "Analysis", "Creative", "Maintenance", "Decision", "Closure"
#     ])]
#     description = "Focus Block Glyph Key:\n\n" + "\n".join(emoji_lines)
#     return Event(
#         # start=day.replace(hour=0, minute=0),
#         # end=day.replace(hour=23, minute=59),
#         summary="⛩️ Focus Block Glyph Key",
#         description=description,
#         emoji="⛩️",
#         all_day=True
#     )


# def generate_focus_block_glyph_key_event(day: datetime) -> Event:
#     """Return a single all-day event on Saturday with emoji reference key."""

#     # Ensure `day` is a date object (no time)
#     if isinstance(day, datetime):
#         day = day.date()

#     emoji_lines = [f"{emoji}  {desc}" for (_, _, _, _, _, emoji), desc in zip(FOCUS_BLOCKS, [
#         "Deep Thinking", "Writing", "Reading", "Technical", "Admin",
#         "Comms", "Reflect", "Analysis", "Creative", "Maintenance", "Decision", "Closure"
#     ])]
#     description = "Focus Block Glyph Key:\n\n" + "\n".join(emoji_lines)

#     return Event(
#         start=day,
#         end=day + timedelta(days=1),
#         summary="⛩️ Focus Block Glyph Key",
#         description=description,
#         emoji="⛩️",
#         all_day=True
#     )


def generate_focus_block_glyph_key_event(day: datetime) -> Event:
    """Return a single all-day event on Saturday with emoji reference key."""

    # Normalize to datetime at midnight
    if isinstance(day, date) and not isinstance(day, datetime):
        day = datetime.combine(day, datetime.min.time())

    start = day.replace(hour=0, minute=0, second=0, microsecond=0)
    end = (start + timedelta(days=1))

    emoji_lines = [f"{emoji}  {desc}" for (_, _, _, _, _, emoji), desc in zip(FOCUS_BLOCKS, [
        "Deep Thinking", "Writing", "Reading", "Technical", "Admin",
        "Comms", "Reflect", "Analysis", "Creative", "Maintenance", "Decision", "Closure"
    ])]
    description = "Focus Block Glyph Key:\n\n" + "\n".join(emoji_lines)

    return Event(
        start=start,
        end=end,
        summary="⛩️ Focus Block Glyph Key",
        description=description,
        emoji="⛩️",
        all_day=True  # Used later by ICS writer to emit VALUE=DATE if True
    )


def write_focus_blocks_weekly(phases: list[Phase]) -> list[str]:
    written_paths = []

    for phase in phases:
        week_spans = group_phase_days_by_week(phase)
        print(f"📅 {phase.name} covers weeks: {[span.iso_week_label for span in week_spans]}")

        for span in week_spans:
            # ⏳ 1. Filter only eligible weekdays for focus blocks
            focus_days = [d for d in span.days if d.weekday() in ACTIVE_WEEKDAYS]
            events = generate_focus_block_events_for_days(focus_days)

            # ⛩️ 2. Add glyph key on Saturday if it's inside phase bounds
            saturday = span.start + timedelta(days=(5 - span.start.weekday()) % 7)
            if phase.start.date() <= saturday <= phase.end.date():
                events.append(generate_focus_block_glyph_key_event(saturday))

            # 💾 3. Write file if any events exist
            if events:
                filename = f"output/focus_blocks_{slugify(phase.name)}_{span.iso_week_label}.ics"
                write_events_to_ics(events, filename)
                written_paths.append(filename)
                print(f"✅ Wrote: {filename}")

    return written_paths


def generate_focus_block_events(phases: list[Phase]) -> list[Event]:
    """Generate all focus block events across all phases (flattened list)."""
    events: list[Event] = []
    for phase in phases:
        week_spans = group_phase_days_by_week(phase)  # returns list[PhaseWeekSpan]
        for span in week_spans:
            events.extend(generate_focus_block_events_for_days(span.days))
    return events
