# tests/test_focus_blocks_writer.py

import datetime
import os
from calmoji.types import Phase, Event
from calmoji.focus_blocks_writer import generate_focus_block_events, group_phase_days_by_week, write_focus_blocks_weekly
from calmoji.focus_blocks_config import FOCUS_BLOCKS, ACTIVE_WEEKDAYS


def test_focus_block_generation_respects_weekdays():
    dummy_phase = Phase(
        name="Test Phase",
        start=datetime.datetime(2025, 1, 1),  # Wednesday (weekday=2)
        end=datetime.datetime(2025, 1, 3),    # Friday (weekday=4)
        start_offset=0,
        end_offset=2,
        emoji="📆"
    )

    events = generate_focus_block_events([dummy_phase])
    active_weekdays_set = set(ACTIVE_WEEKDAYS)

    assert all(e.start.weekday() in active_weekdays_set for e in events)
    assert len(events) == 3 * len(FOCUS_BLOCKS)


def test_final_block_has_torii():
    dummy_phase = Phase(
        name="Short",
        start=datetime.datetime(2025, 1, 1),  # Wednesday
        end=datetime.datetime(2025, 1, 1),
        start_offset=0,
        end_offset=0,
        emoji="🌀"
    )

    events = generate_focus_block_events([dummy_phase])
    assert events  # Ensure we have events
    last_block = sorted(events, key=lambda e: e.start)[-1]
    assert last_block.emoji == "⛩️"


def test_total_events_per_day():
    dummy_phase = Phase(
        name="Two Day",
        start=datetime.datetime(2025, 1, 1),  # Wednesday
        end=datetime.datetime(2025, 1, 2),    # Thursday
        start_offset=0,
        end_offset=1,
        emoji="📆"
    )

    events = generate_focus_block_events([dummy_phase])
    events_by_day = {}
    for e in events:
        key = e.start.date()
        events_by_day.setdefault(key, []).append(e)

    assert all(len(blocks) == len(FOCUS_BLOCKS) for blocks in events_by_day.values())


def test_edge_week_behavior():
    phase = Phase(
        name="Edge Case Phase",
        start=datetime.datetime(2025, 1, 1),  # Wednesday
        end=datetime.datetime(2025, 1, 6),    # Monday (included)
        start_offset=0,
        end_offset=0,
        emoji="🌀"
    )

    week_map = group_phase_days_by_week(phase)
    assert week_map, "Expected grouped days"

    weeks = sorted(week_map.keys())
    first_week_days = week_map[weeks[0]]
    last_week_days = week_map[weeks[-1]]

    assert first_week_days[0].date() == datetime.date(2025, 1, 1)
    assert last_week_days[-1].date() == datetime.date(2025, 1, 6)


def test_torii_emoji_on_final_block():
    dummy_phase = Phase(
        name="Single Day Phase",
        start=datetime.datetime(2025, 1, 2),  # Thursday
        end=datetime.datetime(2025, 1, 2),
        start_offset=0,
        end_offset=0,
        emoji="🌀"
    )

    events = generate_focus_block_events([dummy_phase])
    assert events
    final_event = sorted(events, key=lambda e: e.start)[-1]
    assert final_event.emoji == "⛩️"


def test_glyph_key_event_written_even_when_alone(tmp_path):
    """Ensure the glyph key event is written even if it's the only event in the week."""

    saturday_only_phase = Phase(
        name="Glyph Test Phase",
        start=datetime.datetime(2025, 1, 4),  # Saturday (excluded by ACTIVE_WEEKDAYS)
        end=datetime.datetime(2025, 1, 4),
        start_offset=0,
        end_offset=0,
        emoji="🧪",
    )

    output_dir = tmp_path / "output"
    output_dir.mkdir()
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        write_focus_blocks_weekly([saturday_only_phase])
        expected_filename = output_dir / "focus_blocks_glyph_test_phase_2025_W01.ics"
        assert expected_filename.exists(), "ICS file with glyph event was not created"

        content = expected_filename.read_text(encoding="utf-8")
        summaries = [line for line in content.splitlines() if line.startswith("SUMMARY:")]
        glyph_lines = [s for s in summaries if "Focus Block Glyph Key" in s]

        assert len(glyph_lines) == 1, "Expected exactly one glyph key event in the ICS"
    finally:
        os.chdir(original_cwd)
