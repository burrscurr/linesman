from .abstract import StraightLine, Vector


class Geodesic(StraightLine):
    """Shortest connection between two points on a sphere."""
    def __init__(self, a: Vector, b: Vector):
        if a == b:
            raise ValueError('line cannot be defined by one point')
        self._p1 = a
        self._p2 = b

    def __contains__(self, other: Vector):
        """:return: whether the line contains a certain point"""
        raise NotImplementedError

    def __eq__(self, other):
        """:return: whether all points described by self are also on other"""
        if type(self) != type(other):
            return NotImplemented
        return other.point(0) in self and other.point(1) in self

    def __repr__(self):
        return f'Line({self._p1}, {self._p2})'

    def point(self, factor=0):
        """
        :return: point on the line based on the first initialization point added
        to the factor-th of the direction of the line.
        """
        raise NotImplementedError

    def project(self, point: Vector):
        """:return: projection of given point onto the line"""
        raise NotImplementedError

    def orthogonal_line(self, through: Vector):
        """:return: Line orthogonal to self and through the given point"""
        raise NotImplementedError

    def intersection(self, other):
        """
        :return: intersection point of self and other or None if both lines don't
        intersect or a line of both lines share an infinite number of points
        """
        raise NotImplementedError
