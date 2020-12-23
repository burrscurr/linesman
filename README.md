# linesman

`linesman` is a small python command line tool calculating quality measures for the
straightness of a gpx track. The project is inspired by the "I attempted to
cross \<country\> in a completely straight line" series by the youtuber
[GeoWizard](https://www.youtube.com/channel/UCW5OrUZ4SeUYkUg1XqcjFYA).

## Installation

As a python package, `linesman` is installed via pip (the package is named
`gpx-linesman`):

```
pip install gpx-linesman
```

After installing the package, you should be able to run linesman:

```
linesman --help
```

## Usage

Currently, three deviation measures are implemented: `max_m` (maximum deviation
to the straight line in meters), `avg_m` (average deviation to the straight line
in meters) and `avg_sq_m` (average squared deviation).

Without special arguments, the maximum deviation is being calculated:

```
linesman <file.gpx> <lon_start,lat_start> <lon_end,lat_end>
```

Calculating the average deviation:

```
linesman <file.gpx> <lon_start,lat_start> <lon_end,lat_end> --using avg_m
```

For an example gpx file, see [`examples/simple.gpx`](examples/simple.gpx).

## Development

Python dependencies are managed with poetry and can be installed from
`poetry.lock` by running:

```
poetry install
```

Then, the CLI tool can be started with `poetry run linesman`.

