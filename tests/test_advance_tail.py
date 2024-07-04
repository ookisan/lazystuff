from lazystuff import lazylist


def test_merge_lists():
    act = lazylist([1])
    act_iter = iter(act)
    act.extend(iter(range(2, 5)))
    act.extend([2, 3])
    act.extend([4, 5])
    assert act._strict == [1]
    assert len(act._tails) == 3
    assert type(act._tails[0]) is type(iter(range(2, 5)))
    for _ in range(5):  # Iterate past the range iterator
        next(act_iter)
    assert act._strict == [1, 2, 3, 4, 2, 3, 4, 5]
    assert not act._tails

def test_with_iterable_tail():
    act = lazylist([1])
    act_iter = iter(act)
    iter1 = iter(range(2, 5))
    iter2 = iter(range(5, 7))
    iter3 = iter(range(7, 11))
    act.extend(iter1)
    act.extend(iter2)
    act.extend(iter3)
    assert act._strict == [1]
    assert len(act._tails) == 3
    assert act._tails[0] is iter1
    assert act._tails[1] is iter2
    assert act._tails[2] is iter3
    for _ in range(5):  # Iterate past the range iterator
        next(act_iter)
    act._advance_tail()
    assert len(act._tails) == 2
    assert act._tails[0] is iter2
    assert act._tails[1] is iter3
