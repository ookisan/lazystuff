from lazystuff import lazylist


def test_format():
    assert f'{lazylist(range(1, 4))}' == '[1, 2, 3]'
