# tests/test_slot_generator.py

from calmoji.slot_generator import generate_meeting_slots
from calmoji.calendar_phases import get_semester_phases
from calmoji.calendar_config import get_year_start_date
from calmoji.types import Event, Phase
from calmoji.utils import coerce_to_utc

def test_slot_generation_for_first_phase():
    start_date = get_year_start_date("academic")
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
        if "Mecca" in evt.summary:
            assert evt.start.weekday() in {6, 0, 1, 2, 3}  # Sunday to Thursday
        else:
            assert evt.start.weekday() in range(5)  # Monday (0) to Friday (4)


def test_all_events_within_phase_range():
    start_date = get_year_start_date("academic")
    phase = get_semester_phases(start_date)[0]
    events = generate_meeting_slots(phase)

    for evt in events:
        assert coerce_to_utc(phase.start) <= evt.start <= coerce_to_utc(phase.end)
        assert evt.start.date() == evt.end.date()
