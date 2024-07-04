from lazystuff import lazylist


def test_str_basic():
    lst = lazylist(range(1, 5))
    assert str(lst) == '[1, 2, 3, 4]'
