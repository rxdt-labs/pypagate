import pytest

from pypagate import Term
from pypagate.source import SourceMap, exec_always, exec_either, exec_while


def test_always():
    source = SourceMap({})
    x = 0
    @exec_always(source)
    def f():
        nonlocal x
        x += 1

    for i in range(3):
        assert x == i
        source.listen({})


def test_source_values():
    source = SourceMap({"a": 1, "b": 2})
    assert source["a"].value == 1
    assert source.b.value == 2
    source.listen({"a": 10})
    assert source["a"].value == 10
    assert source.b.value == 2


def test_source_formula():
    source = SourceMap({"a": 1, "b": 2})
    total = source.a + source.b
    assert int(total) == 3
    source.listen({"a": 5, "b": 6})
    assert int(total) == 11


def test_source_missing_key():
    source = SourceMap({"a": 1})
    with pytest.raises(KeyError):
        source.listen({"nope": 1})
    with pytest.raises(KeyError):
        source["nope"]


def test_while():
    source = SourceMap({"a": 0})
    fires = []
    @exec_while(source.a > 2, source)
    def f():
        fires.append(source.a.value)
    source.listen({"a": 1})
    source.listen({"a": 3})
    source.listen({"a": 5})
    assert fires == [3, 5]


def test_while_reactive():
    source = SourceMap({"a": 0, "b": 0})
    fires = []
    @exec_while(source.a + source.b >= 10, source)
    def f():
        fires.append((source.a.value, source.b.value))
    source.listen({"a": 4, "b": 4})
    source.listen({"a": 6, "b": 5})
    assert fires == [(6, 5)]


def test_either():
    source = SourceMap({"a": 0})
    results = []
    @exec_either(source.a == 0, lambda: results.append("true"),
                 lambda: results.append("false"), source)
    def func():
        pass
    source.listen({"a": 0})
    source.listen({"a": 1})
    source.listen({"a": 0})
    assert results == ["true", "false", "true"]


def test_always_with_terms():
    source = SourceMap({"a": 1})
    seen = []
    @exec_always(source)
    def f():
        seen.append(source.a.value)
    source.listen({"a": 2})
    source.listen({"a": 3})
    assert seen == [2, 3]
