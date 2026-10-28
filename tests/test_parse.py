import os
import sys
import unittest
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import peps_piscine as pp  # noqa: E402


class Args:
    file = os.path.join(HERE, "fixture_page.txt")


class TestParse(unittest.TestCase):
    def setUp(self):
        self.events = pp.parse(pp.get_text(Args()), date(2026, 10, 1))

    def test_counts(self):
        kinds = [e["kind"] for e in self.events]
        self.assertEqual(kinds.count("longueurs"), 4)
        self.assertEqual(kinds.count("tous"), 1)

    def test_first_event(self):
        e = self.events[0]
        self.assertEqual(e["day"], date(2026, 10, 4))
        self.assertEqual(e["start"], (8, 0))
        self.assertEqual(e["end"], (16, 0))
        self.assertEqual(e["info"], ["Piscine olympique"])
        self.assertEqual(e["config"], ["25m", "Eau profonde uniquement"])

    def test_note(self):
        e = self.events[2]
        self.assertIn("peu profond", e["note"][0])
        self.assertEqual(e["config"][0], "21m")

    def test_year_rollover(self):
        self.assertEqual(pp.guess_year(1, date(2026, 12, 15)), 2027)
        self.assertEqual(pp.guess_year(12, date(2027, 1, 5)), 2026)
        self.assertEqual(pp.guess_year(10, date(2026, 10, 1)), 2026)


class TestIcs(unittest.TestCase):
    def setUp(self):
        events = pp.parse(pp.get_text(Args()), date(2026, 10, 1))
        self.ics = pp.to_ics(events)
        self.ics_again = pp.to_ics(events)

    def test_structure(self):
        self.assertTrue(self.ics.startswith("BEGIN:VCALENDAR\r\n"))
        self.assertTrue(self.ics.endswith("END:VCALENDAR\r\n"))
        self.assertEqual(self.ics.count("BEGIN:VEVENT"), 5)

    def test_line_length(self):
        for line in self.ics.split("\r\n"):
            self.assertLessEqual(len(line.encode("utf-8")), 75)

    def test_uid_stable(self):
        uids = [l for l in self.ics.split("\r\n") if l.startswith("UID:")]
        uids2 = [l for l in self.ics_again.split("\r\n") if l.startswith("UID:")]
        self.assertEqual(uids, uids2)
        self.assertEqual(len(set(uids)), len(uids))


if __name__ == "__main__":
    unittest.main()
