# tests/test_2039.py

import io
from datetime import datetime
from calmoji.ics_writer import generate_ics_file
from calmoji.pipeline import get_all_events


def test_only_2039_appears_in_calendar_output():
    buf = io.StringIO()
    generate_ics_file(datetime(2039, 1, 1, 0, 0), buf)
    output = buf.getvalue()

    # Scan for all year-like tokens in DTSTART and DTEND lines
    years = set()
    for line in output.splitlines():
        if "DTSTART" in line or "DTEND" in line:
            for token in line.split(":"):
                for year in range(2020, 2050):
                    if str(year) in token:
                        years.add(year)
    assert years == {2039}, f"Unexpected years in output: {years}"
