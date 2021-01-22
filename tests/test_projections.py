from geographiclib.geodesic import Geodesic

from linesman.geo import mercator_project
from linesman.geometry import Vector, Line


def test_mercator_project():
    # example taken from "Map projections: A working manual", page 276
    start = Vector(-77.7610558, 36.0)
    azimuth = 14.3394883
    points = [Vector(-76.8707953, 38.8092128)]
    u = 4414439.018098909
    v = -2356.2521612049804

    res = list(mercator_project(start, azimuth, points, ellps='clrk66'))
    assert abs(res[0].y - v) < 10e-8
