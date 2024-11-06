import pytest

from lazystuff import lazylist


def test_equal():
    left = lazylist(range(1, 11))
    right = lazylist(list(range(1, 11)))
    assert left.__eq__(right)
    assert not left.__ne__(right)
    assert left._is_strict()
    assert right._is_strict()

def test_mixed_types_list():
    left = lazylist(range(1, 5))
    right = [1, 2, 3, 4]
    assert left == right
    assert right == left

def test_mixed_types_tuple():
    left = lazylist(range(1, 5))
    right = (1, 2, 3, 4)
    assert left != right
    assert right != left

def test_mixed_types_iterable():
    left = lazylist(range(1, 5))
    right = range(1, 5)
    assert left != right
    assert right != left

def test_wrong_types():
    assert lazylist().__eq__(1) is False
    assert lazylist().__ne__(1) is True

def test_left_shorter():
    left = lazylist(range(1, 10))
    right = lazylist(range(1, 11))
    assert not left.__eq__(right)
    assert left.__ne__(right)
    assert left._is_strict() is True
    assert right._is_strict() is False

def test_right_shorter():
    left = lazylist(range(1, 11))
    right = lazylist(range(1, 10))
    assert not left.__eq__(right)
    assert left.__ne__(right)
    assert left._is_strict() is False
    assert right._is_strict() is True

def test_inequal_first():
    left = lazylist(iter(['a', 2, 3, 4, 5]))
    right = lazylist(iter(['b', 2, 3, 4, 5]))
    assert not left.__eq__(right)
    assert left.__ne__(right)
    assert left._is_strict() is False
    assert right._is_strict() is False


def test_empty_1():
    left = lazylist()
    right = lazylist()
    assert left.__eq__(right) is True
    assert left.__ne__(right) is False

def test_empty_2():
    left = lazylist(range(5))
    right = lazylist()
    assert left.__eq__(right) is False
    assert left.__ne__(right) is True

def test_empty_3():
    left = lazylist()
    right = lazylist(range(5))
    assert left.__eq__(right) is False
    assert left.__ne__(right) is True
