import pytest

from lazystuff import lazylist


@pytest.mark.parametrize('init,exp,strict', (
    ([range(1, 5)], 4, [1, 2, 3, 4]),
    ([range(1, 5), range(5, 10)], 9, [1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ([range(1, 5), ['a', 'b'], range(5, 10)], 11, [1, 2, 3, 4, 'a', 'b', 5, 6, 7, 8, 9]),
))
def test_len_basic(init, exp, strict):
    lst1 = lazylist()
    for elem in init:
        lst1.extend(elem)
    assert len(lst1) == exp
    assert lst1._strict == strict
