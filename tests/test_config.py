# tests/test_config.py

from datetime import datetime, UTC
from calmoji.calendar_config import get_year_start_date
from calmoji.calendar_phases import get_semester_phases
from calmoji.types import Phase


def test_get_year_start_date_returns_expected_default():
    """Ensure academic alignment returns a start date in the correct year."""
    today = datetime.now(UTC)
    expected_year = today.year if today.month < 9 else today.year + 1
    start_date = get_year_start_date("academic")
    assert start_date.year == expected_year, f"Expected year {expected_year}, got {start_date.year}"
    assert start_date.month == 9
    assert start_date.day == 1


def test_generated_semester_phases_have_valid_structure():
    """Ensure generated semester phases have valid structure and offsets."""
    phases = get_semester_phases(get_year_start_date("academic"))
    for i, phase in enumerate(phases):
        assert isinstance(phase, Phase)
        assert isinstance(phase.name, str)
        assert isinstance(phase.start_offset, int)
        assert isinstance(phase.end_offset, int)
        assert isinstance(phase.emoji, str)
        assert phase.start_offset <= phase.end_offset
