import os
import sys
import tempfile

import pytest
from gpxpy.gpx import GPXTrackPoint, GPXTrack, GPX, GPXTrackSegment

from linesman import get_evaluation_measure
from linesman.geo import dist_m
from linesman.geometry import Vector


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
    refline = '1,1;3,2'
    sys.argv = ['linesman', gpx_file, 'MAX', '--line', refline]
    m = get_evaluation_measure()
    assert abs(m.calculate()/49695.425252590474 - 1) < 0.001


def test_invalid_gpx_file(gpx_obj):
    segment = gpx_obj.tracks[0].segments[0]
    segment.points.append(GPXTrackPoint(1, 1))
    f = tempfile.NamedTemporaryFile('w', encoding='utf-8', delete=False)
    f.write(gpx_obj.to_xml())
    f.close()

    sys.argv = ['linesman', f.name, 'MAX']
    with pytest.raises(SystemExit):
        get_evaluation_measure()
    os.remove(f.name)


def test_warn_multiple_tracks(capsys):
    gpx = GPX()
    track1 = GPXTrack()  # the first track needs at least 2 points to be valid
    segment = GPXTrackSegment()
    segment.points.append(GPXTrackPoint(1, 1))
    segment.points.append(GPXTrackPoint(2, 1))
    track1.segments.append(segment)
    track2 = GPXTrack()
    gpx.tracks.append(track1)
    gpx.tracks.append(track2)
    f = tempfile.NamedTemporaryFile('w', encoding='utf-8', delete=False)
    f.write(gpx.to_xml())
    f.close()

    sys.argv = ['linesman', f.name, 'MAX']
    m = get_evaluation_measure()
    output = capsys.readouterr()
    assert 'Warning' in output.out
    assert 'multiple tracks, defaulting to first one' in output.out

    os.remove(f.name)


def test_measures(gpx_file):
    # the maximum deviation is just from the (2, 1) point, which can be
    # approximated with planar lon/lat geometry (we are close to the equator)
    deviation = dist_m(Vector(1.5, 1.5), Vector(2, 1))
    MAX_REL_DIFF = 0.001

    sys.argv = ['linesman', gpx_file, 'MAX']
    m = get_evaluation_measure()
    assert abs(m.calculate()/deviation - 1) < MAX_REL_DIFF

    sys.argv = ['linesman', gpx_file, 'AVG']
    m = get_evaluation_measure()
    assert abs(m.calculate()/(deviation/3) - 1) < MAX_REL_DIFF

    sys.argv = ['linesman', gpx_file, 'SQ-AVG']
    m = get_evaluation_measure()
    assert abs(m.calculate()/(deviation**2/3) - 1) < MAX_REL_DIFF
