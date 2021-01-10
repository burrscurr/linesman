import pytest

from linesman.util import project


def test_project_point_on_line():
    x, y = project((0, 0), (3, 3), (1, 1))
    assert x == 1
    assert y == 1


def test_project_within_line_points():
    x, y = project((0, 0), (3, 3), (0, 2))
    assert x == 1
    assert y == 1


def test_project_outside_line_points():
    x, y = project((0, 0), (3, 3), (-2, 0))
    assert x == -1
    assert y == -1


def test_project_non_origin_line():
    x, y = project((0, 1), (2, 2), (3, 0))
    assert x == 2
    assert y == 2

