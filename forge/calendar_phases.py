# forge/calendar_phases.py

import datetime
from typing import List, Tuple
from forge.config import SEMESTER_PHASES
from forge.types import Phase


# def get_semester_phases(start_date: datetime.date) -> List[Phase]:
#     """
#     Generate semester planning phases based on a flexible anchor date (YYYY-MM-DD).

#     Args:
#         start_date (datetime.date): Anchor date for phase calculation (e.g., start of academic year)

#     Returns:
#         List of tuples in format:
#         (phase_name: str, start: datetime.date, end: datetime.date, emoji: str)

#     Example:
#         >>> get_semester_phases(datetime.date(2025, 9, 15))
#         [('Semester A (Seed)', datetime.date(...), ... , '🌱'), ...]
#     """

#     # Defensive check for SEMESTER_PHASES validity
#     for phase in SEMESTER_PHASES:
#         if len(phase) != 4:
#             raise ValueError(f"Invalid SEMESTER_PHASES entry: {phase}")
#     phases = []
#     # for name, offset_start, offset_end, emoji in SEMESTER_PHASES:
#     for phase in SEMESTER_PHASES:
#         start = phase.start_date + datetime.timedelta(days=phase.start_offset)
#         end = start_date + datetime.timedelta(days=phase.end_offset)
#         phases.append(Phase(name=name, start=phase_start, end=phase_end, emoji=emoji))
#     return phases


from datetime import datetime, timedelta
from forge.types import Phase
from forge.config import SEMESTER_PHASES


def get_semester_phases(start_date: datetime) -> list[Phase]:
    """
    Returns a list of enriched Phase objects starting from the provided academic year start date.
    Each phase includes concrete start/end datetimes and symbolic meeting density metadata.
    """
    enriched = []

    for phase in SEMESTER_PHASES:
        start = start_date + timedelta(days=phase.start_offset)
        end = start_date + timedelta(days=phase.end_offset)

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

