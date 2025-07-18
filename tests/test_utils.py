import datetime
import pytest
from calmoji.utils import get_first_monday_after, get_first_weekday_of_year, group_phase_days_by_week
from calmoji.types import Phase, PhaseWeekSpan


def test_first_monday_after_basic():
    d = datetime.datetime(2024, 9, 15)  # Sunday
    result = get_first_monday_after(d)
    assert result.weekday() == 0
    assert result.strftime("%Y-%m-%d") == "2024-09-16"

    d2 = datetime.datetime(2024, 9, 16)  # Already Monday
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
        name="Basic",
        start=datetime.datetime(2025, 1, 1),
        end=datetime.datetime(2025, 1, 3),
        start_offset=0,
        end_offset=2,
        emoji="🔑"
    )
    week_spans = group_phase_days_by_week(phase)
    assert len(week_spans) == 1
    assert isinstance(week_spans[0], PhaseWeekSpan)
    assert week_spans[0].days[0].date() == datetime.date(2025, 1, 1)
    assert week_spans[0].days[-1].date() == datetime.date(2025, 1, 3)
