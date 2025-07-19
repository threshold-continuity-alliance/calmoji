# calmoji/slot_generator.py

from datetime import timedelta
from collections import defaultdict
from calmoji.config import OCEANIA_SLOTS_ENABLED
from calmoji.meeting_slots import MEETING_SLOTS
from calmoji.types import Event, Phase
from calmoji.ebi48 import get_emoji_for_time, get_emoji_name_for_slot

def generate_meeting_slots(phase):
    """
    Generate a list of Event objects for all weekday meeting slots in a phase.

    Args:
        phase: Phase object

    Returns:
        List of Event objects, one per city/time slot per weekday.
    """
    events = []
    current_date = phase.start

    # Define city-specific valid weekdays (0 = Monday, 6 = Sunday)
    CITY_WEEKDAYS = {
        "Mecca": {6, 0, 1, 2, 3},  # Sunday–Thursday
        # Default for all others is Monday–Friday (0–4)
    }

    while current_date <= phase.end:
        for slot in MEETING_SLOTS:
            city, start_hr, start_min, end_hr, end_min, local_desc = slot

            # Optional filter (for now only Auckland)
            if city == "Auckland" and not OCEANIA_SLOTS_ENABLED:
                continue

            # Determine valid weekdays for this city
            valid_weekdays = CITY_WEEKDAYS.get(city, {0, 1, 2, 3, 4})
            if current_date.weekday() not in valid_weekdays:
                continue

            # Handle Mecca's Sunday–Thursday week (6 = Sunday, 4 = Thursday)
            if city == "Mecca" and current_date.weekday() in {4, 5}:  # Friday (4), Saturday (5)
                continue

            # All others default to Monday–Friday (0–4)
            if city != "Mecca" and current_date.weekday() > 4:
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

        current_date += timedelta(minutes=1439)

    return events
