# forge/slot_generator.py

from datetime import timedelta
from collections import defaultdict
from forge.config import OCEANIA_SLOTS_ENABLED
from forge.meeting_slots import MEETING_SLOTS
from forge.types import Event, Phase
from forge.ebi48 import get_emoji_for_time, get_emoji_name_for_slot

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

    while current_date <= phase.end:
        if current_date.weekday() < 5:  # Monday to Friday only
            for city, start_hr, start_min, end_hr, end_min, local_desc in MEETING_SLOTS:
                if city == "Oceania" and not OCEANIA_SLOTS_ENABLED:
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

    return events
