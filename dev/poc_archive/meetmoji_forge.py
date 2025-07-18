#!/usr/bin/env python3

"""
🦊 Meetmoji Forge — The Ritual Calendar Crafter — Where Time Meets Glyph

Generates `.ics` calendar files for semester-aligned project phases and
interleaved tri-weekly meeting slots, using deterministic emoji glyphs.

Because your visual processing cortex deserves better than guilt.


"""

from forge.config import START_DATE
from calendar_phases import get_semester_phases
from forge.emoji_clock import get_emoji_for_hour
from forge.slot_generator import generate_meeting_slots_for_phase
from forge.ics_writer import write_ics_files
from forge.dry_run import display_slot_preview
from forge.utils import parse_start_date

import os
import sys
import uuid
import re
from datetime import datetime, timedelta, time, timezone
from collections import defaultdict

# =============================================================================
# 🔧 ARGUMENT PARSING
# =============================================================================

def parse_arguments():
    """Parse command line arguments"""
    dry_run = "--dry-run" in sys.argv
    
    # Parse year argument
    year = 2025  # default
    for arg in sys.argv:
        if arg.startswith("--year="):
            try:
                year = int(arg.split("=")[1])
            except ValueError:
                print(f"❌ Error: Invalid year format in {arg}")
                sys.exit(1)
    
    # Construct year_start based on year
    year_start = f"{year}-09-15"
    
    return dry_run, year_start

# Parse arguments at startup
dry_run_mode, year_start = parse_arguments()

# =============================================================================
# 🔧 USER-EDITABLE CONFIGURATION
# =============================================================================

use_semesters = True  # True for semester system, False for quarterly
meeting_cycle_weeks = 3  # Meeting recurrence interval in weeks
include_oceania = True  # Include Oceania time slots (Mon & Fri only)

# 🐾 Curated emoji pool (150 glyphs)
emoji_pool = [
    "🦊", "🐺", "🦝", "🐱", "🐈", "🐈‍⬛", "🐯", "🦁", "🐅", "🐆", "🐴", "🦓", "🦄", "🐮", "🐂", "🐃",
    "🐷", "🐖", "🐗", "🐏", "🐑", "🦙", "🐐", "🐪", "🐫", "🦒", "🐘", "🦣", "🐕", "🐩", "🦮", "🐕‍🦺",
    "☠️", "🐇", "🐿️", "🦔", "🦇", "🐓", "🐔", "🐣", "🦉", "🦅", "🕊️", "🦤", "🐢", "🦎", "🐍", "🐊",
    "🐳", "🐋", "🐬", "🐟", "🐠", "🐡", "🦈", "🦭", "🐙", "🦑", "🦐", "🦞", "🦀", "🐌", "🦋", "🐛",
    "🐜", "🐝", "🪲", "🪳", "🕷", "🕸", "🦂", "🪰", "🪱", "🌸", "🌼", "🌻", "🌺", "🌹", "🌷", "🌱",
    "🌿", "🍃", "🍂", "🍁", "🍄", "🌵", "🌴", "🌳", "🌲", "🪵", "🪨", "🔥", "💧", "🌊", "🌫️", "☁️",
    "🌤️", "⛅", "🌥️", "🌦️", "🌧️", "🌩️", "🌨️", "❄️", "🌙", "⭐", "🌟", "✨", "⚡", "☀️", "🌞",
    "🪐", "🌌", "🌠", "🌀", "🎐", "🧭", "📡", "⏳", "📅", "🗓", "📌", "📍", "📎", "✏️", "🖋", "🗂",
    "📘", "📕", "📙", "📗", "📖", "🪶", "🧵", "🧶", "🪡", "🔮", "🕯️", "🛠", "🔧", "🧰", "🧪", "🧬",
    "🪜", "🛖", "🛸", "🛰️", "🚀", "🪂", "🏕️", "🧭"
]

# =============================================================================
# 📅 SEMESTER PLANNING PHASES
# =============================================================================

def count_meeting_cycles(start_date, end_date, meeting_cycle_weeks=3):
    """
    Count how many tri-weekly meetings can occur between two dates
    (starting from the first Monday on or after start_date).
    """
    first_monday = get_first_monday_after(start_date.strftime("%Y-%m-%d"))
    current = first_monday
    count = 0
    while current <= end_date:
        count += 1
        current += timedelta(weeks=meeting_cycle_weeks)
    return count

# =============================================================================
# 🕰️ MEETING SLOT CONFIGURATION
# =============================================================================

def get_meeting_slots(include_oceania):
    """Define meeting time slots with UTC times and local time labels"""
    slots = [
        ("Tokyo", 4, 30, 6, 30, "13:30–14:30 JST"),
        ("South Asia", 7, 30, 9, 30, "13:00–14:00 IST"),
        ("Brussels", 11, 30, 13, 30, "13:30–14:30 CEST"),
        ("DC", 17, 30, 19, 30, "13:30–14:30 EDT"),
        ("Seattle", 20, 30, 22, 30, "13:30–14:30 PDT"),
    ]
    
    if include_oceania:
        slots.append(("Oceania", 5, 30, 7, 30, "15:30–16:30 AEST"))
    
    return slots

# =============================================================================
# 📝 ICS FILE GENERATION
# =============================================================================

def create_ics_header():
    """Create ICS file header"""
    return """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Academic Calendar Generator//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
"""

def create_ics_footer():
    """Create ICS file footer"""
    return "END:VCALENDAR\n"

def format_datetime(dt):
    """Format datetime for ICS"""
    return dt.strftime("%Y%m%dT%H%M%SZ")

def create_all_day_event(summary, start_date, end_date):
    """Create an all-day event"""
    uid = str(uuid.uuid4())
    end_inclusive = end_date + timedelta(days=1)
    
    return f"""BEGIN:VEVENT
UID:{uid}
SUMMARY:{summary}
DTSTART;VALUE=DATE:{start_date.strftime('%Y%m%d')}
DTEND;VALUE=DATE:{end_inclusive.strftime('%Y%m%d')}
CLASS:PRIVATE
TRANSP:TRANSPARENT
END:VEVENT
"""

def create_meeting_event(summary, start_datetime, end_datetime, description=""):
    """Create a meeting event"""
    uid = str(uuid.uuid4())
    
    event = f"""BEGIN:VEVENT
UID:{uid}
SUMMARY:{summary}
DTSTART:{format_datetime(start_datetime)}
DTEND:{format_datetime(end_datetime)}
CLASS:PRIVATE
"""
    
    if description:
        event += f"DESCRIPTION:{description}\n"
    
    event += "END:VEVENT\n"
    return event

def slugify(name):
    """Convert phase name to filename-safe slug"""
    return re.sub(r'\W+', '_', name.strip()).lower()

def get_first_monday_after(date_str):
    """Get the first Monday on or after the given date"""
    d = datetime.strptime(date_str, "%Y-%m-%d")
    days_ahead = -d.weekday()  # Monday is 0
    if days_ahead < 0:  # If we're past Monday this week
        days_ahead += 7
    return d + timedelta(days=days_ahead)

def find_phase_for_date(date, phases):
    """Find which phase a given date falls into"""
    for phase_name, phase_start, phase_end in phases:
        if phase_start.date() <= date <= phase_end.date():
            return phase_name
    return "Gap Days 🌑"

# =============================================================================
# 🚀 MAIN GENERATION FUNCTIONS
# =============================================================================


def generate_meeting_events(year_start, phases, meeting_slots, emoji_pool, dry_run=False, use_utc=True):
    phase_events = defaultdict(list)
    emoji_index = 0
    series_counters = defaultdict(int)  # per-slot counters

    for phase in phases:
        start_date, end_date, phase_name, phase_emoji = phase
        current_date = start_date
        emojis_this_phase = emoji_pool.copy()
        emoji_index = 0

        while current_date <= end_date:
            # Only include Mondays
            if current_date.weekday() == 0:
                for slot in meeting_slots:
                    region, slot_start_hour, slot_start_minute, slot_end_hour, slot_end_minute, label = slot
                    key = f"{region}_{slot_start_hour}_{slot_start_minute}"

                    # Assign deterministic emoji
                    if emoji_index >= len(emojis_this_phase):
                        continue  # Avoid out-of-range errors
                    emoji = emojis_this_phase[emoji_index]
                    emoji_index += 1

                    series_counters[key] += 1
                    series_number = series_counters[key]

                    # Convert to datetime
                    start_dt = datetime.combine(current_date, time(slot_start_hour, slot_start_minute))
                    end_dt = datetime.combine(current_date, time(slot_end_hour, slot_end_minute))

                    if use_utc:
                        start_dt = start_dt.replace(tzinfo=timezone.utc)
                        end_dt = end_dt.replace(tzinfo=timezone.utc)

                    summary = f"{region} Slot {emoji} #{series_number} ({label})"
                    description = f"Auto-generated 🤖🔐☕️💬 time slot — {phase_name}"

                    if dry_run:
                        print(f"📅 {start_dt.isoformat()} — {summary}")
                        continue

                    event = Event()
                    event.name = summary
                    event.begin = start_dt
                    event.end = end_dt
                    event.description = description
                    event.location = region
                    event.categories = ["Meetmoji Slot", region, phase_name]

                    phase_events[phase_name].append(event)

            # Advance by 1 day
            current_date += timedelta(days=1)

    if dry_run:
        return None  # Avoid writing files

    return phase_events


def generate_meeting_ics(dry_run=False):
    """Generate meeting ICS files organized by phase"""

    phases = get_semester_phases(year_start)
    meeting_slots = get_meeting_slots(include_oceania)
    
    if dry_run:
        print("\n🔢 DRY RUN: Listing meeting slot schedule\n")
        phase_events = generate_meeting_events(year_start=year_start,
            phases=phases,
            meeting_slots=meeting_slots,
            emoji_pool=emoji_pool,
            dry_run=True)
        return {}
    
    # Generate events
    phase_events = generate_meeting_events(year_start=year_start,
        phases=phases,
        meeting_slots=meeting_slots,
        emoji_pool=emoji_pool,
        dry_run=False)
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Generate ICS file for each phase
    for phase_name, events in phase_events.items():
        if not events:
            continue
            
        filename = f"output/meeting_{slugify(phase_name)}.ics"
        ics_content = create_ics_header() + ''.join(events) + create_ics_footer()
        
        with open(filename, "w", encoding='utf-8') as f:
            f.write(ics_content)
        
        print(f"📁 Generated: {filename} ({len(events)} events)")

def generate_semester_ics():
    """Generate semester phases ICS file"""
    phases = get_semester_phases(year_start)
    
    content = create_ics_header()
    for name, start, end in phases:
        content += create_all_day_event(name, start, end)
    content += create_ics_footer()
    
    os.makedirs("output", exist_ok=True)
    filename = "output/semester_phases.ics"
    
    with open(filename, "w", encoding='utf-8') as f:
        f.write(content)
    
    print(f"📁 Generated: {filename}")

# =============================================================================
# 🧪 UNIT TEST STUB FOR FUTURE VERIFICATION
# =============================================================================

def test_calendar_generator():
    """
    Unit test stub for calendar generation verification
    Run with: python -m pytest ics-generator.py::test_calendar_generator -v
    """
    import tempfile
    
    # Test configuration
    test_year_start = "2025-09-15"
    
    # Test semester phases generation
    phases = get_semester_phases(test_year_start)
    
    # Verify we have 8 phases
    assert len(phases) == 8, f"Expected 8 phases, got {len(phases)}"
    
    # Verify first phase starts on correct date
    first_phase = phases[0]
    assert first_phase[0] == "Semester A (Seed)", f"First phase should be 'Semester A (Seed)', got '{first_phase[0]}'"
    assert first_phase[1].strftime("%Y-%m-%d") == test_year_start, f"First phase should start on {test_year_start}"
    
    # Verify last phase is Preflight Prep
    last_phase = phases[-1]
    assert last_phase[0] == "Preflight Prep", f"Last phase should be 'Preflight Prep', got '{last_phase[0]}'"
    
    # Test meeting slots configuration
    slots = get_meeting_slots()
    expected_slots = 6 if include_oceania else 5
    assert len(slots) == expected_slots, f"Expected {expected_slots} slots, got {len(slots)}"
    
    # Test first Monday calculation
    first_monday = get_first_monday_after(test_year_start)
    assert first_monday.weekday() == 0, "First Monday should be a Monday (weekday 0)"
    
    # Test argument parsing
    import sys
    old_argv = sys.argv.copy()
    try:
        sys.argv = ["script.py", "--year=2024", "--dry-run"]
        dry_run, year_start = parse_arguments()
        assert dry_run == True, "Should detect --dry-run"
        assert year_start == "2024-09-15", f"Should set year_start to 2024-09-15, got {year_start}"
    finally:
        sys.argv = old_argv
    
    print("✅ All unit tests passed!")

def run_tests():
    """Run unit tests manually"""
    print("🧪 Running unit tests...")
    try:
        test_calendar_generator()
        print("🎉 All tests passed successfully!")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"💥 Test error: {e}")
        return False
    return True

# =============================================================================
# 🚀 MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function"""
    if dry_run_mode:
        print("🦊 ICS Generator - Dry Run Mode")
        print("=" * 40)
        print(f"📅 Using year start: {year_start}")
        generate_meeting_ics(dry_run=True)
    else:
        print("🦊 ICS Generator - Academic Year Calendar Creator")
        print("=" * 50)
        
        # Display configuration
        phases = get_semester_phases(year_start)
        calendar_start = phases[0][1]
        calendar_end = phases[-1][2]
        first_monday = get_first_monday_after(year_start)
        
        print(f"📅 Calendar Coverage:")
        print(f"   Start: {calendar_start.strftime('%Y-%m-%d')} ({phases[0][0]})")
        print(f"   End:   {calendar_end.strftime('%Y-%m-%d')} ({phases[-1][0]})")
        print(f"   Meeting slots start: {first_monday.strftime('%Y-%m-%d')} (First Monday)")
        print(f"   Total span: {(calendar_end - calendar_start).days} days")
        
        print(f"\n🔧 Configuration:")
        print(f"   Year start: {year_start}")
        print(f"   Meeting cycle: every {meeting_cycle_weeks} weeks")
        total_cycles = count_meeting_cycles(calendar_start, calendar_end, meeting_cycle_weeks)
        print(f"   Total cycles: {total_cycles}")
        print(f"   Oceania slots: {'included' if include_oceania else 'excluded'}")
        print(f"   Emoji assignment: reset per phase")
        
        print(f"\n📁 Output directory: output/")
        
        # Generate files
        generate_semester_ics()
        generate_meeting_ics()
        
        print("\n🎉 Calendar files generated successfully!")

if __name__ == "__main__":
    # Check if running tests
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_tests()
    else:
        main()
