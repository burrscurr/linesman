from geographiclib.geodesic import Geodesic

from .geometry import Vector, Line


def distance_m(a: Vector, b: Vector):
    """
    Solve the inverse problem for two points on the WGS84 ellipsoid.
    :param a: (longitude, latitude) point
    :param b: (longitude, latitude) point
    :return: distance in meters between a and b
    """
    res = Geodesic.WGS84.Inverse(
        a.y, a.x, b.y, b.x, Geodesic.DISTANCE)
    distance_m = res['s12']
    return distance_m


class Measure:
    """
    Abstract base class for measuring a sequence of points to a reference line.
    """
    desc = None  # description of the value aggregated by this measure

    def __init__(self, points: [Vector], refline: Line, resample=True,
            spherical=True):
        """
        :param points: list of Vector(lon,lat) instances representing the gps
        track
        :param refline: line to compare the points to
        :param resample: Whether to resample the recorded track from equidistant
        points on the reference line (default). If False, the recorded track
        points are compared to their projections on the reference line.
        :param spherical: Whether spherical geometry should be used. If False,
        the reference line is interpreted as a loxodrome rather than a geodesic.
        """
        self.spherical = spherical
        self.resample = resample
        self.points = self._select_points(points, refline)

        self.distances = [
            self.measure_distance(a, b) for a, b in self.points
        ]

    def _select_points(self, points, refline):
        """
        :return: the pairs of points to compare to evaluate the recorded track
        """
        if not self.resample:
            if self.spherical:
                # that's not trivial.
                raise NotImplementedError
            else:
                pairs = [(refline.project(p), p) for p in points]
        else:
            if self.spherical:
                raise NotImplementedError
            else:
                raise NotImplementedError
        return pairs

    def measure_distance(self, a: Vector, b: Vector):
        """:return: distance between two points"""
        raise NotImplementedError()

    def aggregate(self):
        """
        :return: aggregation of all distances (e.g. the maximum or an average)
        """
        raise NotImplementedError()


class MeterDeviation(Measure):
    """
    Interpret the given points as latitude/longitude in WGS84 and return their
    distance in meters.
    """
    def measure_distance(self, a, b):
        return distance_m(a, b)


class MaxDeviation(MeterDeviation):
    """Maximum deviation from the line in meters."""
    desc = 'Maximum deviation in meters'

    def aggregate(self):
        return max(self.distances)


class AvgDeviation(MeterDeviation):
    """Average deviation from the line in meters."""
    desc = 'Average deviation in meters'

    def aggregate(self):
        return sum(self.distances)/len(self.distances)


class SquareDeviationAvg(MeterDeviation):
    """
    Average squared deviation from the line in meters^2.
    This measure punishes bigger distances more than small ones.
    """
    desc = 'Average squared deviation'

    def aggregate(self):
        return sum(map(lambda x: x**2, self.distances))/len(self.distances)
