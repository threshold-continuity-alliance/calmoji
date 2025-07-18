# calmoji/dry_run.py

from calmoji.types import Event

def dry_run(events: list[Event], phase_name: str):
    """
    Print a dry-run preview of meeting events for a given phase.
    """
    print(f"\n📆 Phase: {phase_name}")
    print("─" * (12 + len(phase_name)))

    for event in events:
        start_str = event.start.strftime('%a %Y-%m-%d %H:%M')
        summary_str = event.summary or "(No Summary)"
        print(f"{summary_str.ljust(48)}  [{start_str}]")

    print(f"\nTotal: {len(events)} meeting slots\n")
