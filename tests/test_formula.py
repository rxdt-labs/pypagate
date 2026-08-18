from pypagate import Const, Term, evaluate


def test_arithmetic_ops():
    x = Term(10)
    y = Term(2)
    assert int(x + y) == 12
    assert int(x - y) == 8
    assert int(x * y) == 20
    assert float(x / y) == 5.0
    assert int(x // y) == 5
    assert int(x ** y) == 100
    assert int(x ^ y) == 8


def test_arithmetic_with_literal():
    x = Term(10)
    assert int(x + 5) == 15
    assert int(x - 5) == 5
    assert int(x * 5) == 50
    assert float(x / 5) == 2.0
    assert int(x // 3) == 3
    assert int(x ** 2) == 100
    assert int(x ^ 3) == 9


def test_reverse_ops():
    x = Term(10)
    assert int(2 + x) == 12
    assert int(20 - x) == 10
    assert int(2 * x) == 20
    assert float(20 / x) == 2.0
    assert int(20 // x) == 2
    assert int(2 ** x) == 1024
    assert int(2 ^ x) == 8


def test_reverse_ops_reactive():
    x = Term(10)
    sub = 20 - x
    div = 20 / x
    assert int(sub) == 10
    assert float(div) == 2.0
    x.change(4)
    assert int(sub) == 16
    assert float(div) == 5.0


def test_unary_ops():
    x = Term(-5)
    assert int(-x) == 5
    assert int(+x) == -5
    assert int(abs(x)) == 5
    y = Term(5)
    assert int(-y) == -5


def test_unary_ops_reactive():
    x = Term(-5)
    neg = -x
    pos = +x
    mag = abs(x)
    assert int(neg) == 5
    assert int(mag) == 5
    x.change(3)
    assert int(neg) == -3
    assert int(pos) == 3
    assert int(mag) == 3


def test_comparisons():
    x = Term(3)
    y = Term(4)
    assert bool(x < y)
    assert bool(x <= y)
    assert not bool(x > y)
    assert not bool(x >= y)
    assert not bool(x == y)
    assert bool(x != y)
    assert bool(x < 4)
    assert bool(3 < y)
    assert bool(x == 3)
    assert bool(3 == x)


def test_comparisons_reactive():
    x = Term(3)
    lt = x < 5
    eq = x == 5
    assert bool(lt)
    assert not bool(eq)
    x.change(5)
    assert not bool(lt)
    assert bool(eq)
    x.change(6)
    assert not bool(eq)


def test_nested_formula():
    x = Term(2)
    y = Term(3)
    z = (x + y) * 2 - x
    assert int(z) == 8
    x.change(5)
    assert int(z) == 11
    y.change(1)
    assert int(z) == 7


def test_formula_of_formula():
    x = Term(2)
    y = x + 1
    z = y * 2
    assert int(z) == 6
    x.change(5)
    assert int(y) == 6
    assert int(z) == 12


def test_evaluate():
    x = Term(2)
    y = Term(3)
    assert evaluate(x + y) == 5
    assert evaluate(x) == 2
    assert evaluate(x * 2 + y) == 7


def test_const():
    c = Const(5)
    assert c.value == 5
    x = Term(2)
    f = x + c
    assert int(f) == 7
    x.change(10)
    assert int(f) == 15


def test_str_and_float():
    x = Term(5)
    y = x + 1
    assert str(y) == '6'
    assert float(x) == 5.0
    x.change(5.5)
    assert float(x) == 5.5


def test_repr_binary():
    x = Term(1)
    y = Term(2)
    assert repr(x + y) == "Var[1] + Var[2]"
    assert repr(x - y) == "Var[1] - Var[2]"
    assert repr(x * y) == "Var[1] * Var[2]"
    assert repr(x / y) == "Var[1] / Var[2]"
    assert repr(x // y) == "Var[1] // Var[2]"
    assert repr(x == y) == "Var[1] == Var[2]"
    assert repr(x < y) == "Var[1] < Var[2]"


def test_repr_pow():
    x = Term(2)
    y = Term(3)
    assert repr(x ** y) == "Var[2] pow Var[3]"


def test_repr_prefix():
    x = Term(-5)
    assert repr(-x) == "- (Var[-5])"
    assert repr(abs(x)) == "abs (Var[-5])"


def test_repr_nested():
    x = Term(1)
    y = Term(2)
    f = (x + y) * 2
    assert repr(f) == " (Var[1] + Var[2])  * Const(value=2)"


def test_register_func():
    from pypagate import register_func

    def add3(a, b, c):
        return a + b + c

    radd3 = register_func(add3)
    x = Term(1)
    y = Term(2)
    z = Term(3)
    f = radd3(x, y, z)
    assert int(f) == 6
    x.change(10)
    assert int(f) == 15
    assert repr(f) == "add3 (Var[10], Var[2], Var[3])" or f"add3 ({repr(x)}, {repr(y)}, {repr(z)})" == "add3 (Var[10], Var[2], Var[3])"


def test_term_init_default():
    x = Term()
    assert x.value is None


def test_value_caching():
    x = Term(2)
    f = x + 1
    assert f.value == 3
    assert f.value == 3
    x.change(10)
    assert f.value == 11
