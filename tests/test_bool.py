from lazy import lazylist


def test_empty():
    act = lazylist()
    assert bool(act) is False

def test_nonempty_iterable():
    act = lazylist(range(1, 11))
    assert bool(act) is True
    assert act._strict == [1]
    assert act._tail
    assert not act._tails
