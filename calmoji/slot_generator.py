# calmoji/slot_generator.py

from datetime import timedelta
from calmoji.config import OCEANIA_SLOTS_ENABLED
from calmoji.meeting_slots import MEETING_SLOTS
from calmoji.types import Event
from calmoji.ebi48 import get_emoji_for_time


# Define city-specific valid weekdays (0 = Monday, 6 = Sunday)
CITY_WEEKDAYS = {
    "Mecca": {6, 0, 1, 2, 3},  # Sunday–Thursday
    # All others default to Monday–Friday
}


def is_valid_slot_day(city: str, weekday: int) -> bool:
    """Return True if a meeting slot is valid on this day for the given city."""
    return weekday in CITY_WEEKDAYS.get(city, {0, 1, 2, 3, 4})


def generate_meeting_slots(phase):
    """
    Generate Event objects for valid meeting slots in a given phase.
    """
    events = []
    current_date = phase.start

    while current_date <= phase.end:
        for slot in MEETING_SLOTS:
            city, start_hr, start_min, end_hr, end_min, local_desc = slot

            if city == "Auckland" and not OCEANIA_SLOTS_ENABLED:
                continue

            if not is_valid_slot_day(city, current_date.weekday()):
                continue

            start_dt = current_date.replace(hour=start_hr, minute=start_min)
            end_dt = current_date.replace(hour=end_hr, minute=end_min)

            emoji, face_name = get_emoji_for_time(start_dt)
            summary = f"{city} {emoji} {face_name} Slot ({local_desc})"
            description = f"{phase.emoji} — {phase.name}"

            events.append(Event(
                start=start_dt,
                end=end_dt,
                summary=summary,
                description=description
            ))

        current_date += timedelta(days=1)

    return sorted(events, key=lambda e: e.start)

