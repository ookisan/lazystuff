from lazystuff import lazylist


def test_basic_iteration():
    lst = lazylist(range(1, 11))
    act = [x for x in lst]
    assert act == list(range(1, 11))

def test_lazy_iteration():
    act = lazylist(range(1, 11))
    iterator1 = iter(act)
    _ = next(iterator1)
    _ = next(iterator1)
    _ = next(iterator1)
    assert act._strict == [1, 2, 3]
    iterator2 = iter(act)
    _ = next(iterator2)
    _ = next(iterator2)
    _ = next(iterator2)
    assert act._strict == [1, 2, 3]

def test_iter_iter():
    act_iter_1 = iter(lazylist(range(1, 11)))
    act_iter_2 = iter(act_iter_1)
    assert act_iter_1 is act_iter_2
