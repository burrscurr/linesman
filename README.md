# linesman

`linesman` is a small python script calculating quality measures for the
straightness of a gpx track. The project is inspired by the "I attempted to
cross \<country\> in a completely straight line" series by the youtuber
[GeoWizard](https://www.youtube.com/channel/UCW5OrUZ4SeUYkUg1XqcjFYA).

## Requirements

`linesman` is a python script. Besides python, there are packages to install:

```
pip install geopy
pip install gpxpy
```

After installing the dependencies, you should be able to run linesman:

```
python3 linesman.py --help
```

## Usage

Currently, three deviation measures are implemented: `max_m` (maximum deviation
to the straight line in meters), `avg_m` (average deviation to the straight line
in meters) and `avg_sq_m` (average squared deviation).

Without special arguments, the maximum deviation is being calculated:

```
python3 linesman.py <file.gpx> <lon_start,lat_start> <lon_end,lat_end>
```

Calculating the average deviation:

```
python3 linesman.py <file.gpx> <lon_start,lat_start> <lon_end,lat_end> --using avg_m
```

For an example gpx file, see [`examples/simple.gpx`](examples/simple.gpx).

