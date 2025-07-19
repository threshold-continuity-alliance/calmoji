# tests/test_meeting_slots.py

import datetime
from collections import defaultdict
from calmoji.meeting_slots import MEETING_SLOTS
from calmoji.utils import get_start_date_from_year
from calmoji.ebi48 import get_emoji_for_time, get_emoji_name_for_slot
from calmoji.calendar_phases import get_semester_phases
from calmoji.slot_generator import generate_meeting_slots
from calmoji.types import Phase

def to_datetime(hour, minute):
    return datetime.datetime(2025, 1, 1, hour, minute)

def test_all_slot_labels_are_present():
    for slot in MEETING_SLOTS:
        city, sh, sm, eh, em, label = slot
        assert isinstance(label, str)
        assert ":" in label or "–" in label
        
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

        # Test 1: Duration is 25 minutes
        assert duration == datetime.timedelta(minutes=25), f"{region} {label} is not 25 minutes long"

        # Test 2: Start minutes must be 5 or 35
        assert sm in (5, 35), f"{region} {label} does not start at :05 or :35"

        region_slots[region].append((start, end))

    # Test 3: No overlaps within a region
    for region, slots in region_slots.items():
        slots.sort()
        for i in range(1, len(slots)):
            prev_end = slots[i-1][1]
            current_start = slots[i][0]
            assert current_start >= prev_end, (
                f"Overlap detected in {region} between slot {i-1} and {i}"
            )

def test_emoji_assignment_for_all_slots():
    seen_emojis = set()

    for region, hour_start, min_start, _, _, label in MEETING_SLOTS:
        emoji, face_name = get_emoji_for_time(to_datetime(hour_start, min_start))

        # Test 1: Returned value is a non-empty string (valid emoji)
        assert isinstance(emoji, str) and emoji.strip(), f"Empty emoji returned for {region} {label}"

        # Test 2: No repeated emoji for different slots
        assert emoji not in seen_emojis, f"Duplicate emoji {emoji} for {region} {label}"
        seen_emojis.add(emoji)

def test_all_meeting_slots_map_to_valid_emoji():
    for city, sh, sm, *_ in MEETING_SLOTS:
        dt = datetime.datetime(2024, 1, 1, sh, sm)
        emoji, label = get_emoji_for_time(dt)
        assert emoji != "❓", f"{city} at {sh:02}:{sm:02} maps to unknown emoji!"
        assert label != "Unknown Face", f"{city} at {sh:02}:{sm:02} maps to unknown label!"

def test_mecca_weekdays_are_sunday_to_thursday():
    start_date = get_start_date_from_year(2024)
    phase = get_semester_phases(start_date)[0]
    events = generate_meeting_slots(phase)

    mecca_events = [e for e in events if e.summary.startswith("Mecca")]

    assert len(mecca_events) > 0

    for evt in mecca_events:
        weekday = evt.start.weekday()
        assert weekday in {6, 0, 1, 2, 3}, f"Invalid Mecca slot on weekday {weekday}"

def test_mecca_slot_durations_are_25_minutes():
    start_date = get_start_date_from_year(2024)
    phase = get_semester_phases(start_date)[0]
    events = generate_meeting_slots(phase)

    for evt in events:
        if evt.summary.startswith("Mecca"):
            duration = (evt.end - evt.start).seconds // 60
            assert duration == 25, f"Mecca {evt.summary} is not 25 minutes long"

def test_mecca_slots_have_valid_emoji_faces():
    start_date = get_start_date_from_year(2024)
    phase = get_semester_phases(start_date)[0]
    events = generate_meeting_slots(phase)

    mecca_slots = [e for e in events if e.summary.startswith("Mecca")]
    for evt in mecca_slots:
        assert "Face" in evt.summary, f"Missing emoji face label in: {evt.summary}"

