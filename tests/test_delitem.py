import pytest

from lazystuff import lazylist


def test_positive():
    act = lazylist(range(1, 11))
    del act[3]
    assert act._strict == [1, 2, 3]
    assert len(act._tails) == 1
    assert act[3] == 5
    assert act._strict == [1, 2, 3, 5]

def test_badindex_positive():
    act = lazylist(range(1, 11))
    with pytest.raises(IndexError):
        del act[11]
    assert act._strict == list(range(1, 11))

def test_badindex_negative():
    act = lazylist(range(1, 11))
    with pytest.raises(IndexError):
        del act[-11]
    assert act._strict == list(range(1, 11))

def test_slice_fwd():
    act = lazylist(range(1, 11))
    del act[::2]
    assert act._strict == [2, 4, 6, 8, 10]

def test_slice_rev():
    act = lazylist(range(1, 11))
    del act[10:0:-2]
    assert act._strict == [1, 3, 5, 7, 9]

def test_delall():
    act = lazylist(range(1, 11))
    act.extend([11, 12, 13])
    act.extend(range(14, 20))
    del act[:]
    assert list(act) == []
