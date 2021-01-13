import pytest

from linesman.util import Line, Vector


def test_vector_scale():
    scalar = 5
    vec = Vector(2, -3)
    expected = Vector(scalar*vec.x, scalar*vec.y)

    assert scalar*vec == expected 
    assert vec*scalar == expected 


def test_vector_product():
    v1 = Vector(-3, 2.5)
    v2 = Vector(2, 5)
    assert v1*v2 == (-3*2 + 2.5*5)


def test_negate():
    v1 = Vector(2, -3)
    assert -v1 == Vector(-v1.x, -v1.y)


def test_length():
    v1 = Vector(4, -3)
    v2 = Vector(0, 0)
    assert v1.length() == 5.0
    assert v2.length() == 0


def test_add():
    v1 = Vector(-3, 2.5)
    v2 = Vector(2, 5)
    assert v1 + v2 == Vector(v1.x + v2.x, v1.y + v2.y)


def test_subtract():
    v1 = Vector(-3, 2.5)
    v2 = Vector(2, 5)
    assert v1 - v2 == Vector(v1.x - v2.x, v1.y - v2.y)


def test_line():
    v1 = Vector(1, 0)
    with pytest.raises(ValueError, match='.*? cannot be defined by one.*'):
        Line(v1, v1)


def test_project_point_on_line():
    line = Line(Vector(0, 0), Vector(3, 3))
    assert line.project(Vector(1, 1)) == Vector(1, 1)


def test_project_within_line_points():
    line = Line(Vector(3, 3), Vector(-1, 5))
    expected = Vector(0.2, 4.4)
    actual = line.project(Vector(-1, 2))
    assert (expected - actual).length() < 0.000001  # rounding error


def test_project_outside_line_points():
    line = Line(Vector(1, 1), Vector(3, 3))
    assert line.project(Vector(-2, 0)) == Vector(-1, -1)


def test_project_non_origin_line():
    line = Line(Vector(0, 1), Vector(2, 2))
    assert line.project(Vector(3, 0)) == Vector(2, 2)
