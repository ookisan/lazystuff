from lazystuff import lazylist


def test_clear_empty():
    lst1 = lazylist()
    lst1.clear()
    assert lst1._strict == []
    assert not lst1._tails

def test_clear_full():
    lst1 = lazylist([1, 2, 3])
    lst1.extend(range(4, 7))
    lst1.extend(range(7, 9))
    lst1.clear()
    assert lst1._strict == []
    assert not lst1._tails
