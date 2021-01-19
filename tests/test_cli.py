import sys
import tempfile
import os

import pytest
from gpxpy.gpx import GPXTrackPoint

from linesman import run, get_evaluation_measure


@pytest.fixture
def gpx_file(gpx_obj):
    segment = gpx_obj.tracks[0].segments[0]
    segment.points.append(GPXTrackPoint(1, 1))
    segment.points.append(GPXTrackPoint(2, 1))
    segment.points.append(GPXTrackPoint(2, 2))

    f = tempfile.NamedTemporaryFile('w', encoding='utf-8', delete=False)
    f.write(gpx_obj.to_xml())
    f.close()

    yield f.name
    os.remove(f.name)


def test_implicit_refline(gpx_file):
    sys.argv = ['linesman', gpx_file, 'MAX']
    m_implicit = get_evaluation_measure()
    refline = '1,1;2,2'
    sys.argv = ['linesman', gpx_file, 'MAX', '--line', refline]
    m_explicit = get_evaluation_measure()

    assert m_explicit.calculate() == m_implicit.calculate()


def test_implicit_line_invalid(gpx_obj):
    segment = gpx_obj.tracks[0].segments[0]
    segment.points.append(GPXTrackPoint(1, 1))
    segment.points.append(GPXTrackPoint(1, 1))
    f = tempfile.NamedTemporaryFile('w', encoding='utf-8', delete=False)
    f.write(gpx_obj.to_xml())
    f.close()

    # A line must be defined by at least 2 points
    sys.argv = ['linesman', f.name, 'MAX']
    with pytest.raises(SystemExit):
        m = get_evaluation_measure()
    os.remove(f.name)


def test_explicit_line(gpx_file):
    refline = '1,1;2,3'
    sys.argv = ['linesman', gpx_file, 'MAX', '--line', refline]
    m = get_evaluation_measure()
    assert m.calculate() == 49695.425252590474


def test_invalid_gpx_file(gpx_obj):
    segment = gpx_obj.tracks[0].segments[0]
    segment.points.append(GPXTrackPoint(1, 1))
    f = tempfile.NamedTemporaryFile('w', encoding='utf-8', delete=False)
    f.write(gpx_obj.to_xml())
    f.close()

    sys.argv = ['linesman', f.name, 'MAX']
    with pytest.raises(SystemExit):
        m = get_evaluation_measure()
    os.remove(f.name)


def test_max_deviation(gpx_file):
    sys.argv = ['linesman', gpx_file, 'MAX']
    m = get_evaluation_measure()
    assert m.calculate() == 78433.68568649939


def test_avg_deviation(gpx_file):
    sys.argv = ['linesman', gpx_file, 'AVG']
    m = get_evaluation_measure()
    assert m.calculate() == 26144.561895499795


def test_sq_avg_deviation(gpx_file):
    sys.argv = ['linesman', gpx_file, 'SQ-AVG']
    m = get_evaluation_measure()
    assert m.calculate() == 2050614350.1228597
