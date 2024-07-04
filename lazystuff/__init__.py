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

"""The :py:mod:`lazystuff` package provides lazy-ish list-like objects.

This package implements a single data type, :py:class:`lazylist`, that
behaves almost like a regular list. It has all the normal list methods
and operators and they work as expected with a single exception.

When a :py:class:`lazylist` is extended with an iterable other than a
regular list, evaluation of the iterable is deferred until it is
needed, and is limited to the number of elements required. The
elements that are fetched from the iterator(s) are stored as a regular
list inside the :py:class:`lazylist`.

Iteration only takes place when an element is requested. For example:

* When checking if the list is empty (or non-empty), a single element
  is fetched.
* When indexing the list using a positive number, elements are fetched
  until the requested index is reached.
* When the :py:meth:`index` method is called, elements are fetched
  until the requested value is found.

There are situations when all iterators are exhausted, including:

* When the length of the list is requested.
* When using the `in` operator and the value is not in the list.
* When calling :py:meth:`index` with a value that is not in the list.
* When the list is printed (all elements are printed).
* When the list is indexed with a negative number.
* When the :py:meth:`remove`, :py:meth:`count`, or :py:meth:`sort` methods are called.
* When equal lists are compared.
* When the list is pickled.

For example, a :py:meth:`lazylist` can represent an infinite sequence::

    all_squares = lazylist(x * x for x in itertools.count())
    print(squares[99])  # Only iterates 100 times

Multiple sequences can be added to a lazylist and regular lists and
iterators can be mixed::

    >>> example = lazylist(['a', 'b', 'c'])
    >>> example.extend(range(1, 4))
    >>> example.extend(string.ascii_lowercase[3:6])
    >>> print(example[3])
    1
    >>> del example[6]
    >>> repr(example)
    ['a', 'b', 'c', 1, 2, 3, 'e', 'f']

When the list is indexed with 3, a single element is fetched from the
range iterator. When element 6 is deleted, the range iterator is
exhausted and a single element is fetched from the string iterator in
order to reach the element at index 6. Finally, the string iterator is
also exhausted when the list is printed. The :py:func:`repr` function
to see the current status of the list::

    >>> example = lazylist(['a', 'b', 'c'])
    >>> example.extend(range(1, 4))
    >>> example.extend(string.ascii_lowercase[3:6])
    >>> repr(example)
    "<lazylist ['a', 'b', 'c'] <range_iterator ...> [<str_ascii_iterator ...>]>"
    >>> print(example[3])
    1
    >>> repr(example)
    "<lazylist ['a', 'b', 'c', 1] <range_iterator ...> [<str_ascii_iterator ...>]>"
    >>> del example[6]
    >>> repr(example)
   "<lazylist ['a', 'b', 'c', 1, 2, 3] <str_ascii_iterator object at ...> []>"
    >>> print(example)
    ['a', 'b', 'c', 1, 2, 3, 'e', 'f']
    >>> repr(example)
    "<lazylist ['a', 'b', 'c', 1, 2, 3, 'e', 'f'] None []>"

The first item is a list containing the elements that have been
fetched. The second item is the iterator from which elements will be
fetched next. The third item is a queue of subsequent iterables added
to the list.

:py:class:`lazylist` was originally developed to simplify streaming
results from an API to a receiver with the goal that results should be
sent to the receiver as they became available and that if the process
were aborted, no unnecessary calls to the API should have been made.

The resulting code with :py:class:`lazylist` was similar to this::

    results = lazylist(api.search(query))
    if not results:
        print('Nothing found')
    else:
        for result in results:
            print_result(result)

The `api.search` method returns a generator that yields one item at a
time from the API. By representing the results as a
:py:class:`lazylist` the code for checking if there are any results
and then iterating over them is very simple. The corresponding code
without :py:class:`lazylist` would be something like this::

    results = api.search(query)
    results_iter_1, results_iter_2 = itertools.tee(results)
    if not results_iter_1:
        print('Nothing found')
    else:
        for result in results_iter_2:
            print_result(result)

Additional `tee` iterators would be needed if the results were to be
processed multiple times, and it would be impossible to perform
indexed access on the results, which is sometimes a requirement.

"""

__all__ = (
    'lazylist',
)

from .lazylist import lazylist   # noqa;
