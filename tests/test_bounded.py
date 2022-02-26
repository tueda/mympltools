import numpy as np

import mympltools as mt


def test_bounded_init() -> None:
    a = mt.Bounded([1, 2, 3])
    b = mt.Bounded([1, 2, 3], xlo=[1, 2, 3], xhi=[1, 2, 3])
    assert a == b

    a = mt.Bounded([1, 2, 3], 2)
    b = mt.Bounded([1, 2, 3], xlo=[-1, 0, 1], xhi=[3, 4, 5])
    assert a == b

    a = mt.Bounded([1, 2, 3], [1, 2, 1])
    b = mt.Bounded([1, 2, 3], xlo=[0, 0, 2], xhi=[2, 4, 4])
    assert a == b

    a = mt.Bounded([1, 2, 3], 2, 3)
    b = mt.Bounded([1, 2, 3], xlo=[-1, 0, 1], xhi=[4, 5, 6])
    assert a == b

    a = mt.Bounded([1, 2, 3], [1, 1, 2], [1, 2, 1])
    b = mt.Bounded([1, 2, 3], xlo=[0, 1, 1], xhi=[2, 4, 4])
    assert a == b

    a = mt.Bounded(5, [1, 1, 2])
    b = mt.Bounded([5, 5, 5], xlo=[4, 4, 3], xhi=[6, 6, 7])
    assert a == b

    a = mt.Bounded(5, [1, 1, 2], [1, 2, 1])
    b = mt.Bounded([5, 5, 5], xlo=[4, 4, 3], xhi=[6, 7, 6])
    assert a == b


def test_bounded_dx() -> None:
    a = mt.Bounded([10, 10, 10], xlo=[9, 7, 6], xhi=[12, 11, 14])
    c = a.dx
    assert np.array_equal(c, np.array([2, 3, 4]))


def test_bounded_pos() -> None:
    a = mt.Bounded(10, xlo=9, xhi=12)
    c = +a
    assert c == mt.Bounded(10, xlo=9, xhi=12)

    assert +a == a


def test_bounded_neg() -> None:
    a = mt.Bounded(10, xlo=9, xhi=12)
    c = -a
    assert c == mt.Bounded(-10, xlo=-12, xhi=-9)

    assert -(-a) == a


def test_bounded_add() -> None:
    a = mt.Bounded(10, xlo=9, xhi=12)
    b = mt.Bounded(100, xlo=90, xhi=120)
    c = a + b
    assert c == mt.Bounded(110, xlo=99, xhi=132)

    a = mt.Bounded(10, xlo=9, xhi=12)
    n = -8
    c = a + n
    assert c == mt.Bounded(2, xlo=1, xhi=4)

    d = n + a
    assert d == mt.Bounded(2, xlo=1, xhi=4)


def test_bounded_sub() -> None:
    a = mt.Bounded(10, xlo=9, xhi=12)
    b = mt.Bounded(100, xlo=90, xhi=120)
    c = a - b
    assert c == mt.Bounded(-90, xlo=-111, xhi=-78)

    a = mt.Bounded(10, xlo=9, xhi=12)
    n = -8
    c = a - n
    assert c == mt.Bounded(18, xlo=17, xhi=20)

    d = n - a
    assert d == mt.Bounded(-18, xlo=-20, xhi=-17)


def test_bounded_mul() -> None:
    a = mt.Bounded(10, xlo=9, xhi=12)
    b = mt.Bounded(100, xlo=90, xhi=120)
    c = a * b
    assert c == mt.Bounded(1000, xlo=810, xhi=1440)

    a = mt.Bounded(8, xlo=-5, xhi=12)
    b = mt.Bounded(-2, xlo=-8, xhi=10)
    c = a * b
    assert c == mt.Bounded(-16, xlo=-96, xhi=120)

    a = mt.Bounded(-10, xlo=-12, xhi=-5)
    b = mt.Bounded(-5, xlo=-10, xhi=-2)
    c = a * b
    assert c == mt.Bounded(50, xlo=10, xhi=120)

    a = mt.Bounded(10, xlo=9, xhi=12)
    n = -8
    c = a * n
    assert c == mt.Bounded(-80, xlo=-96, xhi=-72)

    d = n * a
    assert d == mt.Bounded(-80, xlo=-96, xhi=-72)


def test_bounded_div() -> None:
    a = mt.Bounded(6, xlo=-9, xhi=12)
    n = -3
    c = a / n
    assert c == mt.Bounded(-2, xlo=-4, xhi=3)


def test_bounded_pow() -> None:
    a = mt.Bounded([-4, -2, 1, 8], xlo=[-5, -7, -4, 7], xhi=[-3, 3, 5, 9])
    n = 4
    c = a**n
    assert c == mt.Bounded(
        [256, 16, 1, 4096], xlo=[81, 0, 0, 2401], xhi=[625, 2401, 625, 6561]
    )

    n = 5
    c = a**n
    assert c == mt.Bounded(
        [-1024, -32, 1, 32768],
        xlo=[-3125, -16807, -1024, 16807],
        xhi=[-243, 243, 3125, 59049],
    )
