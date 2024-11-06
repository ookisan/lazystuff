import pytest

from lazystuff import lazylist


@pytest.mark.parametrize('init,val,exp', (
    ([range(1, 5)], 5, []),
    ([[1, 2, 3, 4]], 5, [1, 2, 3, 4, 5]),
))
def test_append_basic(init, val, exp):
    lst1 = lazylist()
    lst2 = []
    for elem in init:
        lst1.extend(elem)
        lst2.extend(elem)
    lst1.append(val)
    lst2.append(val)
    assert lst1._strict == exp
    assert list(lst1) == lst2

def test_append_to_empty():
    lst1 = lazylist()
    lst1.append(1)
    assert lst1._strict == [1]

def test_append_to_lazy():
    lst1 = lazylist(range(1, 5))
    lst1.append(5)
    assert lst1._strict == []
    assert len(lst1._tails) == 2
    assert lst1._tails[1] == [5]

def test_append_to_lazy_multi():
    lst1 = lazylist(range(1, 5))
    lst1.append(5)
    assert lst1._strict == []
    assert len(lst1._tails) == 2
    act = lst1._tails[0]
    lst1.append(6)
    assert len(lst1._tails) == 2
    assert lst1._tails[0] is act
    assert lst1._tails[1] == [5, 6]
