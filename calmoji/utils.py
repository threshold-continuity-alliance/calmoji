# calmoji/utils.py

import datetime
from hashlib import md5, sha256
import re
import unicodedata
from typing import Union, Dict, List, Tuple
from collections import defaultdict
from calmoji.types import Phase
from calmoji.focus_blocks_config import ACTIVE_WEEKDAYS


def parse_start_date(start_str):
    return datetime.datetime.strptime(start_str, "%Y-%m-%d")

def format_datetime(dt):
    """Format a datetime object in UTC for .ics files."""
    return dt.strftime('%Y%m%dT%H%M%SZ')

def format_date(d):
    """Format a date object for all-day ICS events."""
    return d.strftime('%Y%m%d')

def format_range_slug(start_date, end_date):
    """Generate a YYYY-MM-DD_to_YYYY-MM-DD slug."""
    return f"{start_date:%Y-%m-%d}_to_{end_date:%Y-%m-%d}"

def format_time_for_tz(dt, tz_name):
    """
    Convert dt to tz and format as string
    """
    raise NotImplementedError("Timezone formatting not yet implemented.")

def get_first_weekday_of_year(year: int, weekday: Union[str, int]) -> datetime.datetime:
    """
    Return the first occurrence of the specified weekday in the given year at 00:05 UTC.

    Args:
        year (int): The calendar year.
        weekday (str|int): The target weekday. Accepts full name ("Monday"),
                           abbreviation ("Mon", "M"), or integer (0=Monday...6=Sunday).

    Returns:
        datetime.datetime: Datetime object for first matching weekday of the year.
    """
    weekday_map = {
        "monday": 0, "mon": 0, "m": 0,
        "tuesday": 1, "tue": 1, "t": 1,
        "wednesday": 2, "wed": 2, "w": 2,
        "thursday": 3, "thu": 3, "h": 3,  # H for "Thursday" in calendars
        "friday": 4, "fri": 4, "f": 4,
        "saturday": 5, "sat": 5, "s": 5,
        "sunday": 6, "sun": 6, "u": 6
    }

    # Normalize input
    if isinstance(weekday, str):
        wd = weekday.lower().strip()
        if wd not in weekday_map:
            raise ValueError(f"Invalid weekday name: {weekday}")
        target_wd = weekday_map[wd]
    elif isinstance(weekday, int) and 0 <= weekday <= 6:
        target_wd = weekday
    else:
        raise ValueError(f"Weekday must be int [0–6] or valid name/abbr, got: {weekday}")

    d = datetime.datetime(year, 1, 1)
    while d.weekday() != target_wd:
        d += datetime.timedelta(days=1)
    return d.replace(hour=0, minute=5)

def generate_uid(dt: datetime.datetime, label: str, namespace: str = "calmoji") -> str:
    raw = f"{namespace}:{dt.isoformat()}:{label}"
    return sha256(raw.encode("utf-8")).hexdigest()[:16]

def get_start_date_from_year(year: int) -> datetime:
    """
    Given a year (e.g. 2024), returns the academic year start date
    (September 15th of that year) as a datetime object.
    """
    return parse_start_date(f"{year}-09-15")

def get_first_monday_after(d):
    """
    Given a datetime object, return the first Monday on or after that date.
    """
    days_ahead = -d.weekday()  # Monday = 0
    if days_ahead < 0:
        days_ahead += 7
    return d + datetime.timedelta(days=days_ahead)

def slugify(value: str, allow_unicode: bool = False) -> str:
    """
    Convert strings to ASCII-safe slugs suitable for filenames or URLs.
    - Replaces spaces with underscores
    - Removes non-word characters
    - Converts to lowercase
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "_", value)


def group_phase_days_by_week(phase: Phase) -> Dict[Tuple[int, int], List[datetime]]:    
    """Return a dict mapping (year, ISO week number) → list of datetime.date within that phase."""
    week_map = defaultdict(list)
    current_day = phase.start

    while current_day <= phase.end:
        if current_day.weekday() in ACTIVE_WEEKDAYS:
            iso_year, iso_week, _ = current_day.isocalendar()
            week_map[(iso_year, iso_week)].append(current_day)
        current_day += datetime.timedelta(days=1)

    return week_map
