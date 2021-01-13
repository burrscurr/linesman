import math


class Vector:
    """A vector (point) in 2-dimensional space."""
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

    def __eq__(self, other):
        return self._x == other._x and self._y == other._y

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
    """Class for a line in a 2-dimensional space."""
    def __init__(self, a: Vector, b: Vector):
        if a == b:
            raise ValueError('line cannot be defined by one point')
        self._p1 = a
        self._p2 = b

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
