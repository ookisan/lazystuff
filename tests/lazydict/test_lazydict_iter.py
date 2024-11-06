import pytest

from lazystuff import lazydict


# pylint:disable=protected-access

def defer(value):
    called = 0

    def _impl():
        nonlocal called
        called += 1
        return (called, value)

    return _impl


def test_iter_1():
    dct = lazydict(a=defer(1), b=defer(2), c=defer(3))
    act = list(iter(dct))
    assert act == ['a', 'b', 'c']
    assert len(dct._unresolved) == 3


def test_keys():
    dct = lazydict(a=defer(1), b=defer(2), c=defer(3))
    act = list(dct.keys())
    assert act == ['a', 'b', 'c']
    assert len(dct._unresolved) == 3


def test_values():
    dct = lazydict(a=defer(1), b=defer(2), c=defer(3))
    act = list(dct.values())
    assert act == [(1, 1), (1, 2), (1, 3)]
    assert len(dct._unresolved) == 0
    act = list(dct.values())
    assert act == [(1, 1), (1, 2), (1, 3)]


def test_items():
    dct = lazydict(a=defer(1), b=defer(2), c=defer(3))
    act = list(dct.items())
    assert act == [('a', (1, 1)), ('b', (1, 2)), ('c', (1, 3))]
    assert len(dct._unresolved) == 0
    act = list(dct.items())
    assert act == [('a', (1, 1)), ('b', (1, 2)), ('c', (1, 3))]
