import contextlib
import io
import unittest
from pathlib import Path
from uuid import uuid4

from swiftserve_summary.cli import main, summarize


class SummaryTests(unittest.TestCase):
    def write_csv(self, text):
        path = Path(__file__).parent / f"temp-{uuid4().hex}.csv"
        self.addCleanup(path.unlink, missing_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_counts_statuses(self):
        path = self.write_csv("trip_id,status\n1,completed\n2,Cancelled\n3,completed\n")
        count, statuses = summarize(path)
        self.assertEqual(count, 3)
        self.assertEqual(statuses, {"completed": 2, "Cancelled": 1})

    def test_accepts_trip_status_header_with_spaces_and_bom(self):
        path = self.write_csv("\ufefftrip_id, Trip_Status \n1,completed\n")
        self.assertEqual(summarize(path)[0], 1)

    def test_empty_file_has_clear_error(self):
        path = self.write_csv("")
        with self.assertRaisesRegex(ValueError, "empty"):
            summarize(path)

    def test_missing_status_header_has_clear_error(self):
        path = self.write_csv("trip_id,driver\n1,Ada\n")
        with self.assertRaisesRegex(ValueError, "status"):
            summarize(path)

    def test_blank_status_is_rejected(self):
        path = self.write_csv("trip_id,status\n1,  \n")
        with self.assertRaisesRegex(ValueError, "blank trip status"):
            summarize(path)

    def test_short_row_is_rejected(self):
        path = self.write_csv("trip_id,status\n1\n")
        with self.assertRaisesRegex(ValueError, "missing a value"):
            summarize(path)

    def test_long_row_is_rejected(self):
        path = self.write_csv("trip_id,status\n1,completed,extra\n")
        with self.assertRaisesRegex(ValueError, "more values"):
            summarize(path)

    def test_missing_file_gets_friendly_message_and_exit_code(self):
        errors = io.StringIO()
        with contextlib.redirect_stderr(errors):
            result = main(["no-such-trips.csv"])
        self.assertEqual(result, 2)
        self.assertIn("cannot read", errors.getvalue())

    def test_help_is_available(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), self.assertRaises(SystemExit) as raised:
            main(["--help"])
        self.assertEqual(raised.exception.code, 0)
        self.assertIn("status column", output.getvalue())


if __name__ == "__main__":
    unittest.main()
