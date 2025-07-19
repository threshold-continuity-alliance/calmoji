from datetime import datetime
import pytest
from calmoji.utils import get_first_monday_after, get_first_weekday_of_year, group_phase_days_by_week
from calmoji.types import Phase


def test_first_monday_after_basic():
    d = datetime(2024, 9, 15)  # Sunday
    result = get_first_monday_after(d)
    assert result.weekday() == 0
    assert result.strftime("%Y-%m-%d") == "2024-09-16"

    d2 = datetime(2024, 9, 16)  # Already Monday
    assert get_first_monday_after(d2) == d2

def test_first_weekday_of_year_by_name():
    result = get_first_weekday_of_year(2025, "Saturday")
    assert result.weekday() == 5
    assert result.strftime("%Y-%m-%d %H:%M") == "2025-01-04 00:05"

    result = get_first_weekday_of_year(2025, "Monday")
    assert result.weekday() == 0
    assert result.strftime("%Y-%m-%d %H:%M") == "2025-01-06 00:05"

def test_first_weekday_of_year_by_abbr():
    assert get_first_weekday_of_year(2025, "F").weekday() == 4  # Friday
    assert get_first_weekday_of_year(2025, "H").weekday() == 3  # Thursday
    assert get_first_weekday_of_year(2025, "W").weekday() == 2  # Wednesday

def test_first_weekday_of_year_by_int():
    for i in range(7):
        result = get_first_weekday_of_year(2025, i)
        assert result.weekday() == i

def test_first_weekday_of_year_invalid():
    with pytest.raises(ValueError):
        get_first_weekday_of_year(2025, "Blursday")

    with pytest.raises(ValueError):
        get_first_weekday_of_year(2025, 7)

    with pytest.raises(ValueError):
        get_first_weekday_of_year(2025, -1)


def test_group_phase_days_by_week_basic():
    """
    Ensure that days across a 7-day range are correctly grouped by ISO week.
    """
    phase = Phase(
        name="Test Week",
        start=datetime(2025, 3, 3),  # Monday
        end=datetime(2025, 3, 9),    # Sunday
        start_offset=0,
        end_offset=6,
        emoji="🧪"
    )

    week_map = group_phase_days_by_week(phase)
    
    # Should cover exactly one ISO week: 2025-W10
    assert len(week_map) == 1, f"Expected 1 week, got {len(week_map)}"
    
    (year, week), days = list(week_map.items())[0]
    assert year == 2025
    assert week == 10
    assert len(days) >= 1, "Expected at least one focus-eligible day"
    assert all(isinstance(day, datetime) for day in days)
