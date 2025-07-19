# tests/test_focus_blocks_writer.py

import datetime
import os
from pathlib import Path
from calmoji.types import Phase
from calmoji.focus_blocks_writer import generate_focus_block_events, group_phase_days_by_week, write_focus_blocks_weekly
from calmoji.focus_blocks_config import FOCUS_BLOCKS, ACTIVE_WEEKDAYS


def test_focus_block_generation_respects_weekdays():
    dummy_phase = Phase(
        name="Test Phase",
        start=datetime.datetime(2025, 1, 1),
        end=datetime.datetime(2025, 1, 3),
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
        start=datetime.datetime(2025, 1, 1),
        end=datetime.datetime(2025, 1, 1),
        start_offset=0,
        end_offset=0,
        emoji="🌀"
    )
    events = generate_focus_block_events([dummy_phase])
    assert events
    last_block = sorted(events, key=lambda e: e.start)[-1]
    assert last_block.emoji == "⛩️"


def test_total_events_per_day():
    dummy_phase = Phase(
        name="Two Day",
        start=datetime.datetime(2025, 1, 1),
        end=datetime.datetime(2025, 1, 2),
        start_offset=0,
        end_offset=1,
        emoji="📆"
    )
    events = generate_focus_block_events([dummy_phase])
    events_by_day = {}
    for e in events:
        key = e.start.date()
        events_by_day.setdefault(key, []).append(e)
    # Ensure that every active day has exactly one block per FOCUS_BLOCK
    active_days = set(
        d for d in (dummy_phase.start + datetime.timedelta(days=i) for i in range((dummy_phase.end - dummy_phase.start).days + 1))
        if d.weekday() in ACTIVE_WEEKDAYS
    )

    assert all(len(events_by_day.get(day.date(), [])) == len(FOCUS_BLOCKS) for day in active_days)


def test_edge_week_behavior():
    phase = Phase(
        name="Edge Case Phase",
        start=datetime.datetime(2025, 1, 1),
        end=datetime.datetime(2025, 1, 6),
        start_offset=0,
        end_offset=0,
        emoji="🌀"
    )
    week_spans = group_phase_days_by_week(phase)
    assert week_spans, "Expected grouped spans"

    all_days = [day for span in week_spans for day in span.days]
    assert all_days[0].date() == datetime.date(2025, 1, 1)
    assert all_days[-1].date() == datetime.date(2025, 1, 6)


def test_torii_emoji_on_final_block():
    dummy_phase = Phase(
        name="Single Day Phase",
        start=datetime.datetime(2025, 1, 2),
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
    saturday_only_phase = Phase(
        name="Glyph Test Phase",
        start=datetime.datetime(2025, 1, 4),
        end=datetime.datetime(2025, 1, 4),
        start_offset=0,
        end_offset=0,
        emoji="🧪",
    )

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Patch CWD temporarily to simulate output behavior
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        write_focus_blocks_weekly([saturday_only_phase])
        # 🛠 Correct the filename logic to match the current generator behavior
        expected_filename = output_dir / "focus_blocks_glyph_test_phase_2025-W01.ics"

        # ✅ If the output_dir was hardcoded in writer, path may be relative to cwd
        if not expected_filename.exists():
            expected_filename = Path("output") / "focus_blocks_glyph_test_phase_2025-W01.ics"

        assert expected_filename.exists(), f"ICS file was not created: {expected_filename}"

        content = expected_filename.read_text(encoding="utf-8")
        summaries = [line for line in content.splitlines() if line.startswith("SUMMARY:")]
        glyph_lines = [line for line in content.splitlines() if "Glyph Key" in line]

        assert len(glyph_lines) == 1, "Expected exactly one glyph key event in the ICS file"
    finally:
        os.chdir(original_cwd)
