# calmoji/utils.py

from datetime import datetime, timedelta, timezone
import re
import unicodedata

from collections import defaultdict
from hashlib import sha256
from typing import Union, Dict, List

from calmoji.focus_blocks_config import ACTIVE_WEEKDAYS
from calmoji.types import Phase, PhaseWeekSpan
from calmoji.uid import generate_uid
from calmoji.calendar_config import get_year_start_date


def coerce_to_datetime(obj: Union[datetime]) -> datetime:
    """
    Normalize input to a datetime object.
    
    Parameters:
        obj (datetime): A datetime object (already datetime — function retained for interface symmetry).
    
    Returns:
        datetime: Normalized datetime object.
    """
    if isinstance(obj, datetime):
        return obj
    raise TypeError("Expected datetime")


def coerce_to_utc(dt: datetime) -> datetime:
    """
    Ensure a datetime is timezone-aware and in UTC.
    
    Args:
        dt (datetime): A datetime object.

    Returns:
        datetime: The same moment, explicitly marked as UTC.

    Raises:
        TypeError: If input is not a datetime object.
        ValueError: If input has a non-UTC timezone.
    """
    if not isinstance(dt, datetime):
        raise TypeError(f"Expected datetime object, got {type(dt).__name__}")
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    if dt.tzinfo != timezone.utc:
        raise ValueError("Input datetime must be in UTC.")
    return dt


def format_datetime(dt: datetime) -> str:
    """Format a datetime object in UTC for .ics files."""
    return dt.strftime('%Y%m%dT%H%M%SZ')


def format_range_slug(start_date: datetime, end_date: datetime) -> str:
    """Generate a YYYY-MM-DD_to_YYYY-MM-DD slug."""
    return f"{start_date:%Y-%m-%d}_to_{end_date:%Y-%m-%d}"


def get_first_weekday_of_year(year: int, weekday: Union[str, int]) -> datetime:
    """
    Return the first occurrence of the specified weekday in the given year at 00:05 UTC.
    """
    weekday_map = {
        "monday": 0, "mon": 0, "m": 0,
        "tuesday": 1, "tue": 1, "t": 1,
        "wednesday": 2, "wed": 2, "w": 2,
        "thursday": 3, "thu": 3, "h": 3,
        "friday": 4, "fri": 4, "f": 4,
        "saturday": 5, "sat": 5, "s": 5,
        "sunday": 6, "sun": 6, "u": 6
    }

    if isinstance(weekday, str):
        wd = weekday.lower().strip()
        if wd not in weekday_map:
            raise ValueError(f"Invalid weekday name: {weekday}")
        target_wd = weekday_map[wd]
    elif isinstance(weekday, int) and 0 <= weekday <= 6:
        target_wd = weekday
    else:
        raise ValueError(f"Weekday must be int [0–6] or valid name/abbr, got: {weekday}")

    d = datetime(year, 1, 1, 0, 5, tzinfo=timezone.utc)
    while d.weekday() != target_wd:
        d += timedelta(days=1)
    return d


def get_first_monday_after(d: datetime) -> datetime:
    """Return the first Monday on or after the given date."""
    days_ahead = -d.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return d + timedelta(days=days_ahead)


def slugify(value: str, allow_unicode: bool = False) -> str:
    """
    Convert strings to ASCII-safe slugs suitable for filenames or URLs.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "_", value)


def group_phase_days_by_week(phase: Phase) -> List[PhaseWeekSpan]:
    """Return a list of PhaseWeekSpan objects (with datetimes) for a given Phase."""
    week_map = defaultdict(list)
    current_day = phase.start

    while current_day <= phase.end:
        iso_year, iso_week, _ = current_day.isocalendar()
        week_map[(iso_year, iso_week)].append(current_day)
        current_day += timedelta(days=1)

    return [
        PhaseWeekSpan(start=days[0], end=days[-1], days=days)
        for (iso_year, iso_week), days in sorted(week_map.items())
    ]


def fold_ics_line(line: str, limit: int = 75) -> str:
    """
    🔒 fold_ics_line — Constrain meaning into line-safe fragments

    Folds a long iCalendar content line per RFC 5545 §3.1.
    - Splits at 75 octets max (UTF-8-safe assumption).
    - Continuation lines begin with a single space.
    - Returns a CRLF-joined string ready for ICS output.

    Input: A single logical content line.
    Output: Folded physical lines (CRLF-separated) suitable for transmission.
    """
    folded = []
    while len(line) > limit:
        folded.append(line[:limit])
        line = " " + line[limit:]
    folded.append(line)
    return "\r\n".join(folded)


def unfold_ics_lines(content: str) -> list[str]:
    """
    🔓 unfold_ics_lines — Restore semantic continuity from line folds

    Unfolds a full .ics file (or chunk) by joining continuation lines.
    - Lines beginning with a space are continuations of the previous.
    - Ensures logical content lines are reassembled for parsing or matching.

    Input: Raw .ics content (CRLF or LF-separated).
    Output: List of unfolded logical lines.

    Lines beginning with a single space (0x20) are continuations of the previous line.
    If a continuation appears without a preceding line, raise ValueError.
    """
    lines = content.splitlines()
    unfolded = []

    for i, line in enumerate(lines):
        if line.startswith(" "):
            if not unfolded:
                raise ValueError(f"Malformed ICS: continuation line on line {i+1} with no prior content.")
            unfolded[-1] += line[1:]
        else:
            unfolded.append(line)

    return unfolded


def format_time_for_tz(dt: datetime, tz_name: str) -> str:
    """
    Convert datetime to a string representation in a given timezone.
    [Placeholder for future implementation.]
    """
    raise NotImplementedError("Timezone formatting not yet implemented.")
