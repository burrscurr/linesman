from .abstract import StraightLine, Vector


class Line(StraightLine):
    """Class for a line in a 2-dimensional space. Instances are immutable."""
    def __contains__(self, other: Vector):
        other = other - self._p1
        return self.direction.parallel_to(other)

    @property
    def direction(self):
        return self._p2 - self._p1

    def point(self, factor=0):
        return self._p1 + factor*self.direction

    def move(self, vec: Vector):
        """:return: line moved in direction of the given vector"""
        return Line(self._p1 + vec, self._p2 + vec)

    def project(self, point: Vector):
        line = self._p2 - self._p1
        return self._p1 + ((point - self._p1)*line/(line*line))*line

    def orthogonal_line(self, through: Vector):
        span = self._p2 - self._p1
        return Line(through, through + span.orthogonal_vector())

    def intersection(self, other):
        if self == other:
            return self
        if self.direction.parallel_to(other.direction):
            return None

        # solve the linear equation system derived from equality of both lines
        o_dir = other.direction
        s_dir = self.direction
        factor = (o_dir.y*(self.point(0).x - other.point(0).x) \
                  - o_dir.x*(self.point(0).y - other.point(0).y)) \
            / (o_dir.x*s_dir.y - o_dir.y*s_dir.x)
        # divisor is the determinant of line directions and != 0 if
        # lines aren't parallel (which is guaranteed here)
        return self.point(factor)
