import pytest

from linesman.geometry import Vector


@pytest.fixture
def minimal():
    # A vector distinct from (0, 0) but considered equal to (0, 0) by linesman
    # approximately 2**-1024 should be the smallest number representable as double
    v = Vector(0, 2**(-1000))
    assert v.y != 0
    return v


def test_vector_scale():
    scalar = 5
    vec = Vector(2, -3)
    expected = Vector(scalar*vec.x, scalar*vec.y)

    assert scalar*vec == expected 
    assert vec*scalar == expected 


def test_length():
    v1 = Vector(4, -3)
    v2 = Vector(0, 0)
    assert v1.length() == 5.0
    assert v2.length() == 0


def test_vector_product():
    v1 = Vector(-3, 2.5)
    v2 = Vector(2, 5)
    assert v1*v2 == (-3*2 + 2.5*5)


def test_equality_simple():
    assert Vector(2, 5) == Vector(2, 5)


def test_equality_practically_equal(minimal):
    v = Vector(2, 5)
    assert v == v + minimal


def test_negate():
    v1 = Vector(2, -3)
    assert -v1 == Vector(-v1.x, -v1.y)


def test_add():
    v1 = Vector(-3, 2.5)
    v2 = Vector(2, 5)
    assert v1 + v2 == Vector(v1.x + v2.x, v1.y + v2.y)


def test_subtract():
    v1 = Vector(-3, 2.5)
    v2 = Vector(2, 5)
    assert v1 - v2 == Vector(v1.x - v2.x, v1.y - v2.y)
