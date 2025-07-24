# tests/test_focus_blocks.py


from datetime import datetime, timedelta, timezone
from calmoji.types import PhaseWeekSpan


def test_generate_focus_block_events_and_glyph_key():
    start = datetime(2039, 1, 2, tzinfo=timezone.utc)
    days = [start + timedelta(days=i) for i in range(7)]
    end = days[-1]
    span = PhaseWeekSpan(start=start, end=end, days=days)

    events = span.generate_focus_block_events(label="Deep Focus", emoji="🔥")
    assert len(events) == 21
    assert all(e.summary.startswith("Deep Work") for e in events)

    glyph = span.generate_focus_block_glyph_key_event(label="Deep Focus", emoji="🔥")
    assert glyph.summary.endswith("glyph key for 2039-W01")
    assert glyph.start.hour == 3

    all_events = span.generate_all_focus_block_events(label="Deep Focus", emoji="🔥")
    assert len(all_events) == 22
    assert all_events[-1].summary == glyph.summary
