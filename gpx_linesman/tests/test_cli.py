import pytest

from ..cli import lonlat_str


def test_lonlat_str_no_comma():
    with pytest.raises(ValueError, match=".* must be 'lon,lat'.*"):
        lonlat_str('nocomma')


def test_lonlat_str_no_float():
    with pytest.raises(ValueError, match="lon .*? is no valid floating point number.*"):
        lonlat_str('5x,48.000945')
    with pytest.raises(ValueError, match="lat .*? is no valid floating point number.*"):
        lonlat_str('48.000945,any')

