from lazystuff import lazylist


def test_count_basic():
    lst1 = lazylist(range(1, 5))
    for _ in range(4):
        lst1.extend(range(1, 5))
    assert lst1.count(2) == 5


def test_count_empty():
    lst1 = lazylist()
    assert lst1.count(None) == 0
    assert lst1.count(2) == 0
