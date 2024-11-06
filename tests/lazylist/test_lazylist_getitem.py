import pytest

from lazystuff import lazylist


@pytest.mark.parametrize('init,idx,exp,strict', [
    ([range(1, 5)], 0, 1, [1]),
    ([range(1, 5)], 3, 4, [1, 2, 3, 4]),
    ([range(1, 5)], -1, 4, [1, 2, 3, 4]),
    ([range(1, 5)], -4, 1, [1, 2, 3, 4]),
    ([range(1, 5), [5, 6, 7], range(8, 10)], 5, 6, [1, 2, 3, 4, 5, 6, 7]),
    ([range(1, 5), [5, 6, 7], range(8, 10)], 7, 8, [1, 2, 3, 4, 5, 6, 7, 8]),
])
def test_getitem_success(init, idx, exp, strict):
    lst1 = lazylist()
    lst2 = []
    for elem in init:
        lst1.extend(elem)
        lst2.extend(elem)
    act = lst1[idx]
    assert act == exp
    assert act == lst2[idx]
    assert lst1._strict == strict

@pytest.mark.parametrize('init,idx1,idx2,step,exp,strict', [
    ([range(1, 5)], None, 2, None, [1, 2], [1, 2]),
    ([range(1, 5)], 2, None, None, [3, 4], [1, 2, 3, 4]),
    ([range(1, 5)], 1, 3, None, [2, 3], [1, 2, 3]),
    ([range(1, 5)], None, -1, None, [1, 2, 3], [1, 2, 3, 4]),
    ([range(1, 5)], -3, -1, None, [2, 3], [1, 2, 3, 4]),
    ([range(1, 5)], -2, -4, -1, [3, 2], [1, 2, 3, 4]),
    ([range(1, 5), [5, 6, 7], range(8, 10)], 2, 8, None, [3, 4, 5, 6, 7, 8],
     [1, 2, 3, 4, 5, 6, 7, 8]),
    ([range(1, 5), [5, 6, 7], range(8, 10)], 8, 2, -2, [9, 7, 5],
     [1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ([range(1, 5)], 2, 100, None, [3, 4], [1, 2, 3, 4]),
    ([range(1, 10)], 4, 4, None, [], []),
    ([range(1, 10)], 5, 4, None, [], []),
    ([range(1, 10)], 4, 5, -1, [], []),
])
def test_getitem_slice(init, idx1, idx2, step, exp, strict):
    lst1 = lazylist()
    lst2 = []
    for elem in init:
        lst1.extend(elem)
        lst2.extend(elem)
    act = lst1[idx1:idx2:step]
    assert act == exp
    assert act == lst2[idx1:idx2:step]
    assert lst1._strict == strict

@pytest.mark.parametrize('init,idx,strict', [
    ([range(1, 5)], 4, [1, 2, 3, 4]),
    ([range(1, 5)], -5, [1, 2, 3, 4]),
])
def test_getitem_indexerror(init, idx, strict):
    lst1 = lazylist()
    for elem in init:
        lst1.extend(elem)
    with pytest.raises(IndexError):
        _ = lst1[idx]
    assert lst1._strict == strict
