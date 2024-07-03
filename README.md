# Lazy list-like containers

This package implements a list-like container that is populated in a
lazy-ish manner. When a container is extended using the extend method
or addition operators, the iterable is not accessed immediately. It is
only accessed when needed and only to the extent required.

For example:

   def positive_squares():
       index = 1
       while True:
           yield index * index
	   index += 1

   result = lazylist(positive_squares)
   print(result[100])

With a normal list, the assignment would never complete. With a lazy
list, it does immediately. The print statement will cause the
generator to be called 101 times.

This data structure was originally developed to simplify an
application that performed expensive operations implemented as
generators. By using lazy lists, the results returned could be
accessed more simply, results could easily be presented to the user
incrementally, and some operations were never performed as their
results were never requested.

## Sorting

Sorting will materialize the entire list.

## Reversing

Reversing will not materialize the list, but will call the reversed
function on every iterable that has not yet been accessed.

## Gotchas

### Equality

Lazy lists test equal to regular lists but not to tuples.


### Mutable extensions

Since elements are materialized the first time they are needed, no
earlier, if a lazy list has been extended with an iterable that can
change, the value at the time it is accessed will be used.

For example, adding an iterator, then requesting some elements from
it:

    >>> low = iter([0, 1, 2])
    >>> high = [3, 4, 5]
    >>> lst = lazylist()
    >>> lst += low
    >>> lst += high
    >>> next(low)
    >>> next(low)
    >>> print(lst)
    [2, 3, 4, 5]

When a list is added to a lazy list, it is copied to avoid surprises.