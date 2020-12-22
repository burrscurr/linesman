
import gpxpy
from geopy.distance import geodesic, lonlat

from .util import project



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

