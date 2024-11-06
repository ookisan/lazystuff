from lazystuff import lazylist


def test_already_strict():
    act = lazylist(list(range(1, 11)))
    assert act._is_strict() is True
    act._make_strict(None)
    assert act._strict == list(range(1, 11))
    assert act._is_strict() is True

def test_make_strict_to_end():
    act = lazylist(range(1, 5))
    act.extend(range(5, 11))
    assert act._is_strict() is False
    act._make_strict(None)
    assert act._strict == list(range(1, 11))
    assert act._is_strict() is True

def test_make_strict_to_negative_index():
    act = lazylist(range(1, 11))
    assert act._is_strict() is False
    act._make_strict(-4)
    assert act._is_strict() is True

def test_make_strict_to_last_index():
    act = lazylist(range(1, 11))
    assert act._is_strict() is False
    act._make_strict(9)
    assert act._strict == list(range(1, 11))
    assert act._is_strict() is False

def test_make_strict_slice_fwd():
    act = lazylist(range(1, 11))
    act._make_strict(slice(2, 4, None))
    assert act._strict == [1, 2, 3, 4]
    assert act._is_strict() is False


def test_make_strict_slice_rev():
    act = lazylist(range(1, 11))
    act._make_strict(slice(4, 2, -1))
    assert act._strict == [1, 2, 3, 4, 5]
    assert act._is_strict() is False


def test_make_strict_slice_to_end_fwd():
    act = lazylist(range(1, 11))
    act._make_strict(slice(2, None, None))
    assert act._strict == list(range(1, 11))
    assert act._is_strict() is True


def test_make_strict_slice_to_end_rev():
    act = lazylist(range(1, 11))
    act._make_strict(slice(None, 2, -1))
    assert act._strict == list(range(1, 11))
    assert act._is_strict() is True


def test_make_strict_empty_slices():
    act = lazylist(range(1, 11))
    act._make_strict(slice(4, 2, None))
    act._make_strict(slice(2, 4, -1))
    act._make_strict(slice(4, 4, None))
    act._make_strict(slice(4, 4, -1))
    assert act._strict == []
    assert act._is_strict() is False

def test_make_strict_to_index():
    act = lazylist(range(1, 5))
    act.extend(range(5, 11))
    act._make_strict(5)
    assert act._strict == [1, 2, 3, 4, 5, 6]
    assert act._is_strict() is False

def test_make_strict_past_end():
    act = lazylist(range(1, 5))
    act.extend(range(5, 11))
    act._make_strict(11)
    assert act._strict == list(range(1, 11))
    assert act._is_strict() is True


def test_empty():
    act = lazylist()
    act._make_strict()
    assert act._is_strict() is True
