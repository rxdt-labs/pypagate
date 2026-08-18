from pypagate import Term, bind, either, fire_on, on_change, permit


def test_fire_on_args_kwargs():
    seen = []
    x = Term(1)
    @fire_on(x == 3, "hello", num=42)
    def f(greeting, num):
        seen.append((greeting, num))
    x += 1
    x += 1
    assert seen == [("hello", 42)]


def test_fire_on_term():
    seen = []
    x = Term(0)
    @fire_on(x)
    def f():
        seen.append(x.value)
    x.change(1)
    x.change(2)
    assert seen == [1, 2]


def test_fire_on_only_fires_when_true():
    seen = []
    x = Term(1)
    @fire_on(x == 1)
    def f():
        seen.append(x.value)
    x += 1
    x += 1
    x += 1
    x -= 1
    x -= 1
    x -= 1
    assert seen == [1]


def test_permit_args_kwargs():
    x = Term(3)
    def f(a, b, c=0):
        return a + b + c
    g = permit(x == 0)(f)
    assert g(1, 2) is None
    x -= 3
    assert g(1, 2) == 3
    assert g(1, 2, c=10) == 13


def test_permit_returns_none_when_blocked():
    x = Term(5)
    @permit(x == 0)
    def f():
        return 42
    assert f() is None
    x -= 5
    assert f() == 42


def test_on_change_old_new():
    values = []
    x = Term(1)
    @on_change(x)
    def f(old, new):
        values.append((old, new))
    x += 1
    x += 2
    assert values == [(1, 2), (2, 4)]


def test_on_change_no_fire_when_same():
    values = []
    x = Term(1)
    @on_change(x)
    def f(old, new):
        values.append((old, new))
    x.change(1)
    assert values == []


def test_on_change_extra_args():
    seen = []
    x = Term(1)
    @on_change(x, "extra", key="value")
    def f(old, new, extra, key):
        seen.append((old, new, extra, key))
    x += 1
    assert seen == [(1, 2, "extra", "value")]


def test_either_return_values():
    x = Term(0)
    def f():
        return "true"
    def g():
        return "false"
    switch = either(x == 0, f, g)
    assert switch() == "true"
    x += 1
    assert switch() == "false"


def test_bind_term():
    class Obj:
        pass
    obj = Obj()
    x = Term(5)
    bind(obj, "field", x)
    x += 1
    assert obj.field == 6
    x.change(10)
    assert obj.field == 10


def test_bind_formula():
    class Obj:
        pass
    obj = Obj()
    x = Term(5)
    y = Term(3)
    bind(obj, "field", x + y)
    x.change(10)
    assert obj.field == 13


def test_change_returns_none():
    x = Term(1)
    assert x.change(2) is None
    assert x.value == 2


def test_inplace_ops():
    x = Term(10)
    x -= 3
    assert x.value == 7
    x *= 2
    assert x.value == 14
    x //= 5
    assert x.value == 2
    x **= 3
    assert x.value == 8
    x += 2
    assert x.value == 10
    x ^= 3
    assert x.value == 9
    x /= 2
    assert x.value == 4.5


def test_inplace_ops_reactive():
    x = Term(2)
    y = Term(1)
    z = x + y
    assert int(z) == 3
    x += 3
    assert int(z) == 6
    x *= 2
    assert int(z) == 11
    y -= 1
    assert int(z) == 10
    x /= 2
    assert float(z) == 5.0


def test_on_change_formula():
    seen = []
    x = Term(1)
    y = x + 1
    @on_change(y)
    def f(old, new):
        seen.append((old, new))
    x.change(2)
    x.change(3)
    assert seen == [(2, 3), (3, 4)]


def test_fire_on_formula():
    seen = []
    x = Term(1)
    @fire_on(x > 5)
    def f():
        seen.append(x.value)
    x += 1
    x += 1
    x += 1
    x += 1
    x += 1
    x += 1
    assert seen == [6]