from lazystuff import lazylist


def test_empty_init():
    act = lazylist()
    assert len(act) == 0

def test_list_init():
    act = lazylist(list(range(1, 11)))
    assert act._strict == list(range(1, 11))
    assert act._tail is None
    assert not act._tails

def test_iterable_init():
    init = range(1, 11)
    act = lazylist(init)
    assert act._strict == []
    assert type(act._tail) is type(iter(init))
    assert not act._tails

def test_iterator_init():
    init = iter(range(1, 11))
    act = lazylist(init)
    assert act._strict == []
    assert act._tail is init
    assert not act._tails
