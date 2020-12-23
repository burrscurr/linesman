import pytest

from ..util import lonlat_str, project


def test_lonlat_str_no_comma():
    with pytest.raises(ValueError, match=".* must be 'lon,lat'.*"):
        lonlat_str('nocomma')


def test_lonlat_str_no_float():
    with pytest.raises(ValueError, match="lon .*? is no valid floating point number.*"):
        lonlat_str('5x,48.000945')
    with pytest.raises(ValueError, match="lat .*? is no valid floating point number.*"):
        lonlat_str('48.000945,any')


def test_project_point_on_line():
    x, y = project((0, 0), (3, 3), (1, 1))
    assert x == 1
    assert y == 1


def test_project_within_line_points():
    x, y = project((0, 0), (3, 3), (0, 2))
    assert x == 1
    assert y == 1


def test_project_outside_line_points():
    x, y = project((0, 0), (3, 3), (-2, 0))
    assert x == -1
    assert y == -1


def test_project_non_origin_line():
    x, y = project((0, 1), (2, 2), (3, 0))
    assert x == 2
    assert y == 2

