import random

import pytest

from lazystuff import lazylist


@pytest.mark.parametrize('init', (
    ((range(10, 1, -1),),),
    ((range(1, 10),),),
    ((),),
))
def test_sort_success(init):
    lst1 = lazylist()
    lst2 = []
    for elem in init:
        lst1.extend(elem)
        lst2.extend(elem)


def test_sort_random():
    random.seed(0)              # For less randomness
    numbers = list(range(100))
    for _ in range(100):
        lst1 = lazylist()
        lst2 = []
        elements = random.choices((range, list), k=random.randint(1, 10))
        for element in elements:
            if element == list:
                element = random.choices(numbers, k=random.randint(1, 10))
            elif element == range:
                start = random.randint(0, 100)
                stop = random.randint(start + 1, start + 30)
                element = range(start, stop)
            else:
                assert False
            lst1.extend(element)
            lst2.extend(element)
            lst1.sort()
            lst2.sort()
            assert lst1 == lst2
