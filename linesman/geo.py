from geographiclib.geodesic import Geodesic
from pyproj import CRS, Transformer

from .geometry import Vector, Line


def azimuth(p1: Vector, p2: Vector):
    """:return: azimuth of geodesic through p1 and p2 in p1 with WGS84"""
    res = Geodesic.WGS84.Inverse(p1.y, p1.x, p2.y, p2.x)
    return res['azi1'] 


def dist_m(a, b):
    """
    :param a: lon lat point
    :param b: lon lat point
    :return: distance between a and b in meters
    """
    res = Geodesic.WGS84.Inverse(a.y, a.x, b.y, b.x)
    return res['s12']


def mercator_project(origin: Vector, azimuth, points: [Vector], ellps='WGS84'):
    """
    Perform a oblique mercator projection of a given list of points with the
    pseudoequator defined by the given line.
    Formulas from DOI 10.3133/pp1395 p.69 (Map projections: A working manual)
    :param origin: (lon, lat) that will become (0, 0) in projection
    :param azimuth: azimuth in degrees of origin defining the direction of the
    geodesic that becomes the new equator (y=0) in projection
    :param points: iterable of (lon,lat) Vector instance
    :param ellps: proj ellipsoid identifier for ellipsoid to use as model for
    the globe. Defaults to WGS84.
    :return: iterable of (x, y) Vector instances in the coordinate system with
    unit 1 meter
    """
    base = CRS.from_user_input(4326)
    mercator = CRS(f'+proj=omerc +lonc={origin.x} +lat_0={origin.y} '
                   f'+alpha={azimuth} +gamma=0 +ellps={ellps}')
    t = Transformer.from_crs(base, mercator)

    for p in points:
        res = t.transform(p.y, p.x)
        yield Vector(res[1], res[0])
