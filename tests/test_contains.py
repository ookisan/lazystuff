from lazystuff import lazylist


def test_empty():
    act = lazylist()
    assert 1 not in act

def test_strict():
    act = lazylist([1, 2, 3, 4, 5])
    assert 3 in act

def test_nonstrict():
    act = lazylist(range(1, 11))
    assert 4 in act
    assert act._strict == [1, 2, 3, 4]
    assert act._is_strict() is False
