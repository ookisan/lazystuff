from lazystuff import lazylist


def test_copy_empty():
    lst1 = lazylist()
    lst2 = lst1.copy()
    assert lst1 is not lst2
    assert lst1._strict is not lst2._strict
    assert lst1._tails is not lst2._tails

def test_copy_strict():
    lst1 = lazylist([1, 2, 3])
    lst2 = lst1.copy()
    assert lst1 is not lst2
    assert lst1._strict == [1, 2, 3]
    assert lst2._strict == [1, 2, 3]
    assert lst1._strict is not lst2._strict
    assert lst1._tails is not lst2._tails

def test_copy_complex():
    lst1 = lazylist([1, 2, 3])
    lst1.extend(range(4, 6))
    lst1.extend([6, 7, 8])
    lst1.extend(range(9, 11))
    lst2 = lst1.copy()
    assert lst1 is not lst2
    assert lst1._strict == [1, 2, 3]
    assert lst2._strict == [1, 2, 3]
    assert lst1._strict is not lst2._strict
    assert len(lst1._tails) == len(lst2._tails)
    assert not any(tail1 is tail2 for tail1, tail2 in zip(lst1._tails, lst2._tails))
    _ = list(lst2)
    assert lst1._strict == [1, 2, 3]
    assert list(lst1) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
