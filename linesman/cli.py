import argparse

from .util import lonlat_str
from .measure import MaxDeviation, AvgDeviation, AvgSquareDeviation


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
        description='Measure the deviation of a gpx track from a completely straigt line.'
    )
    parser.add_argument(
        '--using', '-u', default='max_m', choices=('max_m', 'avg_m', 'avg_sq_m'),
        help='Line quality measure to calculate'
    )
    parser.add_argument(
        'gpxfile', type=argparse.FileType('r'),
        help='gpx file containing the GPS record that is an almost straight line'
    )
    parser.add_argument(
        'linestart', type=lonlat_str, help='Start point of the straight line'
    )
    parser.add_argument(
        'lineend', type=lonlat_str, help='End point of the straight line'
    )
    args = parser.parse_args()
    
    MeasureClass = measures[args.using]

    m = MeasureClass(args.gpxfile, args.linestart, args.lineend)
    print(msgs[args.using] + str(m.aggregate()))

