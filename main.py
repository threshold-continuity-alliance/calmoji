#!/usr/bin/env python3
# 🧿 Meetmoji Forge — main.py
# This is the ritual conductor.
# It reads the glyphs. It sets the cadence. It writes the time.

import argparse
from pathlib import Path
from forge.calendar_phases import get_semester_phases
from forge.slot_generator import generate_meeting_slots
from forge.utils import get_start_date_from_year, slugify, format_range_slug, get_first_monday_of_year
from forge.ics_writer import write_semester_blocks, write_events_to_ics, write_ebi48_layer
from forge.dry_run import dry_run
from datetime import date

def main():
    parser = argparse.ArgumentParser(description="🧿 Meetmoji Forge — Ritual Calendar Crafter")
    parser.add_argument("--year", type=int, help="Start year (e.g., 2024)", default=2024)
    parser.add_argument("--dry-run", action="store_true", help="Only show output, don't write ICS files")
    parser.add_argument("--version", action="version", version="EBI48 Generator v2025.1")
    args = parser.parse_args()

    dry_mode = args.dry_run
    year = args.year

    if dry_mode:
        print("\n🔍 DRY RUN ENABLED — No files will be written.\n")

    print("🦊 Meetmoji Forge — Initiating Ritual Sequence")
    print("=" * 50)

    # 🌅 Step 1: Get semester phase structure
    start_date = get_start_date_from_year(year)
    phases = get_semester_phases(start_date)

    # 📂 Step 2: Ensure output dir exists
    Path("output").mkdir(parents=True, exist_ok=True)

    # 📅 Step 3: Write all-day semester block markers
    if not dry_mode:
        write_semester_blocks(phases, filename=f"output/semester_phases_{year}.ics")

    consolidated_events = []

    # 🔁 Step 4: Iterate through each phase and generate meeting slots
    for phase in phases:
        phase_name, phase_start, phase_end, phase_emoji = phase

        print(f"\n📅 Phase: {phase_name} ({phase_start.date()} → {phase_end.date()}) {phase_emoji}")
        events = generate_meeting_slots(phase)
        consolidated_events.extend(events)

        target_path = f"output/meeting_{slugify(phase_name)}_{format_range_slug(phase_start, phase_end)}.ics"

        if dry_mode:
            dry_run(events, phase_name)
        else:
            write_events_to_ics(events, target_path)
            print(f"✅ Wrote: {target_path}")

    # 🗃️ Step 5: Write combined ICS file
    if not dry_mode:
        target_path = f"output/meeting_all_{start_date.year}.ics"
        write_events_to_ics(all_events, target_path)
        print(f"✅ Wrote: {target_path}")

    # 🧠 Step 6: Write emoji time legend
    target_path = f"output/ebi48_layer_{start_date.year}.ics"
    write_ebi48_layer(target_path, start_date.year)
    print(f"✅ Wrote: {target_path}")

    print("\n🎉 Ritual complete. Time is now encoded.\n")

if __name__ == "__main__":
    main()
