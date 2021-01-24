from .geo import mercator_project, azimuth
from .geometry import Vector, Line


class Measure:
    """
    Abstract base class for measuring a sequence of points to a reference line.
    """
    desc = None  # description of the value aggregated by this measure

    def __init__(self, points: [Vector], refline: Line, resample=True):
        """
        :param points: list of Vector(lon,lat) instances representing the gps
        track
        :param refline: line to compare the points to
        :param resample: Whether to resample the recorded track from equidistant
        points on the reference line (default). If False, the recorded track
        points are compared to their projections on the reference line.
        """
        self.resample = resample

        self.points = list(self._to_meter_grid(points, refline))

    def _to_meter_grid(self, points: [Vector], refline: Line):
        """
        Transform the given (lon, lat) points such that the reference line is
        on the x axis and the y coordinate of a point being its shortest
        distance from the reference line. The unit of the resulting cartesian
        grid is 1 Meter.
        After this transformation, each point's deviation is its y coordinate.
        :param points: iterable of (lon, lat) Vector instances to transform
        :param refline: Line instance that becomes the new x axis
        :return: iterable of transformed points
        """
        start = refline.point(0)
        end = refline.point(1)
        return mercator_project(start, azimuth(start, end), points)

    def calculate(self):
        """
        :return: result of the measure (e.g. maximum or an average)
        """
        raise NotImplementedError()


class AbsoluteDeviationMeasure(Measure):
    """Deviation measure considering the absolute deviation."""
    def _absolute_deviations(self):
        return [abs(p.y) for p in self.points]


class MaxDeviation(AbsoluteDeviationMeasure):
    """Maximum deviation from the line in meters."""
    desc = 'Maximum deviation in meters'

    def calculate(self):
        return max(self._absolute_deviations())


class AvgDeviation(AbsoluteDeviationMeasure):
    """Average deviation from the line in meters."""
    desc = 'Average deviation in meters'

    def calculate(self):
        return sum(self._absolute_deviations())/len(self.points)


class SquareDeviationAvg(Measure):
    """
    Average squared deviation from the line in meters^2.
    This measure punishes bigger distances more than small ones.
    """
    desc = 'Average squared deviation'

    def calculate(self):
        return sum([p.y**2 for p in self.points])/len(self.points)
