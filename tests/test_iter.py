from lazystuff import lazylist


def test_iter_empty():
    lst = lazylist()
    iter1 = iter(lst)
    assert list(iter1) == []

def test_iter_lazy():
    lst = lazylist([1, 2, 3])
    lst.extend(range(4, 7))
    iter1 = iter(lst)
    assert next(iter1) == 1
    assert next(iter1) == 2
    assert next(iter1) == 3
    assert lst._strict == [1, 2, 3]

def test_iter_lazy_2():
    lst = lazylist(range(1, 5))
    iter1 = iter(lst)
    assert next(iter1) == 1
    assert next(iter1) == 2
    assert lst._strict == [1, 2]

def test_iter_multi():
    lst1 = lazylist(range(1, 5))
    iter1 = iter(lst1)
    iter2 = iter(lst1)
    assert iter1 is not iter2
    assert next(iter1) == 1
    assert next(iter2) == 1
    assert lst1._strict == [1]
    assert next(iter1) == 2
    assert next(iter1) == 3
    assert next(iter2) == 2
    assert lst1._strict == [1, 2, 3]
