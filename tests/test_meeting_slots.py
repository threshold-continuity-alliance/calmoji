# tests/test_meeting_slots.py

import datetime
import unicodedata
import emoji
from collections import defaultdict

from calmoji.calendar_config import get_year_start_date, DEFAULT_ALIGNMENT
from calmoji.calendar_phases import get_semester_phases
from calmoji.slot_generator import generate_meeting_slots
from calmoji.ebi48 import get_emoji_for_time
from calmoji.meeting_slots import MEETING_SLOTS


def to_datetime(hour: int, minute: int) -> datetime.datetime:
    """Helper to create a datetime object for a fixed reference day."""
    return datetime.datetime(2025, 1, 1, hour, minute)


def test_all_slot_labels_are_present():
    for slot in MEETING_SLOTS:
        label = slot[-1]
        assert isinstance(label, str)
        assert ":" in label or "–" in label, f"Slot label missing delimiter: {label}"


def test_utc_hour_ranges_are_valid():
    for _, sh, sm, eh, em, _ in MEETING_SLOTS:
        assert 0 <= sh < 24
        assert 0 <= eh < 24
        assert 0 <= sm < 60
        assert 0 <= em < 60


def test_meeting_slots_duration_and_alignment():
    region_slots = defaultdict(list)

    for region, sh, sm, eh, em, label in MEETING_SLOTS:
        start = to_datetime(sh, sm)
        end = to_datetime(eh, em)
        duration = end - start

        assert duration == datetime.timedelta(minutes=25), f"{region} {label} is not 25 minutes long"
        assert sm in (5, 35), f"{region} {label} does not start at :05 or :35"

        region_slots[region].append((start, end))

    # Ensure no overlapping slots within regions
    for region, slots in region_slots.items():
        slots.sort()
        for i in range(1, len(slots)):
            assert slots[i][0] >= slots[i - 1][1], f"Overlap detected in {region} between slots {i-1} and {i}"


def test_emoji_assignment_for_all_slots():
    seen_emojis = set()

    for region, sh, sm, *_ in MEETING_SLOTS:
        emoji_char, face_name = get_emoji_for_time(to_datetime(sh, sm))
        assert emoji_char and emoji_char.strip(), f"Empty emoji for {region} {face_name}"
        assert emoji_char not in seen_emojis, f"Duplicate emoji {emoji_char} in {region} {face_name}"
        seen_emojis.add(emoji_char)


def test_all_meeting_slots_map_to_valid_emoji():
    for city, sh, sm, *_ in MEETING_SLOTS:
        dt = to_datetime(sh, sm)
        emoji_char, label = get_emoji_for_time(dt)
        assert emoji_char != "❓", f"{city} at {sh:02}:{sm:02} maps to unknown emoji!"
        assert label != "Unknown Face", f"{city} at {sh:02}:{sm:02} maps to unknown label!"


# --- Mecca Slot Tests ---

def get_mecca_events():
    start_date = get_year_start_date(DEFAULT_ALIGNMENT)
    first_phase = get_semester_phases(start_date)[0]
    return [e for e in generate_meeting_slots(first_phase) if e.summary.startswith("Mecca")]


def extract_allowed_mecca_emojis():
    """
    Returns a dictionary of single-character emojis whose Unicode names
    contain safe, reverent keywords (e.g., 'moon', 'star', etc.)
    used to designate Mecca-friendly symbolic time slots.
    """
    safe_keywords = {"circle", "square", "diamond", "star", "moon", "sun", "globe", "symbol", "sparkle"}
    allowed = {}

    for char in emoji.EMOJI_DATA:
        if len(char) != 1:
            continue  # skip multi-codepoint emoji (e.g., flags, skin tones)

        try:
            name = unicodedata.name(char).lower()
        except ValueError:
            continue  # skip non-named characters

        if any(kw in name for kw in safe_keywords):
            allowed[char] = name

    return allowed


def test_mecca_weekdays_are_sunday_to_thursday():
    for evt in get_mecca_events():
        weekday = evt.start.weekday()  # 0 = Monday ... 6 = Sunday
        assert weekday in {6, 0, 1, 2, 3}, f"Invalid Mecca slot on weekday {weekday}"


def test_mecca_slot_durations_are_25_minutes():
    for evt in get_mecca_events():
        duration = int((evt.end - evt.start).total_seconds() // 60)
        assert duration == 25, f"Mecca {evt.summary} is not 25 minutes long"


def test_mecca_slots_have_valid_emoji_faces():
    for evt in get_mecca_events():
        assert "Face" in evt.summary, f"Missing emoji face label in: {evt.summary}"


def test_mecca_slots_use_allowed_emojis():
    allowed_emojis = set(extract_allowed_mecca_emojis().keys())
    for evt in get_mecca_events():
        emoji_char = evt.summary.split(" ")[1]  # e.g., "Mecca 🟦 Blue Square Face"
        assert emoji_char in allowed_emojis, f"Mecca slot uses disallowed emoji: {emoji_char}"
