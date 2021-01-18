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


def test_line_orthogonal_line():
    l = Line(Vector(1, 3), Vector(-2, 2))
    p = Vector(4, 4)
    orthogonal_l = l.orthogonal_line(through=p)
    assert orthogonal_l.project(p) == p
    assert orthogonal_l.direction * l.direction == 0


def test_line_project_point_on_line():
    line = Line(Vector(0, 0), Vector(3, 3))
    assert line.project(Vector(1, 1)) == Vector(1, 1)


def test_line_project_within_line_points():
    line = Line(Vector(3, 3), Vector(-1, 5))
    assert line.project(Vector(-1, 2)) == Vector(0.2, 4.4)


def test_line_project_outside_line_points():
    line = Line(Vector(1, 1), Vector(3, 3))
    assert line.project(Vector(-2, 0)) == Vector(-1, -1)


def test_line_project_non_origin_line():
    line = Line(Vector(0, 1), Vector(2, 2))
    assert line.project(Vector(3, 0)) == Vector(2, 2)


def test_line_intersection_parallel_equal():
    l1 = Line(Vector(0, 0), Vector(2, 2))
    l2 = Line(Vector(-1, -1), Vector(4, 4))
    assert l1.intersection(l2) == l1
    assert l1.intersection(l2) == l2


def test_line_intersection_commutativity():
    l1 = Line(Vector(0, 0), Vector(2, 2))
    l2 = Line(Vector(-3, 3), Vector(3, 0))
    assert l1.intersection(l2) == Vector(1, 1)
    assert l2.intersection(l1) == Vector(1, 1)


def test_line_intersection_parallel():
    l1 = Line(Vector(0, 0), Vector(1, 1))
    l2 = l1.move(Vector(-2, 1))
    assert l1.intersection(l2) is None


def test_line_intersection():
    l1 = Line(Vector(0, 2), Vector(4, 0))
    l2 = Line(Vector(0, 0), Vector(1, 1))
    assert l1.intersection(l2) == Vector(4/3, 4/3)
