from lazystuff import lazylist


def test_add_list_to_empty():
    act = lazylist()
    lst = list(range(1, 11))
    act._add_tail(lst)
    assert act._strict is not lst
    assert act._strict == lst
    assert not act._tails

def test_add_iterator_to_empty():
    act = lazylist()
    iterator = iter(range(1, 11))
    act._add_tail(iterator)
    assert act._strict == []
    assert len(act._tails) == 1
    assert act._tails[0] is iterator

def test_add_iterator_to_strict():
    act = lazylist()
    lst = list(range(1, 11))
    iterator = iter(range(1, 11))
    act._add_tail(lst)
    assert act._is_strict() is True
    act._add_tail(iterator)
    assert act._is_strict() is False
    assert act._strict == lst
    assert act._strict is not lst
    assert len(act._tails) == 1
    assert act._tails[0] is iterator

def test_add_list_to_nonstrict():
    act = lazylist()
    lst = list(range(1, 11))
    iterator = iter(range(1, 11))
    act._add_tail(iterator)
    act._add_tail(lst)
    assert act._strict == []
    assert len(act._tails) == 2
    assert act._tails[0] is iterator
    assert act._tails[1] is not lst
    assert act._tails[1] == lst
