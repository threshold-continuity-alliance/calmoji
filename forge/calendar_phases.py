# forge/calendar_phases.py

import datetime
from typing import List, Tuple
from forge.config import SEMESTER_PHASES
from forge.types import Phase
from forge.types import Phase
from forge.config import SEMESTER_PHASES


def get_semester_phases(start_date: datetime.datetime) -> list[Phase]:
    """
    Returns a list of enriched Phase objects starting from the provided academic year start date.
    Each phase includes concrete start/end datetimes and symbolic meeting density metadata.
    """
    enriched = []

    for phase in SEMESTER_PHASES:
        start = start_date + datetime.timedelta(days=phase.start_offset)
        end = start_date + datetime.timedelta(days=phase.end_offset)

        # Apply heuristic enrichment rules
        if any(kw in phase.name for kw in ["Break", "Rest", "Drift"]):
            allow = False
            density = "none"
        elif any(kw in phase.name for kw in ["Downtime", "Prep"]):
            allow = True
            density = "low"
        elif "Deep Work" in phase.name:
            allow = True
            density = "high"
        else:
            allow = True
            density = "normal"

        enriched.append(
            Phase(
                name=phase.name,
                start_offset=phase.start_offset,
                end_offset=phase.end_offset,
                emoji=phase.emoji,
                start=start,
                end=end,
                allow_meetings=allow,
                meeting_density=density,
                note=f"Auto-tagged density: {density}",
            )
        )

    return enriched
