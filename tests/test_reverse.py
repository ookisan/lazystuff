import pytest

from lazystuff import lazylist


@pytest.mark.parametrize('init', (
    ([5, 4, 3, 2, 1],),
    ([5, 4, 3, 2, 1], range(10, 1, -1)),
    (range(1, 5), range(5, 10)),
    (range(1, 5), [6, 4, 9, 0, 1], range(80, 90),),
    (),
))
def test_reverse_success(init):
    lst1 = lazylist()
    lst2 = []
    for elem in init:
        lst1.extend(elem)
        lst2.extend(elem)
    before_strict = lst1._is_strict()
    lst1.reverse()
    lst2.reverse()
    after_strict = lst1._is_strict()
    assert before_strict is after_strict
    assert lst1 == lst2
