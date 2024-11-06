import pickle
import re

from lazystuff import lazylist


def test_pickle_basic():
    lst = lazylist([1, 2])
    lst.extend(range(3, 5))
    lst.extend([5, 6])
    act = pickle.loads(pickle.dumps(lst))
    assert isinstance(act, lazylist)
    assert act._strict == [1, 2, 3, 4, 5, 6]
    assert not act._tails

def test_reduce():
    lst = lazylist([1, 2])
    lst.extend(range(3, 5))
    lst.extend([5, 6])
    act_constructor, act_args = lst.__reduce__()
    assert act_constructor is lazylist
    assert act_args == ([1, 2, 3, 4, 5, 6],)
    assert lst._is_strict() is True

def test_reduce_ex():
    lst = lazylist([1, 2])
    lst.extend(range(3, 5))
    lst.extend([5, 6])
    act_constructor, act_args = lst.__reduce_ex__(1)
    assert act_constructor is lazylist
    assert act_args == ([1, 2, 3, 4, 5, 6],)
    assert lst._is_strict() is True
