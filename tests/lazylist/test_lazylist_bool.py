from lazystuff import lazylist


def test_empty():
    act = lazylist()
    assert bool(act) is False

def test_nonempty_iterable():
    act = lazylist(range(1, 11))
    assert bool(act) is True
    assert act._strict == [1]
    assert len(act._tails) == 1
