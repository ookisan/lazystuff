import contextlib

import pytest

from lazystuff import lazylist


def _maybe_raises(exp, exc):
    if exp is None:
        return pytest.raises(exc)
    else:
        return contextlib.nullcontext()


def test_keyword_arg_names():
    lst1 = lazylist([1, 2, 3, 4, 5, 6])
    _ = lst1.index(1, start=0)
    _ = lst1.index(1, stop=100)


@pytest.mark.parametrize('init,value,start,stop,exp', (
    (([1, 2, 3, 4, 5],), 4, None, None, 3),
    ((range(1, 6),), 4, None, None, 3),
    ((range(1, 6), range(6, 10), range(10, 30)), 29, None, None, 28),
    ((range(1, 6), range(6, 10), range(10, 30)), 29, None, 28, None),
    ((range(1, 6), range(6, 10), range(10, 30)), 1, 1, None, None),
))
def test_index_success(init, value, start, stop, exp):
    lst1 = lazylist()
    lst2 = []
    for elem in init:
        lst1.extend(elem)
        lst2.extend(elem)
    args = [value]
    if start is not None or stop is not None:
        args.append(start or 0)
    if stop is not None:
        args.append(stop)
    with _maybe_raises(exp, ValueError):
        act = lst1.index(*args)
        assert act == lst2.index(*args)
        assert act == exp
