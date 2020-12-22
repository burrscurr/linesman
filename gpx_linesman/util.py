

def lonlat_str(string):
    """:return: tuple of floats"""
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
    return lon, lat


def project(line_a, line_b, point):
    """:return: project a point on a line"""
    # move the points such that line_a is (0, 0)
    ax, ay = line_a
    bx, by = line_b
    bx = bx - ax
    by = by - ay
    px, py = point
    px = px - ax
    py = py - ay

    # moved projection point is ((px; py) * (bx; by)) / ((bx; by) * (bx; by)) * (bx; by)
    factor = (px*bx + py*by)/(bx*bx + by*by)
    return (factor*bx + ax, factor*by + ay)

