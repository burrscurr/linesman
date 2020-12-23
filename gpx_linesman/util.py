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

