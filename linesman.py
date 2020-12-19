import argparse

import gpxpy
from geopy.distance import geodesic, lonlat


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


def project(line_a, line_b, point):
    """:return: project a point on a line"""
    # move the points such that line_a is (0, 0)
    ax, ay = line_a
    bx, by = line_b
    bx = bx - ax
    by = by - ay
    px, py = point
    px = px - ax
    py = py - ay

    # moved projection point is ((px; py) * (bx; by)) / ((bx; by) * (bx; by)) * (bx; by)
    factor = (px*bx + py*by)/(bx*bx + by*by)
    return (factor*bx + ax, factor*by + ay)


class ScoringMethod:
    """Abstract base class for a straight line mission scoring method."""
    def __init__(self, gpxfile, line_start, line_end):
        """
        :param gpxfile: gpx file
        :param line_start: (lon, lat) tuple marking the line start point
        :param line_end: (lon, lat) tuple marking the line end point
        """
        self.measures = []
        self.gpx = gpxpy.parse(gpxfile)

        # calculate the deviation measures for each point
        track = self.gpx.tracks[0]
        if len(self.gpx.tracks) > 1:
            print('WARNING: gpx file has multiple tracks, defaulting to using first one.')
        for track in self.gpx.tracks:
            for segment in track.segments:
                for actual in segment.points:
                    actual_point = (actual.longitude, actual.latitude)
                    self.measures.append(
                        self.measure_deviation(
                            project(line_start, line_end, actual_point),
                            actual_point
                        )
                    )

    def measure_deviation(self, point, actual):
        """:return: deviation of a point on the line to an gps point"""
        raise NotImplementedError()

    def aggregate(self):
        """
        :return: aggregation of all deviations (e.g. the maximum or an average)
        """
        raise NotImplementedError()


class MeterDeviation(ScoringMethod):
    """
    Scoring method using the deviation of points from the line in meters as
    critical measure.
    """
    def measure_deviation(self, point, actual):
        point = lonlat(*point)
        actual = lonlat(*actual)
        return 1000*geodesic(point, actual).km


class MaxDeviation(MeterDeviation):
    """Maximum deviation from the line in meters."""
    def aggregate(self):
        return max(self.measures)



class AvgDeviation(MeterDeviation):
    """Average deviation from the line in meters."""
    def aggregate(self):
        return sum(self.measures)/len(self.measures)


class AvgSquareDeviation(MeterDeviation):
    """
    Average squared deviation from the line in meters^2.
    This measure punishes bigger deviations more than small ones.
    """
    def aggregate(self):
        return sum(map(lambda x: x**2, self.measures))/len(self.measures)


if __name__ == '__main__':
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

