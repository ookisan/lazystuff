# lazystuff documentation

The [`lazystuff`](#module-lazystuff) package provides lazy-ish list-like objects.

This package implements a single data type, `lazylist`, that
behaves almost like a regular list. It has all the normal list methods
and operators and they work as expected with a single exception.

When a `lazylist` is extended with an iterable other than a
regular list, evaluation of the iterable is deferred until it is
needed, and is limited to the number of elements required. The
elements that are fetched from the iterator(s) are stored as a regular
list inside the `lazylist`.

Iteration only takes place when an element is requested. For example:

* When checking if the list is empty (or non-empty), a single element
  is fetched.
* When indexing the list using a positive number, elements are fetched
  until the requested index is reached.
* When the `index()` method is called, elements are fetched
  until the requested value is found.

There are situations when all iterators are exhausted, including:

* When the length of the list is requested.
* When using the in operator and the value is not in the list.
* When calling `index()` with a value that is not in the list.
* When the list is printed (all elements are printed).
* When the list is indexed with a negative number.
* When the `remove()`, `count()`, or `sort()` methods are called.
* When equal lists are compared.
* When the list is pickled.

For example, a `lazylist()` can represent an infinite sequence:

```default
all_squares = lazylist(x * x for x in itertools.count())
print(squares[99])  # Only iterates 100 times
```

Multiple sequences can be added to a lazylist and regular lists and
iterators can be mixed:

```default
>>> example = lazylist(['a', 'b', 'c'])
>>> example.extend(range(1, 4))
>>> example.extend(string.ascii_lowercase[3:6])
>>> print(example[3])
1
>>> del example[6]
>>> print(example)
['a', 'b', 'c', 1, 2, 3, 'e', 'f']
```

When the list is indexed with 3, a single element is fetched from the
range iterator. When element 6 is deleted, the range iterator is
exhausted and a single element is fetched from the string iterator in
order to reach the element at index 6. Finally, the string iterator is
also exhausted when the list is printed. The `repr()` function
to see the current status of the list:

```default
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
```

The representation contains two elements: first the list of list
elements that have been fetched from the iterators and second the list
of iterators and regular lists that have been added to the
`lazylist`.

`lazylist` was originally developed to simplify streaming
results from an API to a receiver with the goal that results should be
sent to the receiver as they became available and that if the process
were aborted, no unnecessary calls to the API should have been made.

The resulting code with `lazylist` was similar to this:

```default
results = lazylist(api.search(query))
if not results:
    print('Nothing found')
else:
    for result in results:
        print_result(result)
```

The api.search method returns a generator that yields one item at a
time from the API. By representing the results as a
`lazylist` the code for checking if there are any results
and then iterating over them is very simple. The corresponding code
without `lazylist` would be something like this:

```default
results = api.search(query)
results_iter_1, results_iter_2 = itertools.tee(results)
if not results_iter_1:
    print('Nothing found')
else:
    for result in results_iter_2:
        print_result(result)
```

Additional tee iterators would be needed if the results were to be
processed multiple times, and it would be impossible to perform
indexed access on the results, which is sometimes a requirement.
