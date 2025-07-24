# calmoji/calendar_config.py

from datetime import datetime, UTC
from typing import List

from calmoji.types import Phase


# 🧭 Alignment definitions — single source of truth
ALIGNMENTS = {
    "calendar": lambda year: datetime(year, 1, 1),
    "academic": lambda year: datetime(year, 9, 1),
    "fiscal_us": lambda year: datetime(year, 10, 1),
    "fiscal_eu": lambda year: datetime(year, 1, 1),
    "japanese_school": lambda year: datetime(year, 4, 1),
    "indian_fiscal": lambda year: datetime(year, 4, 1),
    "chinese_lunar": lambda year: datetime(2024, 2, 10),  # TODO
    "islamic_hijri": lambda year: datetime(2024, 7, 7),   # TODO
}

# 🎯 Constants derived from the keys
ALIGNMENT_MODES = set(ALIGNMENTS.keys())
DEFAULT_ALIGNMENT = "calendar"


def get_year_start_date(alignment: str = DEFAULT_ALIGNMENT, year: int | None = None) -> datetime:
    """
    Returns the start datetime for a given alignment mode and year.
    Defaults to the current year if not provided.

    Args:
        alignment (str): One of the predefined alignment modes.
        year (int, optional): Year to compute the start date for. Defaults to current year.

    Returns:
        datetime: Midnight datetime object for the given alignment's start-of-year.
    """
    if year is None:
        year = datetime.now(UTC).year

    try:
        return ALIGNMENTS[alignment](year)
    except KeyError:
        return ALIGNMENTS[DEFAULT_ALIGNMENT](year)


def get_semester_phase_definitions() -> List[Phase]:
    """Return symbolic semester phases (with offsets and emoji) for a canonical year pattern."""
    return [
        Phase("Semester A (Seed)", 0, 97, "🌱"),
        Phase("Winter Break", 98, 111, "❄️"),
        Phase("Semester A (cont.)", 112, 136, "🌾"),
        Phase("Downtime A→B", 137, 150, "🪷"),
        Phase("Semester B (Flame)", 151, 283, "🔥"),
        Phase("Summer Rest", 284, 298, "🐚"),
        Phase("Deep Work Phase", 299, 340, "🧠"),
        Phase("Autumn Drift", 341, 364, "🍂"),
    ]
