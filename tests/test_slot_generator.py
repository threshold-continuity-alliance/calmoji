# tests/test_slot_generator.py

from forge.slot_generator import generate_meeting_slots
from forge.calendar_phases import get_semester_phases
from forge.utils import get_start_date_from_year
from forge.types import Event


def test_slot_generation_for_first_phase():
    start_date = get_start_date_from_year(2024)
    phase = get_semester_phases(start_date)[0]
    events = generate_meeting_slots(phase)

    assert len(events) > 0

    for evt in events:
        assert isinstance(evt, Event)
        assert hasattr(evt, "start")
        assert hasattr(evt, "end")
        assert hasattr(evt, "summary")
        assert hasattr(evt, "description")
        assert "Face" in evt.summary  # Emoji time label
        assert evt.start.weekday() < 5  # Monday to Friday only


def test_all_events_within_phase_range():
    start_date = get_start_date_from_year(2024)
    phase = get_semester_phases(start_date)[0]
    # _, phase_start, phase_end, _ = phase
    events = generate_meeting_slots(phase)

    for evt in events:
        assert phase.start <= evt.start <= phase.end
        assert evt.start.date() == evt.end.date()
