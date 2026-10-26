# SwiftServe Trip Summary

`swiftserve-summary` is a small command-line helper for the SwiftServe pilot. Give it a CSV trip export and it reports the number of trips and the count for each status. It uses Python's built-in CSV reader and does not need extra runtime packages.

## Install and run

You need Python 3.9 or newer and Git. From a terminal, run these two commands:

```sh
python -m pip install "git+https://github.com/abdulwaheedmuhammed3-maker/task-2.git#subdirectory=swiftserve-trip-summary"
swiftserve-summary examples/trips.csv
```

The first command installs the tool from this folder in the public repository. If you are running the example from another directory, replace `examples/trips.csv` with the path to your own file.

## Example

```text
$ swiftserve-summary examples/trips.csv
Trips reviewed: 4
Trips by status:
  cancelled: 1
  completed: 2
  waiting: 1
```

The CSV needs a header called `status` or `trip_status` (capitalization and surrounding spaces do not matter). Each trip row needs a non-empty status. The tool points to the row when a line is malformed, and exits with a helpful message if a file cannot be read.

Use `swiftserve-summary --help` to see the command options. To run the tests from this folder:

```sh
python -m unittest discover -s tests -v
```

## A change I made after testing awkward input

At first I planned to treat an empty status as just another status in the report. Testing a short row and a row with spaces showed that this would hide incomplete trip records. The tool now stops at the row and explains what needs fixing, so the SwiftServe team can correct the export before using the totals.
