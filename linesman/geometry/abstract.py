import math
import abc


# Floating point operations are prone to rounding error. For equality operations,
# consider values equal when they are differing less than EPSILON.
EPSILON = 10E-12


class Vector:
    """A vector (point) with two coordinates."""
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


class StraightLine(abc.ABC):
    """
    Abstract base class for the line through two points that is the shortest
    path between both points.
    There are implementations with planar and spherical geometry. Instances of
    the subclasses should not be mixed in use. However, the interface makes
    switching between both interpretations easier.
    """
    def __init__(self, a: Vector, b: Vector):
        if a == b:
            raise ValueError('Line cannot be defined by one point')
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
        :return: point on the line based on the first initialization
        point added to the factor-th of the direction of the line.
        """
        raise NotImplementedError

    def project(self, point: Vector):
        """
        :return: projection of given point onto the line such that the distance
        between the original point and the projected point is minimal.
        """
        raise NotImplementedError

    def orthogonal(self, through: Vector):
        """:return: line orthogonal to self and through the given point"""
        raise NotImplementedError

    def intersection(self, other):
        """
        :param other: instance of StraightLine of identical type like self
        :return: intersection point of self and other or None if both lines
        don't intersect or self if both lines share an infinite number of points
        """
        raise NotImplementedError
