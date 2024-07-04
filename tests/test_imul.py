from lazystuff import lazylist


def test_imul_basic():
    lst1 = act = lazylist([1, 2])
    lst1.extend(range(3, 5))
    lst1.extend(range(5, 7))
    act *= 3
    assert act is lst1
    assert act._strict == [1, 2]
    assert list(act) == [1, 2, 3, 4, 5, 6] * 3


def test_imul_empty():
    lst1 = lazylist()
    lst1 *= 3
    assert list(lst1) == []
