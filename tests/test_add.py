from lazystuff import lazylist


def test_add_list():
    left = lazylist([1, 2, 3])
    right = lazylist([4, 5, 6])
    act = left + right
    assert act is not left
    assert act is not right
    assert list(act) == [1, 2, 3, 4, 5, 6]
    assert list(left) == [1, 2, 3]
    assert list(right) == [4, 5, 6]

def test_add_list():
    left = lazylist([1, 2, 3])
    right = iter([4, 5, 6])
    act = left + right
    assert act is not left
    assert act is not right
    assert list(act) == [1, 2, 3, 4, 5, 6]
    assert list(left) == [1, 2, 3]

def test_add_lazylist():
    lst1 = lazylist(range(1, 5))
    lst2 = lazylist(range(5, 10))
    act = lst1 + lst2
    assert act is not lst1
    assert act is not lst2
    assert act._strict == []
    assert list(act) == list(range(1, 10))

def test_add_and_delete():
    lst1 = lazylist(range(1, 5))
    lst2 = lazylist(range(5, 10))
    act = lst1 + lst2
    del lst1[:]
    del lst2[:]
    assert list(act) == list(range(1, 10))

def test_add_complex():
    lst1 = act = lazylist(range(1, 5))
    lst1.extend(range(5, 7))
    lst1.extend([7, 8, 9])
    lst2 = lazylist(iter(['a', 'b', 'c']))
    lst2.extend(iter(['d', 'e']))
    lst2.extend(iter(['f', 'g', 'h']))
    act = lst1 + lst2
    assert act is not lst1
    assert act is not lst2
    assert list(act) == [1, 2, 3, 4, 5, 6, 7, 8, 9,
                         'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    assert list(lst2) == [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
