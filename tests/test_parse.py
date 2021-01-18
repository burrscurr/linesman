import pytest
import argparse
import tempfile
import uuid
import os

from gpxpy.gpx import GPX, GPXTrackPoint, GPXXMLSyntaxException

from linesman.parse import lonlat_str, lonlat_pair_str, gpx_file, gpx_extract_points


@pytest.fixture
def temp_file_path():
    path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
    with open(path, 'a'):
        pass
    yield path
    os.remove(path)


def test_lonlat_str_no_comma():
    with pytest.raises(ValueError, match=".* must be 'lon,lat'.*"):
        lonlat_str('nocomma')


def test_lonlat_str_no_float():
    with pytest.raises(ValueError, match="lon .*? is no valid floating point number.*"):
        lonlat_str('5x,48.000945')
    with pytest.raises(ValueError, match="lat .*? is no valid floating point number.*"):
        lonlat_str('48.000945,any')


def test_lonlat_str():
    assert lonlat_str('5.2,4.3') == (5.2, 4.3)


def test_lonlat_pair_str_no_semicolon():
    with pytest.raises(ValueError, match="Format for line must be .*"):
        lonlat_pair_str('no-semicolon')


def test_lonlat_pair_str():
    assert lonlat_pair_str('1.2,-80;58.3,10.3') == ((1.2, -80), (58.3, 10.3))


def test_gpx_file_no_readable_file():
    with pytest.raises(argparse.ArgumentTypeError):
        gpx_file('no readable gpx file')


def test_gpx_file_invalid_gpx_syntax(temp_file_path):
    with pytest.raises(GPXXMLSyntaxException):
        gpx_file(temp_file_path)


def test_gpx_extract_points_no_tracks():
    gpx = GPX()
    with pytest.raises(ValueError, match='.*?at least one track.*'):
        gpx_extract_points(gpx)


def test_gpx_extract_points_to_few(gpx_obj):
    segment = gpx_obj.tracks[0].segments[0]
    segment.points.append(GPXTrackPoint(1, 1))

    with pytest.raises(ValueError, match='.*?at least two points.*'):
        points = gpx_extract_points(gpx_obj)


def test_gpx_extract_points(gpx_obj):
    segment = gpx_obj.tracks[0].segments[0]
    segment.points.append(GPXTrackPoint(1, 1))
    segment.points.append(GPXTrackPoint(2, 1))
    segment.points.append(GPXTrackPoint(2, 2))

    points = gpx_extract_points(gpx_obj)
    assert points == [(1, 1), (1, 2), (2, 2)]
