import argparse

from .geometry import Line
from .measure import MaxDeviation, AvgDeviation, SquareDeviationAvg
from .output import abort
from .parse import latlon_pair_str, gpx_file, gpx_extract_points

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


def _argparser():
    """:return: argument parser defining the command line interface"""
    parser = argparse.ArgumentParser(
        description='Measure the deviation of a '
                    'gpx track from a completely straight line.'
    )
    parser.add_argument(
        'gpxfile', type=gpx_file,
        help='gpx file containing a GPS record to be compared to a straight line'
    )
    parser.add_argument(
        'measure', choices=available_measures.keys(),
        help="Quality measure to use. Available are maximum deviation in meters "
             "('MAX'), average deviation in meters ('AVG') and squared average "
             "deviation ('SQ-AVG')."
    )
    parser.add_argument(
        '--line', type=latlon_pair_str,
        help="Two points defining the reference line in format 'lat,lon;lat,lon'. "
             "Default: Line defined by first and last point of the gpx track."
    )
    parser.add_argument(
        '-V', '--version', action='version', version=__version__,
        help='Print linesman version and exit.'
    )
    return parser


def get_evaluation_measure():
    """
    :return: Measure instance configured according to the command line
    parameters
    """
    parser = _argparser()
    args = parser.parse_args()

    Measure = available_measures[args.measure]
    try:
        points = gpx_extract_points(args.gpxfile)
    except ValueError as e:
        abort(str(e))

    # if not explicitly given, let first/last point define the reference line
    if not args.line:
        try:
            args.line = Line(points[0], points[-1])
        except ValueError as e:  # may happen if both points are equal
            abort(str(e))
    return Measure(points, args.line, resample=False)


def run():
    m = get_evaluation_measure()
    print(f'{m.desc}: {m.calculate()}')
