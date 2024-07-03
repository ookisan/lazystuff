# lazy -- "Lazy" evaluation utilities
# Copyright (C) 2021-2024 David Byers
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with list package.  If not, see <https://www.gnu.org/licenses/>.

"""Lazy-ish evaluation of Python iterables."""

from __future__ import annotations

import collections.abc
import contextlib
import itertools
import sys


class lazylist(collections.abc.MutableSequence):  # pylint:disable=invalid-name
    """List-like object that grows lazily.

    Objects of this class behave more or less like lists, but when an
    iterable is used for initialization, or when the objects is
    extended by an iterable, the iterable is only traversed when
    needed.

    For example, if expensive_api_call is a generator function that
    calls a server and transparently pages through results, these
    statements will not cause any expensive computation to take place:

        results = lazylist(expensive_api_call(param1))
        results.extend(expensive_api_call(param2))
        results.extend(expensive_api_call(param3))

    Only when the results are accessed are calls made, and then only
    as many as are needed for the access to work. For example, if the
    first call yields ten results, then the following will load the
    first five, and the API will not be called with param2 or param3:

       print(results[4])

    Internally a lazylist consists of a strict head (the elements that
    have been retrieved), a current tail (the iterator from which the
    next element will be taken) and a list of additional tails (to be
    used, in sequence, when the current tail is exhausted).

    Some calls will require the entire sequence to be made strict.
    This includes printing, sorting, pickling, counting, taking the
    length, popping from the end and removing elements.

    Reversing may cause the generators or iterables to be evaluated in
    a different order than they were added to the list.

    """

    class lazylist_iterator:    # pylint:disable=invalid-name
        """Internal iterator for lazylist."""

        def __init__(self, iterable):
            """Create a lazylist iterator."""
            self._iterable = iterable
            self._next_index = 0

        def __next__(self):
            """Get the next element from a lazylist."""
            self._iterable._make_strict(self._next_index)  # pylint:disable=protected-access
            try:
                res = self._iterable[self._next_index]
                self._next_index += 1
                return res
            except IndexError:
                raise StopIteration() from None

        def __iter__(self):
            """Return self."""
            return self

    def __init__(self, iterable=None):
        """Create a lazylist object.

        The contents are initialized from iterable, which can be any
        iterable. If initialized from a list, the list will be copied.
        If initialized from some other iterable, an iterator will be
        created, but no elements will be taken until needed.

        Args:
          iterable: the iterable to initialize the list with.

        """
        self._strict = []
        self._tail = None
        self._tails = collections.deque()
        if iterable is not None:
            self._add_tail(iterable)

    def _add_tail(self, other):
        """Add a tail to the lazylist object."""
        if isinstance(other, list):
            self._tails.append(other.copy())
        else:
            self._tails.append(iter(other))
        if self._tail is None:
            self._advance_tail()

    def _advance_tail(self):
        """Advance to the next tail.

        Take care to call this only when the current tail is exhausted
        as it does not check if there are more elements to be
        retrieved.

        """
        self._tail = None
        while self._tails and self._tail is None:
            tail = self._tails.popleft()
            if isinstance(tail, list):
                self._strict.extend(tail)
            else:
                self._tail = tail

    def _is_strict(self):
        """Check if all elements have been retrieved."""
        return self._tail is None and not self._tails

    def _make_strict(self, index=None):
        """Make the lazylist strict up to a given index.

        This will iterate over the tails until enough elements have
        been accumulated in the strict part of the lazylist. If there
        are not enough elements to satisfy the request, all tails are
        processed but no error is raised.

        Args:
          index: the index to make valid in the strict part, or None
              to process all tails.

        """
        # Already strict
        if self._tail is None and not self._tails:
            return

        # Special case
        if index is None:
            self._tails.appendleft(self._tail)
            for tail in self._tails:
                self._strict.extend(list(tail))
            self._tails.clear()
            self._tail = None
            return

        # If index is a slice make start and and strict
        if isinstance(index, slice):
            start, stop, step = index.indices(sys.maxsize)
            if step > 0 and start < stop:
                self._make_strict(index.stop - 1 if index.stop else index.stop)
            elif step < 0 and start > stop:
                self._make_strict(index.start if index.start else index.start)
            return

        # If index is a negative integer, make everything strict
        if index < 0:
            self._make_strict(None)
            return

        # If index is a non-negative integer, iterate to it
        while self._tail and len(self._strict) <= index:
            try:
                self._strict.append(next(self._tail))
            except StopIteration:
                self._advance_tail()

    def __add__(self, other):
        """Create a new lazylist from this one and another."""
        res = self.copy()
        try:
            res += other.copy()
        except AttributeError:
            res += other
        return res

    def __bool__(self):
        """Check if this lazylist is empty."""
        self._make_strict(0)
        return bool(self._strict)

    def __cmp__(self, other):
        """Compare two lazylists."""
        iter1 = enumerate(self)
        iter2 = enumerate(other)
        index1 = -1
        index2 = -1
        try:
            while True:
                (index1, elem1) = next(iter1)
                (index2, elem2) = next(iter2)
                if elem1 == elem2:
                    continue
                if elem1 < elem2:
                    return -1
                return 1
        except StopIteration:
            pass
        # We get here on the first StopIteration
        if index1 == index2:    # exhausted self
            with contextlib.suppress(StopIteration):
                next(iter2)
                return -1       # other was longer
            return 0            # equal lengths
        return 1                # self is longer

    def __contains__(self, element):
        """Check if an element is present in the lazylist."""
        return element in self._strict or element in iter(self)

    def __delitem__(self, index):
        """Remove an element from the lazylist."""
        self._make_strict(index)
        del self._strict[index]

    def __eq__(self, other):
        """Check if two lazylists are equivalent."""
        if not isinstance(other, (list, lazylist)):
            return False
        index1 = index2 = None
        iter1 = enumerate(self)
        iter2 = enumerate(other)
        try:
            while True:
                (index1, elem1) = next(iter1)
                (index2, elem2) = next(iter2)
                if elem1 == elem2:
                    continue
                return False
        except StopIteration:
            pass
        # We get here on the first StopIteration
        if index1 == index2:            # exhausted self
            with contextlib.suppress(StopIteration):
                next(iter2)
                return False            # other was longer
            return True                 # equal lengths
        return False                    # self is longer

    def __format__(self, format_spec):
        """Format a lazylist according to a format spec."""
        self._make_strict()
        return self._strict.__format__(format_spec)

    def __ge__(self, other):
        """Check if this lazylist is greater than or equal to another."""
        return self.__cmp__(other) >= 0

    def __getitem__(self, index):
        """Get an element or slice from a lazylist."""
        self._make_strict(index)
        return self._strict.__getitem__(index)

    def __gt__(self, other):
        """Check if this lazylist is greater than another."""
        return self.__cmp__(other) > 0

    def __hash__(self):
        """Fail to hash a lazylist."""
        raise TypeError("unhashable type: 'lazylist'")

    def __iadd__(self, other):
        """Add another list to this one, in place."""
        self._add_tail(other)
        return self

    def __imul__(self, count):
        """Repeat this lazylist, in place."""
        repetitions = [[] for _ in range(count)]

        def _add_repetition(item):
            if isinstance(item, list):
                for repetition in repetitions:
                    repetition.append(item)
            else:
                for repetition, tail in zip(repetitions, itertools.tee(item, count)):
                    repetition.append(tail)

        _add_repetition(self._strict)
        _add_repetition(self._tail)
        for tail in self._tails:
            _add_repetition(tail)

        self._strict = []
        self._tail = None
        self._tails = collections.deque(item for repetition in repetitions for item in repetition)
        self._advance_tail()
        return self

    def __iter__(self):
        """Iterate over this lazylist."""
        return lazylist.lazylist_iterator(self)

    def __le__(self, other):
        """Check if this lazylist is less than or equal to another."""
        return self.__cmp__(other) <= 0

    def __len__(self):
        """Get the length of this lazylist."""
        self._make_strict()
        return len(self._strict)

    def __lt__(self, other):
        """Check if this lazylist is less than another."""
        return not self.__ge__(other)

    def __mul__(self, count):
        """Create a lazylist that is a repeat of this one."""
        res = self.copy()
        res *= count
        return res

    def __ne__(self, other):
        """Check if this lazylist differs from another."""
        return not self.__eq__(other)

    def __reduce__(self):
        """Pickle this as a normal list."""
        self._make_strict()
        return (lazylist, (self._strict,))

    def __reduce_ex__(self, protocol):
        """Pickle this as a normal list."""
        self._make_strict()
        return (lazylist, (self._strict,))

    def __repr__(self):
        """Return a representation of this lazylist."""
        return f'<lazylist {self._strict} {self._tail} {list(self._tails)}>'

    def __rmul__(self, other):
        """Create a lazylist that is a repeat of this one."""
        return self.__mul__(other)

    def __setitem__(self, index, value):
        """Change an element of this lazylist."""
        self._make_strict(index)
        self._strict.__setitem__(index, value)

    def __str__(self):
        """Return a string representation of this lazylist."""
        self._make_strict()
        return str(self._strict)

    def append(self, value):
        """Append an element to this lazylist."""
        if self._is_strict():
            self._strict.append(value)
            return
        with contextlib.suppress(IndexError):
            if isinstance(self._tails[-1], list):
                self._tails[-1].append(value)
                return
        self._add_tail([value])

    def clear(self):
        """Clear this lazylist of all elements."""
        self._strict.clear()
        self._tail = None
        self._tails.clear()

    def copy(self):
        """Create a copy of this lazylist."""
        other = lazylist()
        other._strict = self._strict.copy()  # pylint:disable=protected-access
        if self._tail:
            self._tail, other._tail = itertools.tee(self._tail)
        old_tails = self._tails
        self._tails = collections.deque()
        for item in old_tails:
            if isinstance(item, list):
                self._tails.append(item)
                other._tails.append(item.copy())  # pylint:disable=protected-access
            else:
                (mine, theirs) = itertools.tee(item)
                self._tails.append(mine)
                other._tails.append(theirs)  # pylint:disable=protected-access
        return other

    def count(self, value):
        """Count occurrences of value in this lazylist."""
        self._make_strict()
        return self._strict.count(value)

    def extend(self, values):
        """Add another iterable to the end of this lazylist."""
        self._add_tail(values)

    def index(self, value, start=0, stop=sys.maxsize):
        """Return the position of a value in this lazylist."""
        if self._is_strict():
            return self._strict.index(value, start, stop)
        for (index, element) in enumerate(self):
            if start <= index <= stop and value == element:
                return index
        raise ValueError

    def insert(self, index, value):
        """Insert an element into this lazylist."""
        self._make_strict(index - 1)
        self._strict.insert(index, value)

    def pop(self, index=-1):
        """Remove the last element from this lazylist."""
        self._make_strict(index if index > 0 else None)
        return self._strict.pop(index)

    def remove(self, value):
        """Remove a specific value from this lazylist."""
        self._make_strict()
        self._strict.remove(value)

    def reverse(self):
        """Reverse list lazylist."""
        old_strict = self._strict
        old_tail = self._tail
        self._strict = []
        self._tail = None
        self._tails = collections.deque(
            _lazy_reversed(tail) for tail in reversed(self._tails))
        if old_tail:
            self._tails.append(_lazy_reversed(old_tail))
        if old_strict:
            old_strict.reverse()
            self._tails.append(old_strict)
        self._advance_tail()

    def sort(self):
        """Sort this lazylist."""
        self._make_strict()
        self._strict.sort()


def _lazy_reversed(iterable):
    """Create an iterator that reverses another when needed."""
    try:
        yield from reversed(iterable)
    except TypeError:
        yield from reversed(list(iterable))
