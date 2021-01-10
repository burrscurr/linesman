import argparse

from .parse import lonlat_pair_str, gpx_file, gpx_extract_points
from .measure import MaxDeviation, AvgDeviation, SquareDeviationAvg


available_measures = {
    'MAX': MaxDeviation,
    'AVG': AvgDeviation,
    'SQ-AVG': SquareDeviationAvg
}


def info(msg):
    print('INFO : ' + msg, file=sys.stdout)


def abort(msg):
    print('ERROR: ' + msg, file=sys.stderr)
    raise SystemExit(1)


def _argparser():
    """:return: argument parser defining the command line interface"""
    parser = argparse.ArgumentParser(
        description='Measure the deviation of a ' \
                    'gpx track from a completely straight line.'
    )
    parser.add_argument(
        'gpxfile', type=gpx_file,
        help='gpx file containing a GPS record to be compared to a straight line'
    )
    parser.add_argument(
        'measure', choices=available_measures.keys(),
        help="Quality measure to use. Available are maximum deviation in meters " \
             "('MAX'), average deviation in meters ('AVG') and squared average " \
             "deviation ('SQ-AVG')."
    )
    parser.add_argument(
        '--line', type=lonlat_pair_str,
        help="Two points defining the reference line in format 'lon,lat;lon,lat'. " \
            "Default: Line defined by first and last point of the gpx track."
    )
    return parser


def run():
    parser = _argparser()
    args = parser.parse_args()

    Measure = available_measures[args.measure]
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

    m = Measure(points, point_a, point_b)
    print(f'{m.desc}: {m.aggregate()}')
