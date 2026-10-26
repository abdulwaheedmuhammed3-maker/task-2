"""Summarise the trip count and status mix in a SwiftServe CSV export."""

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


def summarize(path):
    """Return (trip_count, status_counts), validating the CSV as we read it."""
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as source:
            reader = csv.DictReader(source)
            headers = reader.fieldnames
            if not headers:
                raise ValueError("the file is empty or has no header row")

            normalized = {name.strip().lower(): name for name in headers if name}
            status_column = normalized.get("status") or normalized.get("trip_status")
            if status_column is None:
                raise ValueError("add a 'status' or 'trip_status' column to the header")

            statuses = Counter()
            trip_count = 0
            for line_number, row in enumerate(reader, start=2):
                if None in row:
                    raise ValueError(f"row {line_number} has more values than the header")
                if any(value is None for value in row.values()):
                    raise ValueError(f"row {line_number} is missing a value")
                status = (row.get(status_column) or "").strip()
                if not status:
                    raise ValueError(f"row {line_number} has a blank trip status")
                statuses[status] += 1
                trip_count += 1

            return trip_count, statuses
    except UnicodeDecodeError as error:
        raise ValueError("the file must be saved as UTF-8 text") from error
    except OSError as error:
        raise ValueError(f"cannot read '{path}': {error.strerror or error}") from error


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="swiftserve-summary",
        description="Count SwiftServe trips and show how many have each status.",
        epilog="Example: swiftserve-summary examples/trips.csv",
    )
    parser.add_argument("csv_file", type=Path, help="path to a CSV with a status column")
    args = parser.parse_args(argv)

    try:
        count, statuses = summarize(args.csv_file)
    except ValueError as error:
        print(f"swiftserve-summary: {error}", file=sys.stderr)
        return 2

    print(f"Trips reviewed: {count}")
    if not count:
        print("No trips found.")
    else:
        print("Trips by status:")
        for status, number in sorted(statuses.items(), key=lambda item: item[0].casefold()):
            print(f"  {status}: {number}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
