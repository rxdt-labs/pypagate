import math as _math

from pypagate import Term
from pypagate.math import (ceil, comb, cos, degrees, exp, factorial, floor,
                           gcd, hypot, lcm, log, pi, e, pow, radians, sin, sqrt,
                           tan)


def test_sqrt():
    x = Term(4)
    y = sqrt(x)
    assert float(y) == 2.0
    x.change(9)
    assert float(y) == 3.0


def test_pow():
    x = Term(2)
    y = pow(x, 3)
    assert float(y) == 8.0
    x.change(3)
    assert float(y) == 27.0


def test_sin_cos_tan():
    x = Term(0)
    assert float(sin(x)) == 0.0
    assert float(cos(x)) == 1.0
    assert float(tan(x)) == 0.0
    x.change(_math.pi / 2)
    assert abs(float(sin(x)) - 1.0) < 1e-9


def test_exp_log():
    x = Term(1)
    assert float(exp(x)) == _math.e
    assert float(log(x)) == 0.0
    x.change(2)
    assert abs(float(log(x)) - _math.log(2)) < 1e-9


def test_ceil_floor():
    x = Term(1.5)
    assert int(ceil(x)) == 2
    assert int(floor(x)) == 1
    x.change(-1.5)
    assert int(ceil(x)) == -1
    assert int(floor(x)) == -2


def test_gcd_lcm():
    x = Term(12)
    y = Term(18)
    assert int(gcd(x, y)) == 6
    assert int(lcm(x, y)) == 36
    x.change(15)
    assert int(gcd(x, y)) == 3
    assert int(lcm(x, y)) == 90


def test_hypot():
    x = Term(3)
    y = Term(4)
    assert float(hypot(x, y)) == 5.0
    x.change(6)
    assert float(hypot(x, y)) == _math.hypot(6, 4)


def test_comb_factorial():
    x = Term(5)
    y = Term(2)
    assert int(comb(x, y)) == 10
    assert int(factorial(x)) == 120
    x.change(6)
    assert int(comb(x, y)) == 15
    assert int(factorial(x)) == 720


def test_degrees_radians():
    x = Term(0)
    assert float(degrees(x)) == 0.0
    assert float(radians(x)) == 0.0
    x.change(_math.pi)
    assert abs(float(degrees(x)) - 180.0) < 1e-9
    x.change(180)
    assert abs(float(radians(x)) - _math.pi) < 1e-9


def test_constants():
    assert pi == _math.pi
    assert _math.isclose(pi, 3.14159, rel_tol=1e-4)
    assert e == _math.e
