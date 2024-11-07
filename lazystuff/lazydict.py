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
import typing

_K = typing.TypeVar('_K', bound=typing.Hashable)
_V = typing.TypeVar('_V')

if typing.TYPE_CHECKING:
    from typing import (
        Any,
        Callable,
        ItemsView,
        Iterable,
        Iterator,
        KeysView,
        ValuesView,
    )  # pragma: no coverage


__all__ = (
    'lazydict',
)


class lazydict(collections.abc.MutableMapping[_K, _V]):  # pylint:disable=invalid-name
    """Dict-like object where computation of values can be deferred.

    Objects of this class behave more or less like dictionaries, but
    when initialized or updated from another :py:class:`lazydict` (and
    only in those cases), callable values have a special meaning: they
    will be called on first access to the associated key.

    For example::

        >>> from lazystuff import lazydict
        >>> def print_on_access(value):
        ...   def _impl():
        ...     print(f'[*] return {value}')
        ...     return value
        ...   return _impl
        ...
        >>> example = lazydict(a=print_on_access('A'), b=print_on_access('B'), c='C')
        >>> list(example)
        ['a', 'b', 'c']
        >>> example['a']
        [*] return A
        'A'
        >>> example['b']
        [*] return B
        'B'
        >>> example['c']
        'C'
        >>> example['a']
        'A'
        >>>

    Note how `print_on_access` is called the first time each key is
    accessed, but only once per key. In situations where the value is
    very expensive to calculate this makes it possible to build a data
    structure that can be used as if all values are present, but in
    reality the expensive computation is deferred until needed.

    When :py:meth:`lazydict.update` is called with a
    :py:class:`lazydict` as the argument, the deferred values will
    remain deferred. Note that in this case the callable is copied.
    When the value is accessed in one :py:class:`lazydict` instance it
    remains deferred in all others.

    """

    _resolved: dict[_K, _V]
    _unresolved: dict[_K, Callable[[], _V]]

    def _update_from_iterable(self, arg: Iterable[Any] | None, init: bool) -> None:
        """Initialize lazydict from iterable."""
        if isinstance(arg, dict):
            self._update_from_iterable(arg.items(), init)
        elif isinstance(arg, lazydict):
            self._resolved.update(arg._resolved)  # pylint:disable=protected-access
            self._unresolved.update(arg._unresolved)  # pylint:disable=protected-access
        elif arg:
            for index, item in enumerate(arg):
                elem = list(item)
                if len(elem) != 2:
                    raise ValueError(
                        f'dictionary update sequence element #{index} has '
                        f'length {len(elem)}; 2 is required')
                key, value = elem
                if callable(value):
                    if init:
                        self._unresolved[key] = value
                        self._resolved[key] = None  # type: ignore
                    else:
                        self[key] = value()
                else:
                    self[key] = value

    def _update(self, arg: Iterable[Any] | None, kwargs: dict[str, Any] | None, init: bool) -> None:
        """Update or initialize this mapping."""
        self._update_from_iterable(arg, init)
        self._update_from_iterable(kwargs, init)

    def __init__(self, /, *args: Iterable[Any], **kwargs: Any) -> None:
        """Initialize the lazydict structure.

        This method accepts the same arguments as dict(). Any values
        that are callable will be called on first access.

        """
        if len(args) > 1:
            raise TypeError(f'lazydict expected at most 1 argument, got {len(args)}')
        self._resolved = {}
        self._unresolved = {}
        self._update(args[0] if args else None, kwargs, True)

    def __getitem__(self, key: _K) -> _V:
        """Get the value of key."""
        if key in self._unresolved:
            self._resolved[key] = self._unresolved.pop(key)()
        return self._resolved[key]

    def __setitem__(self, key: _K, value: _V) -> None:
        """Set the value of a key."""
        with contextlib.suppress(KeyError):
            del self._unresolved[key]
        self._resolved[key] = value

    def __delitem__(self, key: _K) -> None:
        """Delete an element."""
        with contextlib.suppress(KeyError):
            del self._unresolved[key]
        with contextlib.suppress(KeyError):
            del self._resolved[key]

    def __iter__(self) -> Iterator[_K]:
        """Iterate over keys."""
        return iter(self._resolved)

    def __len__(self) -> int:
        """Get length of dict."""
        return len(self._resolved)

    def items(self) -> ItemsView[_K, _V]:
        """Get mapping items."""
        return collections.abc.ItemsView(self)

    def keys(self) -> KeysView[_K]:
        """Get mapping keys."""
        return collections.abc.KeysView(self)

    def values(self) -> ValuesView[_V]:
        """Get mapping values."""
        return collections.abc.ValuesView(self)

    # It does not appear to be possible to type this method correctly
    # since one of the protocols used is in _typeshed.

    def update(self, /, *args: Iterable[Any], **kwargs: Any) -> None:  # type: ignore
        """Update values from other mapping.

        When updating from another lazydict, any deferred values
        remain deferred.

        """
        if len(args) > 1:
            raise TypeError(f'update expected at most 1 argument, got {len(args)}')
        self._update(args[0] if args else None, kwargs, False)
