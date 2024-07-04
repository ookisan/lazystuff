import pytest

from lazystuff import lazylist


def test_equal():
    lst1 = lazylist(range(1, 5))
    lst2 = lazylist(range(1, 5))
    assert lst1.__cmp__(lst2) == 0
    assert lst2.__cmp__(lst1) == 0
    assert lst1._is_strict() is True
    assert lst2._is_strict() is True


def test_differing_elements():
    smaller = lazylist(iter([1, 1, 3, 4, 5]))
    larger = lazylist(iter([1, 2, 3, 4, 5]))
    assert smaller.__cmp__(larger) == -1
    assert larger.__cmp__(smaller) == 1
    assert smaller._strict == [1, 1]
    assert larger._strict == [1, 2]


def test_differing_lengths():
    smaller = lazylist(iter([1, 2, 3]))
    larger = lazylist(iter([1, 2, 3, 4]))
    assert smaller.__cmp__(larger) == -1
    assert smaller._strict == [1, 2, 3]
    assert larger._strict == [1, 2, 3, 4]
    assert larger.__cmp__(smaller) == 1
    assert smaller._strict == [1, 2, 3]
    assert larger._strict == [1, 2, 3, 4]
    assert larger._is_strict() is False


def test_last_element_differs():
    smaller = lazylist(iter([1, 2, 3]))
    larger = lazylist(iter([1, 2, 4]))
    assert smaller.__cmp__(larger) == -1
    assert larger.__cmp__(smaller) == 1
    assert smaller._is_strict() is False
    assert larger._is_strict() is False


def test_empty_lists():
    assert lazylist().__cmp__(lazylist()) == 0
    assert lazylist().__cmp__(lazylist([1])) == -1
    assert lazylist([1]).__cmp__(lazylist()) == 1


def test_types_differ():
    with pytest.raises(TypeError) as exc:
        _ = lazylist().__cmp__('abc')
    assert 'comparison' in str(exc)
