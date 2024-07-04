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

"""Lazy-ish list construction.

This package implements a single data type, lazylist, that mostly
behaves like a list. Unlike a regular list, when a lazylist is
extended with an iterable other than a regular list, the iterable is
not iterated immediately. Instead, iteration is deferred until an
element from the iterator is required, and iteration is limited to
only the necessary elements.

This allows a lazylist to represent an infinite sequence, such as in:

   def squares():
       index = 0
       while True:
           yield index * index
           index += 1

   all_squares = lazylist(squares())
   print(squares[99])  # Only iterates 100 times

It also simplifies the use of generators. Consider an api with a
search function that returns a generator yielding the results, slowly,
one at a time.

   results = lazylist(api.search(query))
   if not results:
       print('Nothing found')
   else:
       for result in results:
           print_result(result)

The first test will fetch a single element from the generator, so if
there are results, they will start printing immediately at the rate
they can be delivered by the api. The corresponding code without
lazylist would be something like this:

   results = api.search(query)
   results_iter_1, results_iter_2 = itertools.tee(results)
   if not results_iter_1:
       print('Nothing found')
   else:
       for result in results_iter_2:
           print_result(result)

If the sequence needs to be processed multiple times, then additional
iterators will need to be created, and random access is not suppported.
"""

__all__ = (
    'lazylist',
)

from .lazylist import lazylist   # noqa;
