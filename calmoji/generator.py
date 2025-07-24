# calmoji/generator.py

from typing import List
from calmoji.types import Phase, Event
from calmoji.focus_blocks_writer import generate_focus_blocks
from calmoji.slot_generator import generate_meeting_slots

def get_all_events(phases: List[Phase]) -> List[Event]:
    """
    Generate all events (focus blocks and meeting slots) across all phases.

    Args:
        phases (List[Phase]): List of Phase objects defining time intervals.

    Returns:
        List[Event]: Combined list of Event objects across all phases.
    """
    all_events = []

    for phase in phases:
        focus_events = generate_focus_blocks(phase)
        meeting_events = generate_meeting_slots(phase)
        all_events.extend(focus_events + meeting_events)

    return all_events
