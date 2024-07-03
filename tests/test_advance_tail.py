from lazy import lazylist


def test_merge_lists():
    act = lazylist([1])
    act.extend(iter(range(2, 5)))
    act.extend([2, 3])
    act.extend([4, 5])
    assert act._strict == [1]
    assert type(act._tail) is type(iter(range(1, 2)))
    assert len(act._tails) is 2
    act._advance_tail()
    assert act._strict == [1, 2, 3, 4, 5]
    assert act._tail is None
    assert not act._tails

def test_with_iterable_tail():
    act = lazylist([1])
    iter1 = iter(range(2, 5))
    iter2 = iter(range(5, 7))
    iter3 = iter(range(7, 11))
    act.extend(iter1)
    act.extend(iter2)
    act.extend(iter3)
    assert act._strict == [1]
    assert act._tail is iter1
    assert act._tails[0] is iter2
    assert act._tails[1] is iter3
    assert len(act._tails) is 2
    act._advance_tail()
    assert act._tail is iter2
    assert act._tails
    assert act._tails[0] is iter3
    assert len(act._tails) is 1
