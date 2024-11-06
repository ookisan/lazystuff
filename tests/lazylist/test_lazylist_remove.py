import pytest

from lazystuff import lazylist


@pytest.mark.parametrize('init,values', (
    (([1, 2, 3, 4, 5],), 3),
    ((range(1, 5), range(5, 10)), 7),
    ((range(1, 5), range(1, 5), range(1, 5)), 3),
))
def test_remove_success(init, values):
    lst1 = lazylist()
    lst2 = []
    for elem in init:
        lst1.extend(elem)
        lst2.extend(elem)
    if not isinstance(values, (list, tuple)):
        values = [values]
    for value in values:
        lst1.remove(value)
    for value in values:
        lst2.remove(value)
    assert lst1._is_strict()
    assert lst1 == lst2


@pytest.mark.parametrize('init,values', (
    ((range(5),), -1),
    ((range(5),), 5),
))
def test_remove_failure(init, values):
    lst1 = lazylist()
    lst2 = []
    for elem in init:
        lst1.extend(elem)
        lst2.extend(elem)
    if not isinstance(values, (list, tuple)):
        values = [values]
    for value in values:
        with pytest.raises(ValueError):
            lst1.remove(value)
    for value in values:
        with pytest.raises(ValueError):
            lst2.remove(value)
    assert lst1 == lst2
