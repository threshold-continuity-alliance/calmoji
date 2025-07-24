# calmoji/focus_blocks_writer.py


from pathlib import Path
from calmoji.types import Phase
from calmoji.utils import group_phase_days_by_week, slugify
from calmoji.ics_writer import write_events_to_ics


def write_focus_block_weeklies(phase: Phase, output_dir: Path) -> None:
    week_spans = group_phase_days_by_week(phase)
    for week in week_spans:
        filename = f"{slugify(phase.name)}__{week.iso_week_label}.ics"
        output_path = output_dir / filename
        events = week.generate_all_focus_block_events(label=phase.name, emoji=phase.emoji)
        write_events_to_ics(events, output_path)

