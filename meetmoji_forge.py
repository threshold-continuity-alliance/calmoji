#!/usr/bin/env python3
"""
🦊 ICS Generator - Academic Year Calendar Creator
Generates phase-specific .ics files for semester phases and meeting slots
"""

import os
import sys
import uuid
import re
from datetime import datetime, timedelta
from collections import defaultdict

# =============================================================================
# 🔧 USER-EDITABLE CONFIGURATION
# =============================================================================

year_start = "2025-09-15"  # Academic year start date
use_semesters = True  # True for semester system, False for quarterly
meeting_cycle_weeks = 3  # Meeting recurrence interval in weeks
include_oceania = True  # Include Oceania time slots (Mon & Fri only)
total_meeting_cycles = 40  # Total cycles across the academic year
reset_emoji_per_phase = True  # Reset emoji index per phase

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

def get_semester_phases(start_date):
    """Generate semester planning phases based on start date"""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    
    phases_data = [
        ("Semester A (Seed)", 0, 97),
        ("Winter Break", 98, 111),
        ("Semester A (cont.)", 112, 136),
        ("Downtime A→B", 139, 150),
        ("Semester B (Flame)", 153, 283),
        ("Summer Rest", 287, 298),
        ("Deep Work Phase", 301, 340),
        ("Preflight Prep", 343, 354),
    ]
    
    return [(name, start + timedelta(days=s), start + timedelta(days=e)) 
            for name, s, e in phases_data]

# =============================================================================
# 🕰️ MEETING SLOT CONFIGURATION
# =============================================================================

def get_meeting_slots():
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
    return None

# =============================================================================
# 🚀 MAIN GENERATION FUNCTIONS
# =============================================================================

def generate_meeting_events(dry_run=False):
    """Generate meeting events organized by phase"""
    slots = get_meeting_slots()
    first_monday = get_first_monday_after(year_start)
    phases = get_semester_phases(year_start)
    
    # Dictionary to store events by phase
    phase_events = defaultdict(list)
    
    # Generate all meeting events across the academic year
    for region, start_hour, start_min, end_hour, end_min, local_time in slots:
        # Determine which days this slot runs
        if region == "Oceania":
            days = [0, 4]  # Monday and Friday only
        else:
            days = [0, 1, 2, 3, 4]  # Monday through Friday
        
        for day_offset in days:
            # Create two 25-minute slots per time block
            for minute_offset in [5, 35]:  # :05 and :35 past the hour
                
                # Calculate base slot time
                slot_base = first_monday + timedelta(days=day_offset)
                
                # Generate events for all cycles across the academic year
                for cycle in range(total_meeting_cycles):
                    # Calculate event start time
                    event_start = slot_base + timedelta(
                        weeks=cycle * meeting_cycle_weeks,
                        hours=start_hour,
                        minutes=minute_offset
                    )
                    event_end = event_start + timedelta(minutes=25)
                    event_date = event_start.date()
                    
                    # Find which phase this event falls into
                    phase_name = find_phase_for_date(event_date, phases)
                    
                    # Skip if event falls outside all phases
                    if not phase_name:
                        continue
                    
                    # Calculate emoji index (deterministic per phase if reset_emoji_per_phase)
                    if reset_emoji_per_phase:
                        # Count events in this phase so far for this specific slot
                        phase_event_count = len([e for e in phase_events[phase_name] 
                                               if f"{region}" in e and f"({local_time})" in e])
                        emoji_index = phase_event_count % len(emoji_pool)
                    else:
                        emoji_index = cycle % len(emoji_pool)
                    
                    emoji = emoji_pool[emoji_index]
                    
                    # Create event summary and description
                    summary = f"{region} Slot {emoji} #{cycle + 1} ({local_time})"
                    description = f"Auto-generated 🤖🔐☕️💬 — {phase_name}"
                    
                    if dry_run:
                        print(f"[{phase_name}] {summary}: {format_datetime(event_start)} UTC")
                    else:
                        event = create_meeting_event(summary, event_start, event_end, description)
                        phase_events[phase_name].append(event)
    
    return phase_events

def generate_meeting_ics(dry_run=False):
    """Generate meeting ICS files organized by phase"""
    if dry_run:
        print("\n🔢 DRY RUN: Listing meeting slot schedule\n")
        generate_meeting_events(dry_run=True)
        return
    
    # Generate events
    phase_events = generate_meeting_events(dry_run=False)
    
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

def main():
    """Main execution function"""
    dry_run = len(sys.argv) > 1 and sys.argv[1] == "--dry-run"
    
    if dry_run:
        print("🦊 ICS Generator - Dry Run Mode")
        print("=" * 40)
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
        print(f"   Meeting cycle: every {meeting_cycle_weeks} weeks")
        print(f"   Total cycles: {total_meeting_cycles}")
        print(f"   Oceania slots: {'included' if include_oceania else 'excluded'}")
        print(f"   Emoji reset per phase: {'enabled' if reset_emoji_per_phase else 'disabled'}")
        
        print(f"\n📁 Output directory: output/")
        
        # Generate files
        generate_semester_ics()
        generate_meeting_ics()
        
        print("\n🎉 Calendar files generated successfully!")

if __name__ == "__main__":
    main()
