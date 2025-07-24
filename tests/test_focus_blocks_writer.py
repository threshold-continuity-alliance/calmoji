import datetime
import os
from pathlib import Path

from calmoji.types import Phase
from calmoji.focus_blocks_writer import (
    generate_focus_block_events,
    group_phase_days_by_week,
    write_focus_blocks_weekly,
)
from calmoji.focus_blocks_config import FOCUS_BLOCKS, ACTIVE_WEEKDAYS, DEFAULT_ACTIVE_WEEKDAYS
from calmoji.utils import unfold_ics_lines


def make_phase(name: str, start: str, end: str, emoji: str = "📆") -> Phase:
    """Create a Phase from ISO-formatted date strings."""
    start_dt = datetime.datetime.fromisoformat(start)
    end_dt = datetime.datetime.fromisoformat(end)
    return Phase(
        name=name,
        start=start_dt,
        end=end_dt,
        start_offset=0,
        end_offset=(end_dt - start_dt).days,
        emoji=emoji,
    )


def test_focus_blocks_respect_active_weekdays():
    phase = make_phase("Week Check", "2025-01-01", "2025-01-03")
    events = generate_focus_block_events([phase])
    active_days = set(ACTIVE_WEEKDAYS or DEFAULT_ACTIVE_WEEKDAYS)

    assert all(e.start.weekday() in active_days for e in events)
    assert len(events) == 3 * len(FOCUS_BLOCKS)


def test_each_day_has_expected_focus_block_count():
    phase = make_phase("Two Day", "2025-01-01", "2025-01-02")
    events = generate_focus_block_events([phase])

    events_by_day = {}
    for event in events:
        events_by_day.setdefault(event.start.date(), []).append(event)

    active_weekdays = set(ACTIVE_WEEKDAYS or DEFAULT_ACTIVE_WEEKDAYS)
    active_days = {
        (phase.start + datetime.timedelta(days=i)).date()
        for i in range((phase.end - phase.start).days + 1)
        if (phase.start + datetime.timedelta(days=i)).weekday() in active_weekdays
    }

    for day in active_days:
        actual = len(events_by_day.get(day, []))
        expected = len(FOCUS_BLOCKS)
        assert actual == expected, f"Expected {expected} events on {day}, found {actual}"


def test_group_phase_days_by_week_consistency():
    phase = make_phase("Edge Case", "2025-01-01", "2025-01-06")
    week_spans = group_phase_days_by_week(phase)
    all_days = [day for week in week_spans for day in week.days]

    assert week_spans, "Expected at least one weekly span"
    assert all_days[0].date() == datetime.date(2025, 1, 1)
    assert all_days[-1].date() == datetime.date(2025, 1, 6)


def test_last_focus_block_uses_torii_emoji():
    phase = make_phase("Final Block", "2025-01-02", "2025-01-02", emoji="🌀")
    events = generate_focus_block_events([phase])

    final_event = sorted(events, key=lambda e: e.start)[-1]
    assert final_event.emoji == "⛩️", f"Expected ⛩️, found {final_event.emoji}"


def test_focus_block_day_ends_with_torii_emoji():
    phase = make_phase("Torii Check", "2025-01-01", "2025-01-01", emoji="🌀")
    events = generate_focus_block_events([phase])

    assert events, "No events generated"
    assert sorted(events, key=lambda e: e.start)[-1].emoji == "⛩️"


def test_glyph_key_event_written_for_single_day(tmp_path):
    phase = make_phase("Glyph Test Phase", "2025-01-04", "2025-01-04", emoji="🧪")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        write_focus_blocks_weekly([phase])
        expected = output_dir / "focus_blocks_glyph_test_phase_2025-W01.ics"

        if not expected.exists():
            expected = Path("output") / expected.name  # fallback

        assert expected.exists(), f"Expected .ics file not found: {expected}"

        content = expected.read_text(encoding="utf-8")
        unfolded_lines = unfold_ics_lines(content)
        glyph_lines = [
            line for line in unfolded_lines
            if "SUMMARY:" in line.upper() and "GLYPH KEY" in line.upper()
        ]
        print("=== All Unfolded ICS Lines ===")
        for line in unfolded_lines:
            print(repr(line))
        print("=== Unfolded SUMMARY lines ===")
        for line in unfolded_lines:
            if "SUMMARY:" in line:
                print(repr(line))
        assert len(glyph_lines) == 1, f"Expected 1 Glyph Key entry, found {len(glyph_lines)}"
        assert any("GLYPH KEY" in line.upper() for line in glyph_lines), "Missing Glyph Key in SUMMARY line"

    finally:
        os.chdir(original_cwd)
