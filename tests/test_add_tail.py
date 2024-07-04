from lazystuff import lazylist


def test_add_list_to_empty():
    act = lazylist()
    lst = list(range(1, 11))
    act._add_tail(lst)
    assert act._strict is not lst
    assert act._strict == lst
    assert act._tail is None
    assert not act._tails

def test_add_iterator_to_empty():
    act = lazylist()
    iterator = iter(range(1, 11))
    act._add_tail(iterator)
    assert act._strict == []
    assert act._tail is iterator
    assert not act._tails

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
    assert act._tail is iterator
    assert not act._tails

def test_add_list_to_nonstrict():
    act = lazylist()
    lst = list(range(1, 11))
    iterator = iter(range(1, 11))
    act._add_tail(iterator)
    act._add_tail(lst)
    assert act._strict == []
    assert act._tail is iterator
    assert len(act._tails) is 1
    assert act._tails[0] is not lst
    assert act._tails[0] == lst
