#!/usr/bin/env python3

# 🧿 calmoji.py
# This is the ritual conductor.
# It reads the glyphs. It sets the cadence. It writes the time.

import argparse
from pathlib import Path
from datetime import date
from forge.calendar_phases import get_semester_phases
from forge.slot_generator import generate_meeting_slots
from forge.utils import (
    get_start_date_from_year,
    slugify,
    format_range_slug,
)
from forge.ics_writer import (
    write_semester_blocks,
    write_events_to_ics,
    write_ebi48_layer,
)
from forge.dry_run import dry_run

def main():
    parser = argparse.ArgumentParser(description="🧿 calmoji — Ritual Calendar Crafter")
    parser.add_argument("--year", type=int, help="Start year (e.g., 2024)", default=2024)
    parser.add_argument("--dry-run", action="store_true", help="Only show output, don't write ICS files")
    parser.add_argument("--version", action="version", version="EBI48 Generator v2025.1")
    args = parser.parse_args()

    dry_mode = args.dry_run
    year = args.year

    if dry_mode:
        print("\n🔍 DRY RUN ENABLED — No files will be written.\n")

    print("🦊 calmoji — Initiating Ritual Sequence")
    print("=" * 50)

    # 🌅 Step 1: Derive academic year start date and phase structure
    start_date = get_start_date_from_year(year)
    phases = get_semester_phases(start_date)

    # 📂 Step 2: Create output directory if needed
    Path("output").mkdir(parents=True, exist_ok=True)

    # 🗓️ Step 3: Write semester phase blocks (all-day markers)
    if not dry_mode:
        write_semester_blocks(phases, filename=f"output/semester_phases_{year}.ics")

    # 🧱 Step 4: Generate meeting slots per phase
    all_events = []

    for phase in phases:
        print(f"\n📅 Phase: {phase.name} ({phase.start.date()} → {phase.end.date()}) {phase.emoji}")
        events = generate_meeting_slots(phase)
        all_events.extend(events)

        target_path = f"output/meeting_{slugify(phase.name)}_{format_range_slug(phase.start, phase.end)}.ics"

        if dry_mode:
            dry_run(events, phase.name)
        else:
            write_events_to_ics(events, target_path)
            print(f"✅ Wrote: {target_path}")

    # 🗃️ Step 5: Write consolidated meeting calendar
    if not dry_mode:
        consolidated_path = f"output/meeting_all_{start_date.year}.ics"
        write_events_to_ics(all_events, consolidated_path)
        print(f"✅ Wrote: {consolidated_path}")

    # 🧠 Step 6: Emit canonical emoji time overlay (EBI48)
    ebi48_path = f"output/ebi48_layer_{start_date.year}.ics"
    write_ebi48_layer(ebi48_path, start_date.year)
    print(f"✅ Wrote: {ebi48_path}")

    print("\n🎉 Ritual complete. Time is now encoded.\n")

if __name__ == "__main__":
    main()
