import pytest

from lazystuff import lazylist


@pytest.mark.parametrize('init,index,exp,exp_strict', (
    (([1, 2, 3, 4, 5],), None, 5, None),
    ((range(1, 5), range(5, 10)), None, 9, None),
    ((range(1, 5), range(5, 10)), -2, 8, None),
    ((range(1, 5), range(5, 10)), 0, 1, []),
    ((range(1, 5), range(5, 10)), 1, 2, [1]),
))
def test_pop_success(init, index, exp, exp_strict):
    lst1 = lazylist()
    lst2 = []
    for elem in init:
        lst1.extend(elem)
        lst2.extend(elem)
    if index is not None:
        act = lst1.pop(index)
        ref = lst2.pop(index)
    else:
        act = lst1.pop()
        ref = lst2.pop()

    assert act == ref
    assert act == exp
    if exp_strict:
        assert lst1._strict == exp_strict
    else:
        assert lst1._is_strict()
    assert lst1 == lst2



@pytest.mark.parametrize('init,index', (
    ((), None),
    ((range(5),), 99),
    ((range(5),), -99),
    (([1],), 1),
    (([1],), -2),
))
def test_pop_error(init, index):
    lst1 = lazylist()
    lst2 = []
    for elem in init:
        lst1.extend(elem)
        lst2.extend(elem)
    if index is not None:
        with pytest.raises(IndexError):
            act = lst1.pop(index)
        with pytest.raises(IndexError):
            ref = lst2.pop(index)
    else:
        with pytest.raises(IndexError):
            act = lst1.pop()
        with pytest.raises(IndexError):
            ref = lst2.pop()
    assert lst1 == lst2
