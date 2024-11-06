from lazystuff import lazylist


def test_equal():
    lst1 = lazylist(range(1, 5))
    lst2 = lazylist(range(1, 5))
    assert not lst1 < lst2
    assert not lst2 < lst1

def test_differing_elements():
    smaller = lazylist(iter([1, 1, 3, 4, 5]))
    larger = lazylist(iter([1, 2, 3, 4, 5]))
    assert smaller < larger
    assert not larger < smaller

def test_differing_lengths():
    smaller = lazylist(iter([1, 2, 3]))
    larger = lazylist(iter([1, 2, 3, 4]))
    assert smaller < larger
    assert not larger < smaller

def test_last_element_differs():
    smaller = lazylist(iter([1, 2, 3]))
    larger = lazylist(iter([1, 2, 4]))
    assert smaller < larger
    assert not larger < smaller

def test_empty_lists():
    assert not lazylist() < lazylist()
    assert not lazylist([1]) < lazylist()
    assert lazylist() < lazylist([1])
