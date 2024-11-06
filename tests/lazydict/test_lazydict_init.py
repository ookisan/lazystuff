import pytest

from lazystuff import lazydict


# pylint:disable=protected-access

def test_init_list():
    dct = lazydict((('a', 1), ('b', 2), ('c', 3)))
    assert dct._resolved == {'a': 1, 'b': 2, 'c': 3}
    assert not dct._unresolved


def test_init_kwargs():
    dct = lazydict(a=1, b=2, c=3)
    assert dct._resolved == {'a': 1, 'b': 2, 'c': 3}
    assert not dct._unresolved


def test_init_mixed():
    dct = lazydict((('a', 1), ('b', 2)), c=3)
    assert dct._resolved == {'a': 1, 'b': 2, 'c': 3}
    assert not dct._unresolved


def test_init_dict():
    def f(): None
    def g(): None
    dct = lazydict({'a': 1, 'b': f, 'c': g})
    assert dct._resolved == {'a': 1, 'b': None, 'c': None}
    assert dct._unresolved == {'b': f, 'c': g}


def test_init_callable():
    def f(): None
    def g(): None
    dct = lazydict((('a', f),), b=g)
    assert dct._resolved == {'a': None, 'b': None}
    assert dct._unresolved == {'a': f, 'b': g}


def test_init_iterable():
    dct = lazydict((range(2), range(1, 3)))
    assert dct._resolved == {0: 1, 1: 2}
    assert not dct._unresolved


def test_init_too_many_args():
    with pytest.raises(TypeError):
        dct = lazydict(('a', 1), ('b', 2))


def test_init_too_short_init():
    with pytest.raises(ValueError):
        dct = lazydict((('a', 1), ('b',)))


def test_init_uniterable_init():
    with pytest.raises(TypeError):
        dct = lazydict((('a', 1), 1))


def test_init_too_long_init():
    with pytest.raises(ValueError):
        dct = lazydict((('a', 1), ('b', 1, 2)))
