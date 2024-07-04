import re

from lazystuff import lazylist


def test_repr_basic():
    lst = lazylist([1, 2])
    lst.extend(range(3, 5))
    lst.extend([5, 6])
    act = repr(lst)
    assert re.match(r'<lazylist \[1, 2\] \[<range_iterator object at 0x[a-f0-9]+>, \[5, 6\]\]>',
                    act)
