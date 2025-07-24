# calmoji/types.py

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Optional, List

from calmoji.uid import generate_uid


@dataclass
class Event:
    start: datetime
    summary: str
    end: Optional[datetime] = None
    uid: Optional[str] = None
    description: str = ""
    emoji: Optional[str] = None
    all_day: bool = False
    recurrence: Optional[str] = None
    private: bool = True
    transparent: bool = True

    def __post_init__(self):
        self.start = self._enforce_utc(self.start)
        if self.end:
            self.end = self._enforce_utc(self.end)

        if self.all_day:
            self.start = self.start.replace(hour=0, minute=0, second=0, microsecond=0)
            self.end = (
                self.end.replace(hour=0, minute=0, second=0, microsecond=0)
                if self.end else self.start + timedelta(days=1)
            )
        else:
            self.end = self.end or self.start + timedelta(hours=1)

        if not self.uid:
            dt_str = self.start.strftime('%Y%m%d') if self.all_day else self.start.strftime('%Y%m%dT%H%M%S')
            label = int(sha256((self.summary + dt_str).encode()).hexdigest(), 16) & 0xffffffff
            self.uid = generate_uid(dt=self.start, label=label, namespace="calmoji")

    @staticmethod
    def _enforce_utc(dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        if dt.tzinfo != timezone.utc:
            raise ValueError("Event datetimes must be in UTC.")
        return dt

    def dtstart(self) -> str:
        return (
            f"DTSTART;VALUE=DATE:{self.start.strftime('%Y%m%d')}"
            if self.all_day else
            f"DTSTART:{self.start.strftime('%Y%m%dT%H%M%SZ')}"
        )

    def dtend(self) -> str:
        return (
            f"DTEND;VALUE=DATE:{self.end.strftime('%Y%m%d')}"
            if self.all_day else
            f"DTEND:{self.end.strftime('%Y%m%dT%H%M%SZ')}"
        )

    def to_ics(self) -> list[str]:
        summary = f"{self.emoji} {self.summary}" if self.emoji else self.summary
        safe_description = self.description.replace("\n", "\\n").replace("\r", "")

        lines = [
            "BEGIN:VEVENT",
            f"UID:{self.uid}",
            f"SUMMARY:{summary}",
            self.dtstart(),
            self.dtend(),
        ]

        if self.description:
            lines.append(f"DESCRIPTION:{safe_description}")

        if self.recurrence:
            lines.append(f"RRULE:{self.recurrence}")

        lines.append(f"CLASS:{'PRIVATE' if self.private else 'PUBLIC'}")
        lines.append(f"TRANSP:{'TRANSPARENT' if self.transparent else 'OPAQUE'}")
        lines.append("END:VEVENT")

        if self.all_day:
            print(f"📆 Serializing all-day event: {summary}")
            print(f"  DTSTART: {self.start}")
            print(f"  DTEND:   {self.end}")

        return lines


@dataclass
class Phase:
    name: str
    start_offset: int
    end_offset: int
    emoji: str
    allow_meetings: bool = True
    meeting_density: str = "normal"
    note: Optional[str] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None

    @property
    def duration_days(self) -> Optional[int]:
        if self.start and self.end:
            return (self.end - self.start).days + 1
        return None


@dataclass
class PhaseWeekSpan:
    start: datetime
    end: datetime
    days: List[datetime]

    @property
    def iso_week_label(self) -> str:
        iso_year, iso_week, _ = self.start.isocalendar()
        return f"{iso_year}-W{iso_week:02}"

    def generate_focus_block_events(self, label: str, emoji: str) -> list[Event]:
        blocks_per_day = [
            (3, "Deep Work 1"),
            (11, "Deep Work 2"),
            (19, "Deep Work 3"),
        ]
        all_events = []
        for day in self.days:
            for hour, summary in blocks_per_day:
                start = day.replace(hour=hour, minute=0, second=0, microsecond=0)
                all_events.append(Event(
                    start=start,
                    summary=summary,
                    emoji=emoji,
                    description=f"{label} focus block for ISO week {self.iso_week_label}",
                ))
        return all_events

    def generate_focus_block_glyph_key_event(self, label: str, emoji: str) -> Event:
        anchor = self.start.replace(hour=3, minute=0, second=0, microsecond=0)
        return Event(
            start=anchor,
            summary=f"{label} glyph key for {self.iso_week_label}",
            description="Symbolic anchor point for glyph generation",
            emoji=emoji,
        )

    def generate_all_focus_block_events(self, label: str, emoji: str) -> list[Event]:
        return self.generate_focus_block_events(label, emoji) + [
            self.generate_focus_block_glyph_key_event(label, emoji)
        ]

