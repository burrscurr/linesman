# linesman
[![coverage](https://codecov.io/gh/burrscurr/linesman/branch/master/graph/badge.svg?token=LTDZFKEX4N)](https://codecov.io/gh/burrscurr/linesman)

`linesman` is a small python command line tool calculating quality measures for
the straightness of a gpx track. The project is inspired by the "I attempted to
cross \<country\> in a completely straight line" series of youtuber
[GeoWizard](https://www.youtube.com/channel/UCW5OrUZ4SeUYkUg1XqcjFYA).

## Installation

As a [python](https://python.org) package, `linesman` is installed [with
pip](https://datatofish.com/install-package-python-using-pip/). The
package is named `gpx-linesman`:

```
pip install gpx-linesman
```

After installing the package, you should be able to run linesman:

```
linesman --help
```

## Usage

`linesman` must be passed a gpx file with the recorded track, it should compare
to a reference line:

```
linesman path/to/file.gpx
```

By default, the first and last point in the gpx file are used to derive the
straight reference line from. If you want to specify the reference line
explicitly, use the `--line` flag.

Currently, three line quality measures are implemented: `max_m` (maximum
deviation to the straight line in meters), `avg_m` (average deviation to the
straight line in meters) and `avg_sq_m` (average squared deviation). By default,
the maximum deviation is being calculated. Different quality measures can be
calculated with the `--using` flag:

```
linesman <file.gpx> --using avg_m
```

## Development

Python dependencies are managed with poetry and can be installed from
`poetry.lock` by running:

```
poetry install
```

Then, the CLI tool can be started with `poetry run linesman`. Run tests with
`poetry run pytest`. Pass `--cov` flag to pytest to get a test coverage report.

