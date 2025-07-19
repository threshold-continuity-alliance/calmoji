# calmoji/focus_blocks_writer.py

from datetime import datetime
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


def generate_focus_block_glyph_key_event(day: datetime) -> Event:
    """Return a single all-day event on Saturday with emoji reference key."""
    emoji_lines = [f"{emoji}  {desc}" for (_, _, _, _, _, emoji), desc in zip(FOCUS_BLOCKS, [
        "Deep Thinking", "Writing", "Reading", "Technical", "Admin",
        "Comms", "Reflect", "Analysis", "Creative", "Maintenance", "Decision", "Closure"
    ])]
    description = "Focus Block Glyph Key:\n\n" + "\n".join(emoji_lines)
    return Event(
        start=day.replace(hour=0, minute=0),
        end=day.replace(hour=23, minute=59),
        summary="⛩️ Focus Block Glyph Key",
        description=description,
        emoji="⛩️",
    )


# def write_focus_blocks_weekly(phases: list[Phase]) -> None:
#     """Write focus blocks per week per phase into .ics files, always including glyph key on Saturday."""
#     for phase in phases:
#         weekly_days = group_phase_days_by_week(phase)

#         for (year, week), days in weekly_days.items():
#             events = generate_focus_block_events_for_days(days)

#             # Always include glyph key on Saturday if present
#             saturday = next((d for d in days if d.weekday() == 5), None)
#             if saturday:
#                 glyph_event = generate_focus_block_glyph_key_event(saturday)
#                 events.append(glyph_event)

#             if events:
#                 filename = f"output/focus_blocks_{slugify(phase.name)}_{year}_W{week:02d}.ics"
#                 write_events_to_ics(events, filename)
#                 print(f"✅ Wrote: {filename}")

# def write_focus_blocks_weekly(phases: list[Phase]) -> None:
#     """Write focus blocks per week per phase into .ics files, always including glyph key on Saturdays."""
#     for phase in phases:
#         print(f"📅 {phase.name} covers weeks: {[w for (_, w) in group_phase_days_by_week(phase).keys()]}")
#         weekly_days = group_phase_days_by_week(phase)

#         for (year, week), days in weekly_days.items():
#             events = generate_focus_block_events_for_days(days)

#             # 🔒 Always add glyph block on Saturday if one exists
#             saturday = next((d for d in days if d.weekday() == 5), None)
#             if saturday:
#                 events.append(generate_focus_block_glyph_key_event(saturday))

#             # ✅ Write .ics if any event exists
#             if events:
#                 filename = f"output/focus_blocks_{slugify(phase.name)}_{year}_W{week:02d}.ics"
#                 write_events_to_ics(events, filename)
#                 print(f"✅ Wrote: {filename}")


from datetime import timedelta

def write_focus_blocks_weekly(phases: list[Phase]) -> list[str]:
    written_paths = []

    for phase in phases:
        weekly_days = group_phase_days_by_week(phase)
        print(f"📅 {phase.name} covers weeks: {[w for (_, w) in weekly_days.keys()]}")

        for (year, week), week_days in weekly_days.items():
            # ⏳ 1. Filter only eligible weekdays for focus blocks
            focus_days = [d for d in week_days if d.weekday() in ACTIVE_WEEKDAYS]
            events = generate_focus_block_events_for_days(focus_days)

            # ⛩️ 2. Add glyph key on Saturday if it's inside phase bounds
            week_start = min(week_days)
            saturday = week_start + timedelta(days=(5 - week_start.weekday()) % 7)
            if phase.start <= saturday <= phase.end:
                events.append(generate_focus_block_glyph_key_event(saturday))

            # 💾 3. Write file if any events exist
            if events:
                filename = f"output/focus_blocks_{slugify(phase.name)}_{year}_W{week:02d}.ics"
                write_events_to_ics(events, filename)
                written_paths.append(filename)
                print(f"✅ Wrote: {filename}")

    return written_paths


def generate_focus_block_events(phases: list[Phase]) -> list[Event]:
    """Generate all focus block events across all phases (flattened list)."""
    events = []
    for phase in phases:
        for days in group_phase_days_by_week(phase).values():
            events.extend(generate_focus_block_events_for_days(days))
    return events
