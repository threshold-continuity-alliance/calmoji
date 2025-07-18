# tests/test_calendar_phases.py

import datetime
from forge.calendar_phases import get_semester_phases
from forge.config import SEMESTER_PHASES, YEAR_START_DATE
from forge.types import Phase


def test_semester_phase_count():
    phases = get_semester_phases(YEAR_START_DATE)
    assert len(phases) == len(SEMESTER_PHASES)


def test_get_semester_phases_returns_expected_structure():
    anchor_date = datetime.datetime(2024, 9, 15)
    phases = get_semester_phases(anchor_date)

    assert isinstance(phases, list)
    assert all(isinstance(p, Phase) for p in phases)
    assert len(phases) == len(SEMESTER_PHASES)

    for i, phase in enumerate(phases):
        ref = SEMESTER_PHASES[i]
        expected_start = anchor_date + datetime.timedelta(days=ref.start_offset)
        expected_end = anchor_date + datetime.timedelta(days=ref.end_offset)

        assert phase.name == ref.name
        assert phase.emoji == ref.emoji
        assert phase.start == expected_start
        assert phase.end == expected_end


def test_phase_enrichment_fields_exist():
    phases = get_semester_phases(datetime.datetime(2024, 9, 15))
    for p in phases:
        assert hasattr(p, "meeting_density")
        assert hasattr(p, "allow_meetings")
        assert hasattr(p, "note")
        assert p.start <= p.end


def test_phase_density_tags():
    phases = get_semester_phases(datetime.datetime(2024, 9, 15))

    for p in phases:
        if any(kw in p.name for kw in ["Break", "Rest", "Drift"]):
            assert p.meeting_density == "none"
            assert p.allow_meetings is False
        elif any(kw in p.name for kw in ["Downtime", "Prep"]):
            assert p.meeting_density == "low"
            assert p.allow_meetings is True
        elif "Deep Work" in p.name:
            assert p.meeting_density == "high"
            assert p.allow_meetings is True
        else:
            assert p.meeting_density == "normal"
            assert p.allow_meetings is True


def test_phase_duration_computation():
    phases = get_semester_phases(YEAR_START_DATE)

    for p in phases:
        expected = (p.end - p.start).days + 1
        assert p.duration_days == expected, f"{p.name} has incorrect duration"
