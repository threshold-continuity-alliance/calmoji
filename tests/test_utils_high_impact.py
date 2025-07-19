# tests/test_utils_high_impact.py

import unittest
from datetime import datetime, timedelta
from calmoji.utils import format_datetime, fold_ics_line
from calmoji.ics_writer import create_ics_header
from calmoji.focus_blocks_writer import group_phase_days_by_week
from calmoji.types import Phase


class TestUtilsHighImpact(unittest.TestCase):

    def test_create_ics_header_format(self):
        header = create_ics_header("test comment")
        self.assertTrue(header.startswith("BEGIN:VCALENDAR"))
        self.assertIn("X-WR-CALNAME", header)
        self.assertIn("PRODID", header)
        self.assertTrue("test comment" in header or "X-COMMENT" in header)

    def test_group_phase_days_by_week_cross_year(self):
        # Dec 30, 2024 (Monday) to Jan 5, 2025 (Sunday)
        # This is *all* ISO week 1 of 2025
        phase = Phase(
            name="Cross-Year",
            start=datetime(2024, 12, 30),
            end=datetime(2025, 1, 5),
            start_offset=0,
            end_offset=0,
            emoji="🌀"
        )
        grouped_weeks = group_phase_days_by_week(phase)
        self.assertEqual(len(grouped_weeks), 1)  # All in ISO week 1
        for span in grouped_weeks:
            self.assertTrue(hasattr(span, 'days'))
            self.assertIsInstance(span.days, list)

    def test_format_datetime_line_folding(self):
        dt = datetime(2025, 1, 1, 12, 0)
        long_prop = f"DTSTART:{format_datetime(dt)}" + "A" * 100
        folded = fold_ics_line(long_prop)
        self.assertTrue("\n" in folded or len(folded) > 75)


if __name__ == '__main__':
    unittest.main()
