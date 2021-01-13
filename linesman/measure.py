
from geopy.distance import geodesic, lonlat

from .util import Vector, Line



class Measure:
    """Abstract base class evaluating a sequence of points to a straight line."""
    desc = None  # description of the value aggregated by this measure

    def __init__(self, points: [Vector], refline: Line):
        """
        :param points: list of Vector(lon,lat) instances representing the gps track
        :param refline: line to compare the points to
        """
        # measure the deviation of each point to its projection onto the
        # straight line
        self.measures = [
            self.measure_deviation(refline.project(point), point)
                for point in points
        ]

    def measure_deviation(self, point: Vector, actual: Vector):
        """:return: deviation of a point on the line to an gps point"""
        raise NotImplementedError()

    def aggregate(self):
        """
        :return: aggregation of all deviations (e.g. the maximum or an average)
        """
        raise NotImplementedError()


class MeterDeviation(Measure):
    """
    Scoring method using the deviation of points from the line in meters as
    critical measure.
    """
    def measure_deviation(self, point, actual):
        point = lonlat(point.x, point.y)
        actual = lonlat(actual.x, actual.y)
        return 1000*geodesic(point, actual).km


class MaxDeviation(MeterDeviation):
    """Maximum deviation from the line in meters."""
    desc = 'Maximum deviation in meters'

    def aggregate(self):
        return max(self.measures)



class AvgDeviation(MeterDeviation):
    """Average deviation from the line in meters."""
    desc = 'Average deviation in meters'

    def aggregate(self):
        return sum(self.measures)/len(self.measures)


class SquareDeviationAvg(MeterDeviation):
    """
    Average squared deviation from the line in meters^2.
    This measure punishes bigger deviations more than small ones.
    """
    desc = 'Average squared deviation'

    def aggregate(self):
        return sum(map(lambda x: x**2, self.measures))/len(self.measures)
