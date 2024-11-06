from lazystuff import lazylist


def test_is_strict():
    act = lazylist(range(1, 11))
    assert act[9] == 10
    assert act._is_strict() is False
    assert act[-10] == 1
    assert act._is_strict() is True
