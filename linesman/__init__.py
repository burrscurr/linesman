import argparse

from .parse import lonlat_pair_str, gpx_file, gpx_extract_points
from .measure import MaxDeviation, AvgDeviation, SquareDeviationAvg
from .util import Line


try:                         # python ^3.8
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # python <3.8
    import importlib_metadata

__version__ = importlib_metadata.version('gpx-linesman')


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
    parser.add_argument(
        '-V', '--version', action='version', version=__version__,
        help='Print linesman version and exit.'
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
    if not args.line:
        try:
            args.line = Line(points[0], points[-1])
        except ValueError as e:
            abort(str(e))

    m = Measure(points, args.line, resample=False, spherical=False)
    print(f'{m.desc}: {m.aggregate()}')
