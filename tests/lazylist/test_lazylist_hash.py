import pytest

from lazystuff import lazylist


def test_hash():
    lst = lazylist()
    with pytest.raises(TypeError):
        {}[lst] = None
