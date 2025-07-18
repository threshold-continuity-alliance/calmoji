import datetime
from forge.calendar_phases import get_semester_phases
from forge.slot_generator import generate_meeting_slots
from forge.ics_writer import create_event, create_ics_header, create_ics_footer
from forge.utils import get_start_date_from_year
from forge.types import Event


def test_ics_file_line_count(tmp_path):
    testfile = tmp_path / "test_output.ics"

    # Set up a simple event using the new Event dataclass
    start = datetime.datetime(2024, 9, 15, 13, 35)
    end = start + datetime.timedelta(minutes=25)
    event = Event(
        start=start,
        end=end,
        summary="Test Slot",
        description="Test Description",
        emoji="🦊"
    )

    # Write ICS file with one event
    with open(testfile, "w", encoding="utf-8") as f:
        f.write(create_ics_header())
        f.write(create_event(event))
        f.write(create_ics_footer())

    # Read and verify output
    with open(testfile, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Sanity checks
    assert any("UID:" in line for line in lines)
    assert any("BEGIN:VEVENT" in line for line in lines)
    assert any("END:VEVENT" in line for line in lines)
    assert len(lines) > 10  # Enough content to be a valid .ics
