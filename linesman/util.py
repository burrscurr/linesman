import math


# Floating point operations are prone to rounding error. For equality operations,
# consider values equal when they are differing less than EPSILON.
EPSILON = 10E-12


class Vector:
    """A vector (point) in 2-dimensional space. Instances are immutable."""
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def orthogonal_vector(self):
        """:return: Vector orthogonal to self"""
        return Vector(self.y, -self.x)

    def parallel_to(self, other):
        """
        :return: whether self and other are parallel; null vector is considered
        parallel to every other vector.
        """
        # determinant method
        return abs(self.x*other.y - self.y*other.x) < EPSILON

    def __eq__(self, other):
        return abs(self._x - other._x) < EPSILON and \
                abs(self._y - other._y) < EPSILON

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """:return: vector product if argument is vector"""
        if isinstance(other, Vector):
            return self.x*other.x + self.y*other.y
        elif isinstance(other, (float, int)):
            return Vector(other*self.x, other*self.y)
        return NotImplemented

    def __rmul__(self, factor):
        """:return: scalar product if argument is scalar"""
        if type(factor) == int or type(factor) == float:
            return Vector(self.x*factor, self.y*factor)
        return NotImplemented

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __str__(self):
        return f'({self._x}, {self._y})'

    def __repr__(self):
        return str(self)


class Line:
    """Class for a line in a 2-dimensional space. Instances are immutable."""
    def __init__(self, a: Vector, b: Vector):
        if a == b:
            raise ValueError('line cannot be defined by one point')
        self._p1 = a
        self._p2 = b

    def __contains__(self, other: Vector):
        """:return: whether the line contains a certain point"""
        other = other - self._p1
        return self.direction.parallel_to(other)

    def __eq__(self, other):
        """:return: whether all points described by self are also on other"""
        if type(self) != type(other):
            return NotImplemented
        if self.direction.parallel_to(other.direction):
            print('are parallel')
            if self.point(0) in other:
                return True
            print('but no matching point')
        return False

    def __repr__(self):
        return f'Line({self._p1}, {self._p2})'

    @property
    def direction(self):
        return self._p2 - self._p1

    def point(self, factor=0):
        """
        :return: point on the line based on the first initialization point added
        to the factor-th of the vector from first to second initialization point.
        """
        return self._p1 + factor*self.direction

    def move(self, vec: Vector):
        """:return: line moved with given vector"""
        return Line(self._p1 + vec, self._p2 + vec)

    def project(self, point: Vector):
        """:return: projection of given point onto the line"""
        # move line and argument such that both start in (0, 0)
        origin_line = self.move(-self._p1)
        span = origin_line._p2 - origin_line._p1
        point = point - self._p1
        return ((point*span)/(span*span))*span + self._p1

    def orthogonal_line(self, through: Vector):
        """:return: Line orthogonal of self through the given point"""
        span = self._p2 - self._p1
        return Line(through, through + span.orthogonal_vector())

    def intersection(self, other):
        """
        :return: intersection point of self and other or None if both lines don't
        intersect or a line of both lines share an infinite number of points
        """
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
