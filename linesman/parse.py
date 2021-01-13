import argparse

import gpxpy

from .util import Vector, Line


def lonlat_str(string):
    """:return: Vector(lon, lat) point"""
    if ',' not in string:
        raise ValueError("Format must be 'lon,lat' (missing ',')!")
    lon, lat = string.split(',', maxsplit=1)
    try:
        lon = float(lon)
    except ValueError as e:
        raise ValueError(f"lon '{lon}' is no valid floating point number.")
    try:
        lat = float(lat)
    except ValueError as e:
        raise ValueError(f"lat '{lat}' is no valid floating point number.")
    return Vector(lon, lat)


def lonlat_pair_str(string):
    """:return: Line instance"""
    if ';' not in string:
        raise ValueError("Format for line must be 'start;end' (missing ';')!")

    start, end = string.split(';', maxsplit=1)
    return Line(lonlat_str(start), lonlat_str(end))


def gpx_file(path):
    """:return: contents of gpx file parsed with gpxpy"""
    file_tester = argparse.FileType('r')
    gpxfile = file_tester(path)
    return gpxpy.parse(gpxfile)


def gpx_extract_points(gpx_obj):
    """
    Extract the points of the first track of a gpx file.
    :return: list of lon,lat-Vector instances
    """
    tracks = len(gpx_obj.tracks)
    if tracks < 1:
        raise ValueError('The gpx file must contain at least one track!')
    elif tracks > 1:
        info('gpx file has multiple tracks, defaulting to first one.')

    points = []
    track = gpx_obj.tracks[0]
    for segment in track.segments:
        for actual in segment.points:
            points.append(Vector(actual.longitude, actual.latitude))

    if len(points) < 2:
        msg = 'gpx file must have at least two points in the selected track!'
        raise ValueError(msg)

    return points
