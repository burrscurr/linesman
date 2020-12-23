
from geopy.distance import geodesic, lonlat

from .util import project



class ScoringMethod:
    """Abstract base class evaluating a sequence of points to a straight line."""

    def __init__(self, points, line_start, line_end):
        """
        :param points: iterable of (x,y) tuples representing points
        :param line_start: (x,y) tuple marking the line start
        :param line_end: (x,y) tuple marking the line end
        """
        # measure the deviation of each point to its projection onto the
        # straight line
        self.measures = [
            self.measure_deviation(
                project(line_start, line_end, point),
                point
            ) for point in points
        ]

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

