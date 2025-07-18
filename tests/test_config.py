# tests/test_config.py

from calmoji import config
from calmoji.types import Phase

def test_year_start_date():
    assert config.YEAR_START_DATE.year == 2024
    assert config.YEAR_START_DATE.day == 15

def test_phase_structure():
    for phase in config.SEMESTER_PHASES:
        assert isinstance(phase, Phase)
        assert isinstance(phase.name, str)
        assert isinstance(phase.start_offset, int)
        assert isinstance(phase.end_offset, int)
        assert isinstance(phase.emoji, str)
        assert phase.start_offset <= phase.end_offset
