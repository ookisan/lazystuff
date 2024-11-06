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

This package implements a two data types: :py:class:`lazylist` and
:py:class:`lazydict'. The main use of these types is in situations
where a list or dictionary elemnt may be very expensive to calculate,
but might never be used (or only partially used), but the user expects
something that behaves like a list or dictionary.

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

:py:class:`lazydict` was developed for a similar situation, where
certain dictionary elements were calculated by making expensive API
calls, but were not always used. By deferring calculating to the first
access, the calls would only be made if necessary.

"""

__all__ = (
    'lazylist',
    'lazydict',
)

from .lazylist import lazylist   # noqa;
from .lazydict import lazydict   # noqa;
