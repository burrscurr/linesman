import pytest

from linesman.geometry import Line, Vector


def test_line_init():
    v1 = Vector(1, 0)
    with pytest.raises(ValueError, match='.*? cannot be defined by one.*'):
        Line(v1, v1)


def test_line_contains():
    l = Line(Vector(1, 1), Vector(3, 2))
    assert Vector(1, 1) in l
    assert Vector(2, 1.5) in l
    assert Vector(0, 0) not in l


def test_line_equality_simple():
    l = Line(Vector(1, 1), Vector(-2, 5))
    assert l == l


def test_line_equality_different_definition():
    l1 = Line(Vector(0, 0), Vector(-3, 4))
    l2 = Line(Vector(-6, 8), Vector(3, -4))
    assert l1 == l2


def test_line_point_0():
    l = Line(Vector(1, 1), Vector(3, 2))
    assert l.point() == Vector(1, 1)


def test_line_point_1():
    l = Line(Vector(1, 1), Vector(3, 2))
    assert l.point(1) == Vector(3, 2)


def test_line_point():
    l = Line(Vector(1, 1), Vector(3, 2))
    assert l.point(-2) == Vector(-3, -1)
    assert l.point(1.5) == Vector(4, 2.5)


def test_line_direction():
    v1 = Vector(1, 0)
    v2 = Vector(5, 3)
    l = Line(v1, v2)
    assert l.direction == v2 - v1
