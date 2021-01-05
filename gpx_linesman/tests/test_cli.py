import pytest

from ..cli import lonlat_str, lonlat_pair_str


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


def test_lonlat_pair_str():
    with pytest.raises(ValueError, match="Format for line must be .*"):
        lonlat_pair_str('no-semicolon')


def test_lonlat_pair_str():
    assert lonlat_pair_str('1.2,-80;58.3,10.3') == ((1.2, -80), (58.3, 10.3))
