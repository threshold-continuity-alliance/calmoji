# calmoji/config.py

from datetime import datetime
from calmoji.types import Phase

# 🧿 Academic Year Start
YEAR_START_DATE_STR: str = "2024-09-15"
YEAR_START_DATE: datetime = datetime.strptime(YEAR_START_DATE_STR, "%Y-%m-%d")

# 🔁 Slot Generation Settings
SERIES_INTERVAL_WEEKS: int = 3
NUM_SERIES: int = 3
NUM_SLOTS_PER_DAY: int = 8
DAYS_PER_WEEK: int = 5

# 🧭 Optional Regional Support
OCEANIA_SLOTS_ENABLED: bool = False

# 🧪 Output Mode
ENABLE_DRY_RUN: bool = True  # overridden in main.py via CLI

# 📆 Phase Definitions
SEMESTER_PHASES: list[Phase] = [
    Phase("Semester A (Seed)", 0, 97, "🌱"),
    Phase("Winter Break", 98, 111, "❄️"),
    Phase("Semester A (cont.)", 112, 136, "🌾"),
    Phase("Downtime A→B", 137, 150, "🪷"),
    Phase("Semester B (Flame)", 151, 283, "🔥"),
    Phase("Summer Rest", 284, 298, "🐚"),
    Phase("Deep Work Phase", 299, 340, "🧱"),
    Phase("Preflight Prep", 341, 354, "🛫"),
    Phase("Liminal Drift", 355, 365, "🌕"),
]
