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



def test_getitem_1():
    dct = lazydict(a=1, b=defer(2), c=defer(3))
    assert dct['a'] == 1
    assert len(dct._unresolved) == 2
    assert dct['b'] == (1, 2)
    assert len(dct._unresolved) == 1
    assert dct['c'] == (1, 3)
    assert len(dct._unresolved) == 0
    assert len(dct._resolved) == 3

    # Repeat indexing to check called
    assert dct['b'] == (1, 2)
    assert dct['c'] == (1, 3)
    assert len(dct._unresolved) == 0
    assert len(dct._resolved) == 3


def test_getitem_keyerror():
    dct = lazydict(a=1, b=defer(2), c=defer(3))
    assert dct['a'] == 1
    with pytest.raises(KeyError):
        _ = dct['x']
    assert len(dct._unresolved) == 2


def test_getitem_ordering():
    dct = lazydict(a=1, b=defer(2), c=defer(3), d=defer(4))
    _ = dct['d']
    _ = dct['c']
    assert list(iter(dct)) == ['a', 'b', 'c', 'd']
