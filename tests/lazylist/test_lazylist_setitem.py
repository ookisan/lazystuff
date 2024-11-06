import pytest

from lazystuff import lazylist


@pytest.mark.parametrize('init,idx,val,exp', [
    ([range(1, 5)], 0, 'a', ['a']),
    ([range(1, 5)], 3, 'b', [1, 2, 3, 'b']),
    ([range(1, 5)], -1, 'c', [1, 2, 3, 'c']),
    ([range(1, 5)], -4, 'd', ['d', 2, 3, 4]),
    ([range(1, 5), [5, 6, 7], range(8, 10)], 5, 'e', [1, 2, 3, 4, 5, 'e', 7]),
    ([range(1, 5), [5, 6, 7], range(8, 10)], 7, 'f', [1, 2, 3, 4, 5, 6, 7, 'f']),
])
def test_getitem_success(init, idx, val, exp):
    lst1 = lazylist()
    lst2 = []
    for elem in init:
        lst1.extend(elem)
        lst2.extend(elem)

    assert lst1[idx] != val
    lst1[idx] = val
    lst2[idx] = val
    assert lst1[idx] == val
    assert lst1._strict == exp
    assert list(lst1) == lst2

@pytest.mark.parametrize('init,idx1,idx2,step,val,exp', [
    ([range(1, 10)], None, 2, None, ['a', 'b'], ['a', 'b']),
    ([range(1, 10)], 2, 4, None, ['a', 'b'], [1, 2, 'a', 'b']),
    ([range(1, 10)], 2, 4, None, [], [1, 2]),
    ([range(1, 10)], 2, 6, None, ['a'], [1, 2, 'a']),
    ([range(1, 10)], 4, 2, -1, ['a', 'b'], [1, 2, 3, 'b', 'a']),
    ([range(1, 5), [5, 6, 7], range(8, 10)], 2, 8, None, ['a', 'b', 'c'],
     [1, 2, 'a', 'b', 'c']),
])
def test_getitem_slice(init, idx1, idx2, step, val, exp):
    lst1 = lazylist()
    lst2 = []
    for elem in init:
        lst1.extend(elem)
        lst2.extend(elem)
    lst1[idx1:idx2:step] = val
    lst2[idx1:idx2:step] = val
    assert lst1._strict == exp
    assert list(lst1) == lst2

@pytest.mark.parametrize('init,idx,strict', [
    ([range(1, 5)], 4, [1, 2, 3, 4]),
    ([range(1, 5)], -5, [1, 2, 3, 4]),
])
def test_getitem_indexerror(init, idx, strict):
    lst1 = lazylist()
    for elem in init:
        lst1.extend(elem)
    with pytest.raises(IndexError):
        lst1[idx] = None
    assert lst1._strict == strict
