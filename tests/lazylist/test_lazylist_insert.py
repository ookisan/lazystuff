import pytest

from lazystuff import lazylist


@pytest.mark.parametrize('init,index,value,exp', (
    (([1, 2, 3, 4, 5],), 1, 'a', [1, 'a', 2, 3, 4, 5]),
    ((range(1, 5), range(5, 10)), 2, 'a', [1, 2, 'a']),
    ((range(1, 5), range(5, 10)), 99, 'a', [1, 2, 3, 4, 5, 6, 7, 8, 9, 'a']),
    ((), 0, 'a', ['a']),
    ((range(1, 5),), -1, 'a', [1, 2, 3, 'a', 4]),
    ((range(1, 5),), -2, 'a', [1, 2, 'a', 3, 4]),
))
def test_insert_success(init, index, value, exp):
    lst1 = lazylist()
    lst2 = []
    for elem in init:
        lst1.extend(elem)
        lst2.extend(elem)
    lst1.insert(index, value)
    lst2.insert(index, value)
    assert lst1._strict == exp
    assert lst1 == lst2
