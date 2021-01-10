import sys
import tempfile
import os

import pytest
from gpxpy.gpx import GPXTrackPoint

from linesman import run


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


def test_cli_max_deviation(gpx_file, capsys):
    sys.argv = ['linesman', gpx_file, 'MAX']
    run()
    stdout, _ = capsys.readouterr()
    assert stdout.endswith('78433.68568649939\n')


def test_cli_avg_deviation(gpx_file, capsys):
    sys.argv = ['linesman', gpx_file, 'AVG']
    run()
    stdout, _ = capsys.readouterr()
    assert stdout.endswith('26144.561895499795\n')


def test_cli_sq_avg_deviation(gpx_file, capsys):
    sys.argv = ['linesman', gpx_file, 'SQ-AVG']
    run()
    stdout, _ = capsys.readouterr()
    assert stdout.endswith('2050614350.1228597\n')
