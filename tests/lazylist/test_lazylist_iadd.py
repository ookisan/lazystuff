from lazystuff import lazylist


def test_iadd_basic():
    lst1 = act = lazylist(range(1, 5))
    act += range(5, 10)
    assert act is lst1
    assert act._strict == []
    assert list(act) == list(range(1, 10))

def test_iadd_lazylist():
    lst1 = act = lazylist(range(1, 5))
    lst2 = lazylist(range(5, 10))
    act += lst2
    assert act is lst1
    assert act._strict == []
    assert list(act) == list(range(1, 10))

def test_iadd_complex():
    lst1 = act = lazylist(range(1, 5))
    lst1.extend(range(5, 7))
    lst1.extend([7, 8, 9])
    lst2 = lazylist(iter(['a', 'b', 'c']))
    lst2.extend(iter(['d', 'e']))
    lst2.extend(iter(['f', 'g', 'h']))
    act += lst2
    assert act is lst1
    assert list(act) == [1, 2, 3, 4, 5, 6, 7, 8, 9,
                         'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    assert list(lst2) == [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
