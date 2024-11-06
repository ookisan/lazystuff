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


def test_delitem_1():
    dct = lazydict(a=1, b=defer(2), c=defer(3))
    assert len(dct._unresolved) == 2
    del dct['b']
    assert len(dct._unresolved) == 1
    assert dct['a'] == 1
    assert dct['c'] == (1, 3)


def test_delitem_missing_key():
    dct = lazydict(a=1, b=defer(2), c=defer(3))
    del dct['x']
    assert len(dct._resolved) == 3
    assert len(dct._unresolved) == 2
