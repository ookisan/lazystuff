from lazystuff import lazylist


def test_mul_basic():
    lst1 = lazylist([1, 2])
    lst1.extend(range(3, 5))
    lst1.extend(range(5, 7))
    act = lst1 * 3
    assert act is not lst1
    assert act._strict == [1, 2]
    assert list(act) == [1, 2, 3, 4, 5, 6] * 3
