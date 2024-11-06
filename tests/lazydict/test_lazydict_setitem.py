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



def test_setitem_1():
    dct = lazydict(a=1, b=defer(2), c=defer(3))
    dct['x'] = defer(4)
    assert callable(dct['x'])
    assert dct['x']() == (1, 4)
    assert len(dct._unresolved) == 2
