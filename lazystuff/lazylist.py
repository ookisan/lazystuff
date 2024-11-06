# lazystuff -- "Lazy" data structures for Python
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
# along with this package.  If not, see <https://www.gnu.org/licenses/>.

"""Lazy-ish list-like data structure."""

from __future__ import annotations

import collections.abc
import contextlib
import itertools
import sys
import typing

_T = typing.TypeVar('_T')

if typing.TYPE_CHECKING:
    from typing import (
        Any,
        Generator,
        Iterable,
        Iterator,
        Literal,
        Self,
        SupportsIndex
    )  # pragma: no coverage


__all__ = (
    'lazylist',
)


class lazylist(collections.abc.MutableSequence[_T]):  # pylint:disable=invalid-name
    """List-like object that grows lazily.

    Objects of this class behave more or less like lists, but when an
    iterable is used for initialization, or when the objects is
    extended by an iterable, the iterable is only traversed when
    needed.

    When a :py:class:`lazylist` is extended with an iterable other
    than a regular list, evaluation of the iterable is deferred until
    it is needed, and is limited to the number of elements required.
    The elements that are fetched from the iterator(s) are stored as a
    regular list inside the :py:class:`lazylist`.

    Iteration only takes place when an element is requested. For
    example:

    * When checking if the list is empty (or non-empty), a single
      element is fetched.
    * When indexing the list using a positive number, elements are
      fetched until the requested index is reached.
    * When the :py:meth:`index` method is called, elements are fetched
      until the requested value is found.

    There are situations when all iterators are exhausted, including:

    * When the length of the list is requested.
    * When using the `in` operator and the value is not in the list.
    * When calling :py:meth:`index` with a value that is not in the
      list.
    * When the list is printed (all elements are printed).
    * When the list is indexed with a negative number.
    * When the :py:meth:`remove`, :py:meth:`count`, or :py:meth:`sort`
        methods are called.
    * When equal lists are compared.
    * When the list is pickled.

    For example, a :py:meth:`lazylist` can represent an infinite
    sequence::

        all_squares = lazylist(x * x for x in itertools.count())
        print(squares[99])  # Only iterates 100 times

    Multiple sequences can be added to a lazylist and regular lists
    and iterators can be mixed::

        >>> example = lazylist(['a', 'b', 'c'])
        >>> example.extend(range(1, 4))
        >>> example.extend(string.ascii_lowercase[3:6])
        >>> print(example[3])
        1
        >>> del example[6]
        >>> print(example)
        ['a', 'b', 'c', 1, 2, 3, 'e', 'f']

    When the list is indexed with 3, a single element is fetched from
    the range iterator. When element 6 is deleted, the range iterator
    is exhausted and a single element is fetched from the string
    iterator in order to reach the element at index 6. Finally, the
    string iterator is also exhausted when the list is printed. The
    :py:func:`repr` function to see the current status of the list::

        >>> example = lazylist(['a', 'b', 'c'])
        >>> example.extend(range(1, 4))
        >>> example.extend(string.ascii_lowercase[3:6])
        >>> repr(example)
        "<lazylist ['a', 'b', 'c'] [<range_iterator ...> <str_ascii_iterator ...>]>"
        >>> print(example[3])
        1
        >>> repr(example)
        "<lazylist ['a', 'b', 'c', 1] [<range_iterator ...> <str_ascii_iterator ...>]>"
        >>> del example[6]
        >>> repr(example)
       "<lazylist ['a', 'b', 'c', 1, 2, 3] [<str_ascii_iterator object at ...>]>"
        >>> print(example)
        ['a', 'b', 'c', 1, 2, 3, 'e', 'f']
        >>> repr(example)
        "<lazylist ['a', 'b', 'c', 1, 2, 3, 'e', 'f'] []>"

    The representation contains two elements: first the list of list
    elements that have been fetched from the iterators and second the
    list of iterators and regular lists that have been added to the
    :py:class:`lazylist`.

    """

    class _lazylist_iterator(typing.Iterator[_T]):    # pylint:disable=invalid-name
        """Internal iterator for lazylist."""

        _iterable: lazylist[_T]
        _next_index: int

        def __init__(self, iterable: lazylist[_T]) -> None:
            """Create a lazylist iterator."""
            self._iterable = iterable
            self._next_index = 0

        def __next__(self) -> _T:
            """Get the next element from a lazylist."""
            self._iterable._make_strict(self._next_index)  # pylint:disable=protected-access
            try:
                res = self._iterable[self._next_index]
                self._next_index += 1
                return res
            except IndexError:
                raise StopIteration() from None

        def __iter__(self) -> Self:
            """Return self."""
            return self

    _strict: list[_T]
    _tails: collections.deque[Iterator[_T] | list[_T]]

    def __init__(self, iterable: Iterable[_T] | None = None) -> None:
        """Create a lazylist object.

        The contents are initialized from iterable, which can be any
        iterable. If initialized from a list, the list will be copied.
        If initialized from some other iterable, an iterator will be
        created, but no elements will be taken until needed.

        Args:
          iterable: the iterable to initialize the list with.

        """
        self._strict = []
        self._tails = collections.deque()
        if iterable is not None:
            self._add_tail(iterable)

    def _add_tail(self, other: Iterable[_T]) -> None:
        """Add a tail to the lazylist object."""
        if isinstance(other, list):
            self._tails.append(other.copy())
        else:
            self._tails.append(iter(other))
        self._advance_tail()

    def _advance_tail(self) -> None:
        """Advance to the next tail.

        Take care to call this only when the current tail is exhausted
        as it does not check if there are more elements to be
        retrieved.

        """
        while self._tails and isinstance(self._tails[0], list):
            self._strict.extend(self._tails.popleft())

    def _is_strict(self) -> bool:
        """Check if all elements have been retrieved."""
        return not self._tails

    def _make_strict(self, index: SupportsIndex | slice | None = None) -> None:
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
        if not self._tails:
            return

        # Special case
        if index is None:
            for tail in self._tails:
                self._strict.extend(list(tail))
            self._tails.clear()
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
        index_value = index.__index__()
        if index_value < 0:
            self._make_strict()
            return

        # If index is a non-negative integer, iterate to it
        while self._tails and len(self._strict) <= index_value:
            try:
                self._strict.append(next(self._tails[0]))  # type: ignore[arg-type]
            except StopIteration:
                self._tails.popleft()
                self._advance_tail()

    def __add__(self, other: Iterable[_T]) -> lazylist[_T]:
        """Create a new lazylist from this one and another."""
        res = self.copy()
        try:
            res += other.copy()  # type: ignore[attr-defined]
        except AttributeError:
            res += other
        return res

    def __bool__(self) -> bool:
        """Check if this lazylist is empty."""
        self._make_strict(0)
        return bool(self._strict)

    def __cmp__(self, other: Any) -> Literal[-1, 0, 1]:
        """Compare two lazylists."""
        if not isinstance(other, (list, lazylist)):
            raise TypeError(f"comparison not supported between instances of 'lazylist' "
                            f"and '{type(other).__name__}'")
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

    def __contains__(self, element: Any) -> bool:
        """Check if an element is present in the lazylist."""
        return element in self._strict or element in iter(self)

    def __delitem__(self, index: SupportsIndex | slice) -> None:
        """Remove an element from the lazylist."""
        self._make_strict(index)
        del self._strict[index]

    def __eq__(self, other: Any) -> bool:
        """Check if two lazylists are equivalent."""
        if not isinstance(other, (list, lazylist)):
            return False
        return self.__cmp__(other) == 0

    def __format__(self, format_spec: str) -> str:
        """Format a lazylist according to a format spec."""
        self._make_strict()
        return self._strict.__format__(format_spec)

    def __ge__(self, other: Any) -> bool:
        """Check if this lazylist is greater than or equal to another."""
        return self.__cmp__(other) >= 0

    @typing.overload
    def __getitem__(self, index: SupportsIndex) -> _T:  # noqa: D105;
        ...                                             # pragma: no cover

    @typing.overload
    def __getitem__(self, index: slice) -> list[_T]:  # noqa: D105;
        ...                                           # pragma: no cover

    def __getitem__(self, index: SupportsIndex | slice) -> _T | list[_T]:
        """Get an element or slice from a lazylist."""
        self._make_strict(index)
        return self._strict[index]

    def __gt__(self, other: Any) -> bool:
        """Check if this lazylist is greater than another."""
        return self.__cmp__(other) > 0

    def __hash__(self) -> int:
        """Fail to hash a lazylist."""
        raise TypeError("unhashable type: 'lazylist'")

    def __iadd__(self, other: Iterable[_T]) -> Self:
        """Add another list to this one, in place."""
        self._add_tail(other)
        return self

    def __imul__(self, count: int) -> Self:
        """Repeat this lazylist, in place."""
        repetitions: list[list[list[_T] | Iterator[_T]]] = [[] for _ in range(count)]

        def _add_repetition(item: list[_T] | Iterator[_T]) -> None:
            if isinstance(item, list):
                for repetition in repetitions:
                    repetition.append(item)
            else:
                for repetition, tail in zip(repetitions, itertools.tee(item, count)):
                    repetition.append(tail)

        _add_repetition(self._strict)
        for tail in self._tails:
            _add_repetition(tail)

        self._strict = []
        self._tails = collections.deque(item for repetition in repetitions for item in repetition)
        self._advance_tail()
        return self

    def __iter__(self) -> Iterator[_T]:
        """Iterate over this lazylist."""
        return lazylist._lazylist_iterator(self)

    def __le__(self, other: Any) -> bool:
        """Check if this lazylist is less than or equal to another."""
        return self.__cmp__(other) <= 0

    def __len__(self) -> int:
        """Get the length of this lazylist."""
        self._make_strict()
        return len(self._strict)

    def __lt__(self, other: Any) -> bool:
        """Check if this lazylist is less than another."""
        return not self.__ge__(other)

    def __mul__(self, count: int) -> lazylist[_T]:
        """Create a lazylist that is a repeat of this one."""
        res = self.copy()
        res *= count
        return res

    def __ne__(self, other: Any) -> bool:
        """Check if this lazylist differs from another."""
        return not self.__eq__(other)

    def __reduce__(self) -> tuple[type, tuple[list[_T]]]:
        """Pickle this as a normal list."""
        self._make_strict()
        return (lazylist, (self._strict,))

    def __reduce_ex__(self, protocol: SupportsIndex) -> tuple[type, tuple[list[_T]]]:
        """Pickle this as a normal list."""
        self._make_strict()
        return (lazylist, (self._strict,))

    def __repr__(self) -> str:
        """Return a representation of this lazylist."""
        return f'<lazylist {self._strict} {list(self._tails)}>'

    def __rmul__(self, other: int) -> lazylist[_T]:
        """Create a lazylist that is a repeat of this one."""
        return self.__mul__(other)

    @typing.overload
    def __setitem__(self, index: SupportsIndex, value: _T) -> None:  # noqa: D105;
        ...                                                          # pragma: no cover

    @typing.overload
    def __setitem__(self, index: slice, value: Iterable[_T]) -> None:  # noqa: D105;
        ...                                                            # pragma: no cover

    def __setitem__(self, index: SupportsIndex | slice, value: _T | Iterable[_T]) -> None:
        """Change an element of this lazylist."""
        self._make_strict(index)
        self._strict[index] = value  # type: ignore[index,assignment]

    def __str__(self) -> str:
        """Return a string representation of this lazylist."""
        self._make_strict()
        return str(self._strict)

    def append(self, value: _T) -> None:
        """Append an element to this lazylist."""
        if self._is_strict():
            self._strict.append(value)
            return
        with contextlib.suppress(IndexError):
            if isinstance(self._tails[-1], list):
                self._tails[-1].append(value)
                return
        self._add_tail([value])

    def clear(self) -> None:
        """Clear this lazylist of all elements."""
        self._strict.clear()
        self._tails.clear()

    def copy(self) -> lazylist[_T]:
        """Create a copy of this lazylist."""
        other: lazylist[_T] = lazylist()
        other._strict = self._strict.copy()  # pylint:disable=protected-access
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

    def count(self, value: Any) -> int:
        """Count occurrences of value in this lazylist."""
        self._make_strict()
        return self._strict.count(value)

    def extend(self, values: Iterable[_T]) -> None:
        """Add another iterable to the end of this lazylist."""
        self._add_tail(values)

    def index(self, value: Any, start: int = 0, stop: int = sys.maxsize) -> int:
        """Return the position of a value in this lazylist."""
        if self._is_strict():
            return self._strict.index(value, start, stop)
        for (index, element) in enumerate(self):
            if start <= index <= stop and value == element:
                return index
        raise ValueError

    def insert(self, index: int, value: _T) -> None:
        """Insert an element into this lazylist."""
        self._make_strict(index - 1)
        self._strict.insert(index, value)

    def pop(self, index: int = -1) -> _T:
        """Remove the last element from this lazylist."""
        self._make_strict(index if index > 0 else None)
        return self._strict.pop(index)

    def remove(self, value: Any) -> None:
        """Remove a specific value from this lazylist."""
        self._make_strict()
        self._strict.remove(value)

    def reverse(self) -> None:
        """Reverse list lazylist."""
        old_strict = self._strict
        self._strict = []
        self._tails = collections.deque(
            _lazy_reversed(tail) for tail in reversed(self._tails))
        if old_strict:
            old_strict.reverse()
            self._tails.append(old_strict)
        self._advance_tail()

    def sort(self) -> None:
        """Sort this lazylist."""
        self._make_strict()
        self._strict.sort()


def _lazy_reversed(iterable: Iterable[_T]) -> Generator[_T, None, None]:
    """Create an iterator that reverses another when needed."""
    try:
        yield from reversed(iterable)  # type: ignore[call-overload]
    except TypeError:
        yield from reversed(list(iterable))
