# linesman
[![test coverage](https://coveralls.io/repos/github/burrscurr/linesman/badge.svg)](https://coveralls.io/github/burrscurr/linesman)
[![Documentation Status](https://readthedocs.org/projects/linesman/badge/?version=latest)](https://linesman.readthedocs.io/en/latest/?badge=latest)

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

`linesman` must be passed a gpx file with the recorded track and a quality
measure that shall be used to compare the gpx track against the reference line:

```
linesman path/to/file.gpx <measure>
```

Currently, the following quality measures are implemented:

 - `MAX`: maximum deviation from the reference line in meters
 - `AVG`: average deviation in meters
 - `SQ-AVG`: squared deviation average in meters

## Development

Python dependencies are managed with poetry and can be installed from
`poetry.lock` by running:

```
poetry install
```

Then, the CLI tool can be started with `poetry run linesman`. Run tests with
`poetry run pytest`.

## Documentation

Conceptual documentation can be found on [readthedocs](https://linesman.readthedocs.io).
