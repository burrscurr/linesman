import argparse

import gpxpy

from .measure import MaxDeviation, AvgDeviation, AvgSquareDeviation


def info(msg):
    print('INFO : ' + msg, file=sys.stdout)


def abort(msg):
    print('ERROR: ' + msg, file=sys.stderr)
    raise SystemExit(1)


def lonlat_str(string):
    """:return: tuple of floats"""
    if ',' not in string:
        raise ValueError("Format must be 'lon,lat' (missing ',')!")
    lon, lat = string.split(',', maxsplit=1)
    try:
        lon = float(lon)
    except ValueError as e:
        raise ValueError(f"lon '{lon}' is no valid floating point number.")
    try:
        lat = float(lat)
    except ValueError as e:
        raise ValueError(f"lat '{lat}' is no valid floating point number.")
    return lon, lat


def lonlat_pair_str(string):
    """:return: pair of two lon,lat points"""
    if ';' not in string:
        raise ValueError("Format for line must be 'start;end' (missing ';')!")

    start, end = string.split(';', maxsplit=1)
    return lonlat_str(start), lonlat_str(end)


def gpx_file(path):
    """:return: contents of gpx file parsed with gpxpy"""
    file_tester = argparse.FileType('r')
    gpxfile = file_tester(path)
    return gpxpy.parse(gpxfile)


def gpx_extract_points(gpx_obj):
    """
    Extract the points of the first track of a gpx file.
    :return: list of 2-tuples in (lon, lat) form
    """
    tracks = len(gpx_obj.tracks)
    if tracks < 1:
        raise ValueError('The gpx file must contain at least one track!')
    elif tracks > 1:
        info('gpx file has multiple tracks, defaulting to first one.')

    points = []
    track = gpx_obj.tracks[0]
    for segment in track.segments:
        for actual in segment.points:
            points.append((actual.longitude, actual.latitude))

    if len(points) < 2:
        msg = 'gpx file must have at least two points in the selected track!'
        raise ValueError(msg)

    return points


def run():
    measures = {
        'max_m': MaxDeviation,
        'avg_m': AvgDeviation,
        'avg_sq_m': AvgSquareDeviation
    }
    msgs = {
        'max_m': 'Maximum deviation in meters: ',
        'avg_m': 'Average deviation in meters: ',
        'avg_sq_m': 'Average squared deviation: ',
    }

    parser = argparse.ArgumentParser(
        description='Measure the deviation of a gpx track from a completely straight line.'
    )
    parser.add_argument(
        '--using', '-u', default='max_m', choices=('max_m', 'avg_m', 'avg_sq_m'),
        help='Line quality measure to calculate'
    )
    parser.add_argument(
        'gpxfile', type=gpx_file,
        help='gpx file containing the GPS record that is an almost straight line'
    )
    parser.add_argument(
        '--line', type=lonlat_pair_str,
        help="Two points defining the reference line in format 'lon,lat;lon,lat'. " \
            "Default: Line defined by first and last point of the gpx track."
    )
    args = parser.parse_args()
    
    MeasureClass = measures[args.using]
    try:
        points = gpx_extract_points(args.gpxfile)
    except ValueError as e:
        abort(str(e))

    # define the reference line from the first/last point in the gpx file, if
    # not explicitly defined with --line
    if args.line:
        point_a = args.line[0]
        point_b = args.line[1]
    else:
        point_a = points[0]
        point_b = points[-1]
    if point_a == point_b:
        abort('Points defining the line must not be equal!')

    m = MeasureClass(points, point_a, point_b)
    print(msgs[args.using] + str(m.aggregate()))
