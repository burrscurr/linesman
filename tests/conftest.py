import pytest

from gpxpy.gpx import GPX, GPXTrack, GPXTrackSegment


@pytest.fixture
def gpx_obj():
    gpx = GPX()
    track = GPXTrack()
    gpx.tracks.append(track)
    segment = GPXTrackSegment()
    track.segments.append(segment)
    return gpx
