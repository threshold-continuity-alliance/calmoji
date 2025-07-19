# calmoji/types.py

from dataclasses import dataclass
from datetime import datetime, date, timedelta
from typing import Optional, List, Union
from calmoji.uid import generate_uid
from hashlib import sha256


@dataclass
class Event:
    start: Union[datetime, date]
    summary: str
    end: Optional[Union[datetime, date]] = None
    uid: Optional[str] = None
    description: str = ""
    emoji: Optional[str] = None
    all_day: bool = False
    recurrence: Optional[str] = None
    private: bool = True
    transparent: bool = True
    
    def __post_init__(self):
        if self.uid is None:
            dt_str = self.start.strftime('%Y%m%dT%H%M%S') if not self.all_day else self.start.strftime('%Y%m%d')
            label = int(sha256((self.summary + dt_str).encode()).hexdigest(), 16) & 0xffffffff
            self.uid = generate_uid(dt=self.start, label=label, namespace="calmoji")

        if self.all_day:
            if isinstance(self.start, datetime):
                self.start = self.start.date()
            if self.end is None:
                self.end = self.start + timedelta(days=1)
            elif isinstance(self.end, datetime):
                self.end = self.end.date()
        else:
            if self.end is None:
                self.end = self.start + timedelta(hours=1)
        

    def dtstart(self) -> str:
        if self.all_day:
            return f"DTSTART;VALUE=DATE:{self.start.strftime('%Y%m%d')}"
        return f"DTSTART:{self.start.strftime('%Y%m%dT%H%M%S')}"

    def dtend(self) -> str:
        if self.all_day:
            return f"DTEND;VALUE=DATE:{self.end.strftime('%Y%m%d')}"
        return f"DTEND:{self.end.strftime('%Y%m%dT%H%M%S')}"

    def to_ics(self) -> str:
        lines = [
            "BEGIN:VEVENT",
            f"UID:{self.uid}",
        ]
        summary = f"{self.emoji} {self.summary}" if self.emoji else self.summary
        lines.append(f"SUMMARY:{summary}")

        if self.all_day:
            lines.append(f"DTSTART;VALUE=DATE:{self.start.strftime('%Y%m%d')}")
            lines.append(f"DTEND;VALUE=DATE:{(self.end).strftime('%Y%m%d')}")
        else:
            lines.append(f"DTSTART:{self.start.strftime('%Y%m%dT%H%M%S')}")
            lines.append(f"DTEND:{self.end.strftime('%Y%m%dT%H%M%S')}")

        if self.description:
            lines.append(f"DESCRIPTION:{self.description}")
        if self.recurrence:
            lines.append(f"RRULE:{self.recurrence}")
        lines.append(f"CLASS:{'PRIVATE' if self.private else 'PUBLIC'}")
        lines.append(f"TRANSP:{'TRANSPARENT' if self.transparent else 'OPAQUE'}")
        lines.append("END:VEVENT")
        
        print(f"📆 Serializing all-day event: {self.summary}")
        print(f"  DTSTART: {self.start}")
        print(f"  DTEND:   {self.end}")
        
        return "\n".join(lines) + "\n"


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

@dataclass
class PhaseWeekSpan:
    start: date
    end: date
    days: List[date]

    @property
    def iso_week_label(self) -> str:
        return f"{self.start.isocalendar()[0]}-W{self.start.isocalendar()[1]:02}"
