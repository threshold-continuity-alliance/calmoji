from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Event:
    start: datetime
    end: datetime
    summary: str
    uid: Optional[str] = None
    description: str = ""
    emoji: Optional[str] = None
    all_day: bool = False
    recurrence: Optional[str] = None
    private: bool = True
    transparent: bool = True


# @dataclass
# class Phase:
#     name: str
#     start: datetime
#     end: datetime
#     emoji: str
#     start_date: Optional[datetime] = None
#     end_date: Optional[datetime] = None
#     allow_meetings: bool = True
#     meeting_density: str = "normal"  # Options: 'none', 'low', 'normal', 'high'
#     note: Optional[str] = None

@dataclass
class Phase:
    name: str
    start_offset: int  # offset from YEAR_START_DATE
    end_offset: int
    emoji: str
    allow_meetings: bool = True
    meeting_density: str = "normal"  # Options: 'none', 'low', 'normal', 'high'
    note: Optional[str] = None

    # These are computed later
    start: Optional[datetime] = None
    end: Optional[datetime] = None

    @property
    def duration_days(self) -> Optional[int]:
        """Returns the number of days in the phase, inclusive."""
        if self.start and self.end:
            return (self.end - self.start).days + 1
        return None
