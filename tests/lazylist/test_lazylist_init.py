from lazystuff import lazylist


def test_empty_init():
    act = lazylist()
    assert len(act) == 0

def test_list_init():
    act = lazylist(list(range(1, 11)))
    assert act._strict == list(range(1, 11))
    assert len(act._tails) == 0

def test_iterable_init():
    init = range(1, 11)
    act = lazylist(init)
    assert act._strict == []
    assert len(act._tails) == 1
    assert type(act._tails[0]) is type(iter(init))

def test_iterator_init():
    init = iter(range(1, 11))
    act = lazylist(init)
    assert act._strict == []
    assert len(act._tails) == 1
    assert act._tails[0] is init
