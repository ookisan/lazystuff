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

"""Lazy-ish evaluation of Python iterables."""

__all__ = (
    'lazylist',
)

from .lazylist import lazylist   # noqa;
