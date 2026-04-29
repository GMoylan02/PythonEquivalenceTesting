"""Sorted Set
=============

:doc:`Sorted Containers<index>` is an Apache2 licensed Python sorted
collections library, written in pure-Python, and fast as C-extensions. The
:doc:`introduction<introduction>` is the best way to get started.

Sorted set implementations:

.. currentmodule:: sortedcontainers

* :class:`SortedSet`

"""

from collections.abc import MutableSet, Sequence, Set
from itertools import chain
from operator import eq, ge, gt, le, lt, ne
from textwrap import dedent

from .sortedlist import SortedList, recursive_repr
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


def _make_cmp(set_op, symbol, doc):
    args = [set_op, symbol, doc]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__make_cmp__mutmut_orig, x__make_cmp__mutmut_mutants, args, kwargs, None)


def x__make_cmp__mutmut_orig(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_1(set_op, symbol, doc):  # pragma: no mutate
    "XXMake comparator method.XX"

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_2(set_op, symbol, doc):  # pragma: no mutate
    "make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_3(set_op, symbol, doc):  # pragma: no mutate
    "MAKE COMPARATOR METHOD."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_4(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "XXCompare method for sorted set and set.XX"
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_5(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_6(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "COMPARE METHOD FOR SORTED SET AND SET."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_7(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(None, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_8(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, None)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_9(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_10(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, )
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_11(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(None, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_12(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, None)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_13(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_14(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, )
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_15(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = None
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_16(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = None
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_17(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = None
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_18(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = None
    return comparer


def x__make_cmp__mutmut_19(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(None)
    return comparer


def x__make_cmp__mutmut_20(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(None, set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_21(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, None, symbol))
    return comparer


def x__make_cmp__mutmut_22(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, None))
    return comparer


def x__make_cmp__mutmut_23(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(set_op_name, symbol))
    return comparer


def x__make_cmp__mutmut_24(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, symbol))
    return comparer


def x__make_cmp__mutmut_25(set_op, symbol, doc):  # pragma: no mutate
    "Make comparator method."

    def comparer(self, other):
        "Compare method for sorted set and set."
        if isinstance(other, SortedSet):
            return set_op(self._set, other._set)
        elif isinstance(other, Set):
            return set_op(self._set, other)
        return NotImplemented

    set_op_name = set_op.__name__
    comparer.__name__ = f'__{set_op_name}__'
    doc_str = """Return true if and only if sorted set is {0} `other`.

    ``ss.__{1}__(other)`` <==> ``ss {2} other``

    Comparisons use subset and superset semantics as with sets.

    Runtime complexity: `O(n)`

    :param other: `other` set
    :return: true if sorted set is {0} `other`

    """
    comparer.__doc__ = dedent(doc_str.format(doc, set_op_name, ))
    return comparer

x__make_cmp__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__make_cmp__mutmut_1': x__make_cmp__mutmut_1, 
    'x__make_cmp__mutmut_2': x__make_cmp__mutmut_2, 
    'x__make_cmp__mutmut_3': x__make_cmp__mutmut_3, 
    'x__make_cmp__mutmut_4': x__make_cmp__mutmut_4, 
    'x__make_cmp__mutmut_5': x__make_cmp__mutmut_5, 
    'x__make_cmp__mutmut_6': x__make_cmp__mutmut_6, 
    'x__make_cmp__mutmut_7': x__make_cmp__mutmut_7, 
    'x__make_cmp__mutmut_8': x__make_cmp__mutmut_8, 
    'x__make_cmp__mutmut_9': x__make_cmp__mutmut_9, 
    'x__make_cmp__mutmut_10': x__make_cmp__mutmut_10, 
    'x__make_cmp__mutmut_11': x__make_cmp__mutmut_11, 
    'x__make_cmp__mutmut_12': x__make_cmp__mutmut_12, 
    'x__make_cmp__mutmut_13': x__make_cmp__mutmut_13, 
    'x__make_cmp__mutmut_14': x__make_cmp__mutmut_14, 
    'x__make_cmp__mutmut_15': x__make_cmp__mutmut_15, 
    'x__make_cmp__mutmut_16': x__make_cmp__mutmut_16, 
    'x__make_cmp__mutmut_17': x__make_cmp__mutmut_17, 
    'x__make_cmp__mutmut_18': x__make_cmp__mutmut_18, 
    'x__make_cmp__mutmut_19': x__make_cmp__mutmut_19, 
    'x__make_cmp__mutmut_20': x__make_cmp__mutmut_20, 
    'x__make_cmp__mutmut_21': x__make_cmp__mutmut_21, 
    'x__make_cmp__mutmut_22': x__make_cmp__mutmut_22, 
    'x__make_cmp__mutmut_23': x__make_cmp__mutmut_23, 
    'x__make_cmp__mutmut_24': x__make_cmp__mutmut_24, 
    'x__make_cmp__mutmut_25': x__make_cmp__mutmut_25
}
x__make_cmp__mutmut_orig.__name__ = 'x__make_cmp'

class SortedSet(MutableSet, Sequence):
    """Sorted set is a sorted mutable set.

    Sorted set values are maintained in sorted order. The design of sorted set
    is simple: sorted set uses a set for set-operations and maintains a sorted
    list of values.

    Sorted set values must be hashable and comparable. The hash and total
    ordering of values must not change while they are stored in the sorted set.

    Mutable set methods:

    * :func:`SortedSet.__contains__`
    * :func:`SortedSet.__iter__`
    * :func:`SortedSet.__len__`
    * :func:`SortedSet.add`
    * :func:`SortedSet.discard`

    Sequence methods:

    * :func:`SortedSet.__getitem__`
    * :func:`SortedSet.__delitem__`
    * :func:`SortedSet.__reversed__`

    Methods for removing values:

    * :func:`SortedSet.clear`
    * :func:`SortedSet.pop`
    * :func:`SortedSet.remove`

    Set-operation methods:

    * :func:`SortedSet.difference`
    * :func:`SortedSet.difference_update`
    * :func:`SortedSet.intersection`
    * :func:`SortedSet.intersection_update`
    * :func:`SortedSet.symmetric_difference`
    * :func:`SortedSet.symmetric_difference_update`
    * :func:`SortedSet.union`
    * :func:`SortedSet.update`

    Methods for miscellany:

    * :func:`SortedSet.copy`
    * :func:`SortedSet.count`
    * :func:`SortedSet.__repr__`
    * :func:`SortedSet._check`

    Sorted list methods available:

    * :func:`SortedList.bisect_left`
    * :func:`SortedList.bisect_right`
    * :func:`SortedList.index`
    * :func:`SortedList.irange`
    * :func:`SortedList.islice`
    * :func:`SortedList._reset`

    Additional sorted list methods available, if key-function used:

    * :func:`SortedKeyList.bisect_key_left`
    * :func:`SortedKeyList.bisect_key_right`
    * :func:`SortedKeyList.irange_key`

    Sorted set comparisons use subset and superset relations. Two sorted sets
    are equal if and only if every element of each sorted set is contained in
    the other (each is a subset of the other). A sorted set is less than
    another sorted set if and only if the first sorted set is a proper subset
    of the second sorted set (is a subset, but is not equal). A sorted set is
    greater than another sorted set if and only if the first sorted set is a
    proper superset of the second sorted set (is a superset, but is not equal).

    """

    def __init__(self, iterable=None, key=None):
        args = [iterable, key]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁ__init____mutmut_orig(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_1(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = None

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_2(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_3(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(None, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_4(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, None):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_5(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr('_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_6(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, ):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_7(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, 'XX_setXX'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_8(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_SET'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_9(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = None

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_10(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = None

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_11(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(None, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_12(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=None)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_13(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_14(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, )

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_15(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = None
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_16(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = None
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_17(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = None
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_18(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = None

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_19(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = None
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_20(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = None
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_21(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = None
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_22(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = None
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_23(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = None
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_24(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = None
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_25(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = None
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_26(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = None

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_27(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_28(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = None
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_29(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = None
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_30(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = None
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_31(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = None

        if iterable is not None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_32(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is None:
            self._update(iterable)

    def xǁSortedSetǁ__init____mutmut_33(self, iterable=None, key=None):
        """Initialize sorted set instance.

        Optional `iterable` argument provides an initial iterable of values to
        initialize the sorted set.

        Optional `key` argument defines a callable that, like the `key`
        argument to Python's `sorted` function, extracts a comparison key from
        each value. The default, none, compares values directly.

        Runtime complexity: `O(n*log(n))`

        >>> ss = SortedSet([3, 1, 2, 5, 4])
        >>> ss
        SortedSet([1, 2, 3, 4, 5])
        >>> from operator import neg
        >>> ss = SortedSet([3, 1, 2, 5, 4], neg)
        >>> ss
        SortedSet([5, 4, 3, 2, 1], key=<built-in function neg>)

        :param iterable: initial values (optional)
        :param key: function used to extract comparison key (optional)

        """
        self._key = key

        # SortedSet._fromset calls SortedSet.__init__ after initializing the
        # _set attribute. So only create a new set if the _set attribute is not
        # already present.

        if not hasattr(self, '_set'):
            self._set = set()

        self._list = SortedList(self._set, key=key)

        # Expose some set methods publicly.

        _set = self._set
        self.isdisjoint = _set.isdisjoint
        self.issubset = _set.issubset
        self.issuperset = _set.issuperset

        # Expose some sorted list methods publicly.

        _list = self._list
        self.bisect_left = _list.bisect_left
        self.bisect = _list.bisect
        self.bisect_right = _list.bisect_right
        self.index = _list.index
        self.irange = _list.irange
        self.islice = _list.islice
        self._reset = _list._reset

        if key is not None:
            self.bisect_key_left = _list.bisect_key_left
            self.bisect_key_right = _list.bisect_key_right
            self.bisect_key = _list.bisect_key
            self.irange_key = _list.irange_key

        if iterable is not None:
            self._update(None)
    
    xǁSortedSetǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁ__init____mutmut_1': xǁSortedSetǁ__init____mutmut_1, 
        'xǁSortedSetǁ__init____mutmut_2': xǁSortedSetǁ__init____mutmut_2, 
        'xǁSortedSetǁ__init____mutmut_3': xǁSortedSetǁ__init____mutmut_3, 
        'xǁSortedSetǁ__init____mutmut_4': xǁSortedSetǁ__init____mutmut_4, 
        'xǁSortedSetǁ__init____mutmut_5': xǁSortedSetǁ__init____mutmut_5, 
        'xǁSortedSetǁ__init____mutmut_6': xǁSortedSetǁ__init____mutmut_6, 
        'xǁSortedSetǁ__init____mutmut_7': xǁSortedSetǁ__init____mutmut_7, 
        'xǁSortedSetǁ__init____mutmut_8': xǁSortedSetǁ__init____mutmut_8, 
        'xǁSortedSetǁ__init____mutmut_9': xǁSortedSetǁ__init____mutmut_9, 
        'xǁSortedSetǁ__init____mutmut_10': xǁSortedSetǁ__init____mutmut_10, 
        'xǁSortedSetǁ__init____mutmut_11': xǁSortedSetǁ__init____mutmut_11, 
        'xǁSortedSetǁ__init____mutmut_12': xǁSortedSetǁ__init____mutmut_12, 
        'xǁSortedSetǁ__init____mutmut_13': xǁSortedSetǁ__init____mutmut_13, 
        'xǁSortedSetǁ__init____mutmut_14': xǁSortedSetǁ__init____mutmut_14, 
        'xǁSortedSetǁ__init____mutmut_15': xǁSortedSetǁ__init____mutmut_15, 
        'xǁSortedSetǁ__init____mutmut_16': xǁSortedSetǁ__init____mutmut_16, 
        'xǁSortedSetǁ__init____mutmut_17': xǁSortedSetǁ__init____mutmut_17, 
        'xǁSortedSetǁ__init____mutmut_18': xǁSortedSetǁ__init____mutmut_18, 
        'xǁSortedSetǁ__init____mutmut_19': xǁSortedSetǁ__init____mutmut_19, 
        'xǁSortedSetǁ__init____mutmut_20': xǁSortedSetǁ__init____mutmut_20, 
        'xǁSortedSetǁ__init____mutmut_21': xǁSortedSetǁ__init____mutmut_21, 
        'xǁSortedSetǁ__init____mutmut_22': xǁSortedSetǁ__init____mutmut_22, 
        'xǁSortedSetǁ__init____mutmut_23': xǁSortedSetǁ__init____mutmut_23, 
        'xǁSortedSetǁ__init____mutmut_24': xǁSortedSetǁ__init____mutmut_24, 
        'xǁSortedSetǁ__init____mutmut_25': xǁSortedSetǁ__init____mutmut_25, 
        'xǁSortedSetǁ__init____mutmut_26': xǁSortedSetǁ__init____mutmut_26, 
        'xǁSortedSetǁ__init____mutmut_27': xǁSortedSetǁ__init____mutmut_27, 
        'xǁSortedSetǁ__init____mutmut_28': xǁSortedSetǁ__init____mutmut_28, 
        'xǁSortedSetǁ__init____mutmut_29': xǁSortedSetǁ__init____mutmut_29, 
        'xǁSortedSetǁ__init____mutmut_30': xǁSortedSetǁ__init____mutmut_30, 
        'xǁSortedSetǁ__init____mutmut_31': xǁSortedSetǁ__init____mutmut_31, 
        'xǁSortedSetǁ__init____mutmut_32': xǁSortedSetǁ__init____mutmut_32, 
        'xǁSortedSetǁ__init____mutmut_33': xǁSortedSetǁ__init____mutmut_33
    }
    xǁSortedSetǁ__init____mutmut_orig.__name__ = 'xǁSortedSetǁ__init__'

    @classmethod
    def _fromset(cls, values, key=None):
        """Initialize sorted set from existing set.

        Used internally by set operations that return a new set.

        """
        sorted_set = object.__new__(cls)
        sorted_set._set = values
        sorted_set.__init__(key=key)
        return sorted_set

    @property
    def key(self):
        """Function used to extract comparison key from values.

        Sorted set compares values directly when the key function is none.

        """
        return self._key

    def __contains__(self, value):
        args = [value]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁ__contains____mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁ__contains____mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁ__contains____mutmut_orig(self, value):
        """Return true if `value` is an element of the sorted set.

        ``ss.__contains__(value)`` <==> ``value in ss``

        Runtime complexity: `O(1)`

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> 3 in ss
        True

        :param value: search for value in sorted set
        :return: true if `value` in sorted set

        """
        return value in self._set

    def xǁSortedSetǁ__contains____mutmut_1(self, value):
        """Return true if `value` is an element of the sorted set.

        ``ss.__contains__(value)`` <==> ``value in ss``

        Runtime complexity: `O(1)`

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> 3 in ss
        True

        :param value: search for value in sorted set
        :return: true if `value` in sorted set

        """
        return value not in self._set
    
    xǁSortedSetǁ__contains____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁ__contains____mutmut_1': xǁSortedSetǁ__contains____mutmut_1
    }
    xǁSortedSetǁ__contains____mutmut_orig.__name__ = 'xǁSortedSetǁ__contains__'

    def __getitem__(self, index):
        """Lookup value at `index` in sorted set.

        ``ss.__getitem__(index)`` <==> ``ss[index]``

        Supports slicing.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet('abcde')
        >>> ss[2]
        'c'
        >>> ss[-1]
        'e'
        >>> ss[2:5]
        ['c', 'd', 'e']

        :param index: integer or slice for indexing
        :return: value or list of values
        :raises IndexError: if index out of range

        """
        return self._list[index]

    def __delitem__(self, index):
        args = [index]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁ__delitem____mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁ__delitem____mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁ__delitem____mutmut_orig(self, index):
        """Remove value at `index` from sorted set.

        ``ss.__delitem__(index)`` <==> ``del ss[index]``

        Supports slicing.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet('abcde')
        >>> del ss[2]
        >>> ss
        SortedSet(['a', 'b', 'd', 'e'])
        >>> del ss[:2]
        >>> ss
        SortedSet(['d', 'e'])

        :param index: integer or slice for indexing
        :raises IndexError: if index out of range

        """
        _set = self._set
        _list = self._list
        if isinstance(index, slice):
            values = _list[index]
            _set.difference_update(values)
        else:
            value = _list[index]
            _set.remove(value)
        del _list[index]

    def xǁSortedSetǁ__delitem____mutmut_1(self, index):
        """Remove value at `index` from sorted set.

        ``ss.__delitem__(index)`` <==> ``del ss[index]``

        Supports slicing.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet('abcde')
        >>> del ss[2]
        >>> ss
        SortedSet(['a', 'b', 'd', 'e'])
        >>> del ss[:2]
        >>> ss
        SortedSet(['d', 'e'])

        :param index: integer or slice for indexing
        :raises IndexError: if index out of range

        """
        _set = None
        _list = self._list
        if isinstance(index, slice):
            values = _list[index]
            _set.difference_update(values)
        else:
            value = _list[index]
            _set.remove(value)
        del _list[index]

    def xǁSortedSetǁ__delitem____mutmut_2(self, index):
        """Remove value at `index` from sorted set.

        ``ss.__delitem__(index)`` <==> ``del ss[index]``

        Supports slicing.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet('abcde')
        >>> del ss[2]
        >>> ss
        SortedSet(['a', 'b', 'd', 'e'])
        >>> del ss[:2]
        >>> ss
        SortedSet(['d', 'e'])

        :param index: integer or slice for indexing
        :raises IndexError: if index out of range

        """
        _set = self._set
        _list = None
        if isinstance(index, slice):
            values = _list[index]
            _set.difference_update(values)
        else:
            value = _list[index]
            _set.remove(value)
        del _list[index]

    def xǁSortedSetǁ__delitem____mutmut_3(self, index):
        """Remove value at `index` from sorted set.

        ``ss.__delitem__(index)`` <==> ``del ss[index]``

        Supports slicing.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet('abcde')
        >>> del ss[2]
        >>> ss
        SortedSet(['a', 'b', 'd', 'e'])
        >>> del ss[:2]
        >>> ss
        SortedSet(['d', 'e'])

        :param index: integer or slice for indexing
        :raises IndexError: if index out of range

        """
        _set = self._set
        _list = self._list
        if isinstance(index, slice):
            values = None
            _set.difference_update(values)
        else:
            value = _list[index]
            _set.remove(value)
        del _list[index]

    def xǁSortedSetǁ__delitem____mutmut_4(self, index):
        """Remove value at `index` from sorted set.

        ``ss.__delitem__(index)`` <==> ``del ss[index]``

        Supports slicing.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet('abcde')
        >>> del ss[2]
        >>> ss
        SortedSet(['a', 'b', 'd', 'e'])
        >>> del ss[:2]
        >>> ss
        SortedSet(['d', 'e'])

        :param index: integer or slice for indexing
        :raises IndexError: if index out of range

        """
        _set = self._set
        _list = self._list
        if isinstance(index, slice):
            values = _list[index]
            _set.difference_update(None)
        else:
            value = _list[index]
            _set.remove(value)
        del _list[index]

    def xǁSortedSetǁ__delitem____mutmut_5(self, index):
        """Remove value at `index` from sorted set.

        ``ss.__delitem__(index)`` <==> ``del ss[index]``

        Supports slicing.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet('abcde')
        >>> del ss[2]
        >>> ss
        SortedSet(['a', 'b', 'd', 'e'])
        >>> del ss[:2]
        >>> ss
        SortedSet(['d', 'e'])

        :param index: integer or slice for indexing
        :raises IndexError: if index out of range

        """
        _set = self._set
        _list = self._list
        if isinstance(index, slice):
            values = _list[index]
            _set.difference_update(values)
        else:
            value = None
            _set.remove(value)
        del _list[index]

    def xǁSortedSetǁ__delitem____mutmut_6(self, index):
        """Remove value at `index` from sorted set.

        ``ss.__delitem__(index)`` <==> ``del ss[index]``

        Supports slicing.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet('abcde')
        >>> del ss[2]
        >>> ss
        SortedSet(['a', 'b', 'd', 'e'])
        >>> del ss[:2]
        >>> ss
        SortedSet(['d', 'e'])

        :param index: integer or slice for indexing
        :raises IndexError: if index out of range

        """
        _set = self._set
        _list = self._list
        if isinstance(index, slice):
            values = _list[index]
            _set.difference_update(values)
        else:
            value = _list[index]
            _set.remove(None)
        del _list[index]
    
    xǁSortedSetǁ__delitem____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁ__delitem____mutmut_1': xǁSortedSetǁ__delitem____mutmut_1, 
        'xǁSortedSetǁ__delitem____mutmut_2': xǁSortedSetǁ__delitem____mutmut_2, 
        'xǁSortedSetǁ__delitem____mutmut_3': xǁSortedSetǁ__delitem____mutmut_3, 
        'xǁSortedSetǁ__delitem____mutmut_4': xǁSortedSetǁ__delitem____mutmut_4, 
        'xǁSortedSetǁ__delitem____mutmut_5': xǁSortedSetǁ__delitem____mutmut_5, 
        'xǁSortedSetǁ__delitem____mutmut_6': xǁSortedSetǁ__delitem____mutmut_6
    }
    xǁSortedSetǁ__delitem____mutmut_orig.__name__ = 'xǁSortedSetǁ__delitem__'

    __eq__ = _make_cmp(eq, '==', 'equal to')  # pragma: no mutate
    __ne__ = _make_cmp(ne, '!=', 'not equal to')  # pragma: no mutate
    __lt__ = _make_cmp(lt, '<', 'a proper subset of')  # pragma: no mutate
    __gt__ = _make_cmp(gt, '>', 'a proper superset of')  # pragma: no mutate
    __le__ = _make_cmp(le, '<=', 'a subset of')  # pragma: no mutate
    __ge__ = _make_cmp(ge, '>=', 'a superset of')  # pragma: no mutate
    _make_cmp = staticmethod(_make_cmp)

    def __len__(self):
        """Return the size of the sorted set.

        ``ss.__len__()`` <==> ``len(ss)``

        :return: size of sorted set

        """
        return len(self._set)

    def __iter__(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁ__iter____mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁ__iter____mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁ__iter____mutmut_orig(self):
        """Return an iterator over the sorted set.

        ``ss.__iter__()`` <==> ``iter(ss)``

        Iterating the sorted set while adding or deleting values may raise a
        :exc:`RuntimeError` or fail to iterate over all values.

        """
        return iter(self._list)

    def xǁSortedSetǁ__iter____mutmut_1(self):
        """Return an iterator over the sorted set.

        ``ss.__iter__()`` <==> ``iter(ss)``

        Iterating the sorted set while adding or deleting values may raise a
        :exc:`RuntimeError` or fail to iterate over all values.

        """
        return iter(None)
    
    xǁSortedSetǁ__iter____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁ__iter____mutmut_1': xǁSortedSetǁ__iter____mutmut_1
    }
    xǁSortedSetǁ__iter____mutmut_orig.__name__ = 'xǁSortedSetǁ__iter__'

    def __reversed__(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁ__reversed____mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁ__reversed____mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁ__reversed____mutmut_orig(self):
        """Return a reverse iterator over the sorted set.

        ``ss.__reversed__()`` <==> ``reversed(ss)``

        Iterating the sorted set while adding or deleting values may raise a
        :exc:`RuntimeError` or fail to iterate over all values.

        """
        return reversed(self._list)

    def xǁSortedSetǁ__reversed____mutmut_1(self):
        """Return a reverse iterator over the sorted set.

        ``ss.__reversed__()`` <==> ``reversed(ss)``

        Iterating the sorted set while adding or deleting values may raise a
        :exc:`RuntimeError` or fail to iterate over all values.

        """
        return reversed(None)
    
    xǁSortedSetǁ__reversed____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁ__reversed____mutmut_1': xǁSortedSetǁ__reversed____mutmut_1
    }
    xǁSortedSetǁ__reversed____mutmut_orig.__name__ = 'xǁSortedSetǁ__reversed__'

    def add(self, value):
        args = [value]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁadd__mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁadd__mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁadd__mutmut_orig(self, value):
        """Add `value` to sorted set.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet()
        >>> ss.add(3)
        >>> ss.add(1)
        >>> ss.add(2)
        >>> ss
        SortedSet([1, 2, 3])

        :param value: value to add to sorted set

        """
        _set = self._set
        if value not in _set:
            _set.add(value)
            self._list.add(value)

    def xǁSortedSetǁadd__mutmut_1(self, value):
        """Add `value` to sorted set.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet()
        >>> ss.add(3)
        >>> ss.add(1)
        >>> ss.add(2)
        >>> ss
        SortedSet([1, 2, 3])

        :param value: value to add to sorted set

        """
        _set = None
        if value not in _set:
            _set.add(value)
            self._list.add(value)

    def xǁSortedSetǁadd__mutmut_2(self, value):
        """Add `value` to sorted set.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet()
        >>> ss.add(3)
        >>> ss.add(1)
        >>> ss.add(2)
        >>> ss
        SortedSet([1, 2, 3])

        :param value: value to add to sorted set

        """
        _set = self._set
        if value in _set:
            _set.add(value)
            self._list.add(value)

    def xǁSortedSetǁadd__mutmut_3(self, value):
        """Add `value` to sorted set.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet()
        >>> ss.add(3)
        >>> ss.add(1)
        >>> ss.add(2)
        >>> ss
        SortedSet([1, 2, 3])

        :param value: value to add to sorted set

        """
        _set = self._set
        if value not in _set:
            _set.add(None)
            self._list.add(value)

    def xǁSortedSetǁadd__mutmut_4(self, value):
        """Add `value` to sorted set.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet()
        >>> ss.add(3)
        >>> ss.add(1)
        >>> ss.add(2)
        >>> ss
        SortedSet([1, 2, 3])

        :param value: value to add to sorted set

        """
        _set = self._set
        if value not in _set:
            _set.add(value)
            self._list.add(None)
    
    xǁSortedSetǁadd__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁadd__mutmut_1': xǁSortedSetǁadd__mutmut_1, 
        'xǁSortedSetǁadd__mutmut_2': xǁSortedSetǁadd__mutmut_2, 
        'xǁSortedSetǁadd__mutmut_3': xǁSortedSetǁadd__mutmut_3, 
        'xǁSortedSetǁadd__mutmut_4': xǁSortedSetǁadd__mutmut_4
    }
    xǁSortedSetǁadd__mutmut_orig.__name__ = 'xǁSortedSetǁadd'

    _add = add

    def clear(self):
        """Remove all values from sorted set.

        Runtime complexity: `O(n)`

        """
        self._set.clear()
        self._list.clear()

    def copy(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁcopy__mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁcopy__mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁcopy__mutmut_orig(self):
        """Return a shallow copy of the sorted set.

        Runtime complexity: `O(n)`

        :return: new sorted set

        """
        return self._fromset(set(self._set), key=self._key)

    def xǁSortedSetǁcopy__mutmut_1(self):
        """Return a shallow copy of the sorted set.

        Runtime complexity: `O(n)`

        :return: new sorted set

        """
        return self._fromset(None, key=self._key)

    def xǁSortedSetǁcopy__mutmut_2(self):
        """Return a shallow copy of the sorted set.

        Runtime complexity: `O(n)`

        :return: new sorted set

        """
        return self._fromset(set(self._set), key=None)

    def xǁSortedSetǁcopy__mutmut_3(self):
        """Return a shallow copy of the sorted set.

        Runtime complexity: `O(n)`

        :return: new sorted set

        """
        return self._fromset(key=self._key)

    def xǁSortedSetǁcopy__mutmut_4(self):
        """Return a shallow copy of the sorted set.

        Runtime complexity: `O(n)`

        :return: new sorted set

        """
        return self._fromset(set(self._set), )

    def xǁSortedSetǁcopy__mutmut_5(self):
        """Return a shallow copy of the sorted set.

        Runtime complexity: `O(n)`

        :return: new sorted set

        """
        return self._fromset(set(None), key=self._key)
    
    xǁSortedSetǁcopy__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁcopy__mutmut_1': xǁSortedSetǁcopy__mutmut_1, 
        'xǁSortedSetǁcopy__mutmut_2': xǁSortedSetǁcopy__mutmut_2, 
        'xǁSortedSetǁcopy__mutmut_3': xǁSortedSetǁcopy__mutmut_3, 
        'xǁSortedSetǁcopy__mutmut_4': xǁSortedSetǁcopy__mutmut_4, 
        'xǁSortedSetǁcopy__mutmut_5': xǁSortedSetǁcopy__mutmut_5
    }
    xǁSortedSetǁcopy__mutmut_orig.__name__ = 'xǁSortedSetǁcopy'

    __copy__ = copy

    def count(self, value):
        args = [value]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁcount__mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁcount__mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁcount__mutmut_orig(self, value):
        """Return number of occurrences of `value` in the sorted set.

        Runtime complexity: `O(1)`

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.count(3)
        1

        :param value: value to count in sorted set
        :return: count

        """
        return 1 if value in self._set else 0

    def xǁSortedSetǁcount__mutmut_1(self, value):
        """Return number of occurrences of `value` in the sorted set.

        Runtime complexity: `O(1)`

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.count(3)
        1

        :param value: value to count in sorted set
        :return: count

        """
        return 2 if value in self._set else 0

    def xǁSortedSetǁcount__mutmut_2(self, value):
        """Return number of occurrences of `value` in the sorted set.

        Runtime complexity: `O(1)`

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.count(3)
        1

        :param value: value to count in sorted set
        :return: count

        """
        return 1 if value not in self._set else 0

    def xǁSortedSetǁcount__mutmut_3(self, value):
        """Return number of occurrences of `value` in the sorted set.

        Runtime complexity: `O(1)`

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.count(3)
        1

        :param value: value to count in sorted set
        :return: count

        """
        return 1 if value in self._set else 1
    
    xǁSortedSetǁcount__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁcount__mutmut_1': xǁSortedSetǁcount__mutmut_1, 
        'xǁSortedSetǁcount__mutmut_2': xǁSortedSetǁcount__mutmut_2, 
        'xǁSortedSetǁcount__mutmut_3': xǁSortedSetǁcount__mutmut_3
    }
    xǁSortedSetǁcount__mutmut_orig.__name__ = 'xǁSortedSetǁcount'

    def discard(self, value):
        args = [value]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁdiscard__mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁdiscard__mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁdiscard__mutmut_orig(self, value):
        """Remove `value` from sorted set if it is a member.

        If `value` is not a member, do nothing.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.discard(5)
        >>> ss.discard(0)
        >>> ss == set([1, 2, 3, 4])
        True

        :param value: `value` to discard from sorted set

        """
        _set = self._set
        if value in _set:
            _set.remove(value)
            self._list.remove(value)

    def xǁSortedSetǁdiscard__mutmut_1(self, value):
        """Remove `value` from sorted set if it is a member.

        If `value` is not a member, do nothing.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.discard(5)
        >>> ss.discard(0)
        >>> ss == set([1, 2, 3, 4])
        True

        :param value: `value` to discard from sorted set

        """
        _set = None
        if value in _set:
            _set.remove(value)
            self._list.remove(value)

    def xǁSortedSetǁdiscard__mutmut_2(self, value):
        """Remove `value` from sorted set if it is a member.

        If `value` is not a member, do nothing.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.discard(5)
        >>> ss.discard(0)
        >>> ss == set([1, 2, 3, 4])
        True

        :param value: `value` to discard from sorted set

        """
        _set = self._set
        if value not in _set:
            _set.remove(value)
            self._list.remove(value)

    def xǁSortedSetǁdiscard__mutmut_3(self, value):
        """Remove `value` from sorted set if it is a member.

        If `value` is not a member, do nothing.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.discard(5)
        >>> ss.discard(0)
        >>> ss == set([1, 2, 3, 4])
        True

        :param value: `value` to discard from sorted set

        """
        _set = self._set
        if value in _set:
            _set.remove(None)
            self._list.remove(value)

    def xǁSortedSetǁdiscard__mutmut_4(self, value):
        """Remove `value` from sorted set if it is a member.

        If `value` is not a member, do nothing.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.discard(5)
        >>> ss.discard(0)
        >>> ss == set([1, 2, 3, 4])
        True

        :param value: `value` to discard from sorted set

        """
        _set = self._set
        if value in _set:
            _set.remove(value)
            self._list.remove(None)
    
    xǁSortedSetǁdiscard__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁdiscard__mutmut_1': xǁSortedSetǁdiscard__mutmut_1, 
        'xǁSortedSetǁdiscard__mutmut_2': xǁSortedSetǁdiscard__mutmut_2, 
        'xǁSortedSetǁdiscard__mutmut_3': xǁSortedSetǁdiscard__mutmut_3, 
        'xǁSortedSetǁdiscard__mutmut_4': xǁSortedSetǁdiscard__mutmut_4
    }
    xǁSortedSetǁdiscard__mutmut_orig.__name__ = 'xǁSortedSetǁdiscard'

    _discard = discard

    def pop(self, index=-1):
        args = [index]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁpop__mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁpop__mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁpop__mutmut_orig(self, index=-1):
        """Remove and return value at `index` in sorted set.

        Raise :exc:`IndexError` if the sorted set is empty or index is out of
        range.

        Negative indices are supported.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet('abcde')
        >>> ss.pop()
        'e'
        >>> ss.pop(2)
        'c'
        >>> ss
        SortedSet(['a', 'b', 'd'])

        :param int index: index of value (default -1)
        :return: value
        :raises IndexError: if index is out of range

        """
        # pylint: disable=arguments-differ
        value = self._list.pop(index)
        self._set.remove(value)
        return value

    def xǁSortedSetǁpop__mutmut_1(self, index=-1):
        """Remove and return value at `index` in sorted set.

        Raise :exc:`IndexError` if the sorted set is empty or index is out of
        range.

        Negative indices are supported.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet('abcde')
        >>> ss.pop()
        'e'
        >>> ss.pop(2)
        'c'
        >>> ss
        SortedSet(['a', 'b', 'd'])

        :param int index: index of value (default -1)
        :return: value
        :raises IndexError: if index is out of range

        """
        # pylint: disable=arguments-differ
        value = None
        self._set.remove(value)
        return value

    def xǁSortedSetǁpop__mutmut_2(self, index=-1):
        """Remove and return value at `index` in sorted set.

        Raise :exc:`IndexError` if the sorted set is empty or index is out of
        range.

        Negative indices are supported.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet('abcde')
        >>> ss.pop()
        'e'
        >>> ss.pop(2)
        'c'
        >>> ss
        SortedSet(['a', 'b', 'd'])

        :param int index: index of value (default -1)
        :return: value
        :raises IndexError: if index is out of range

        """
        # pylint: disable=arguments-differ
        value = self._list.pop(None)
        self._set.remove(value)
        return value

    def xǁSortedSetǁpop__mutmut_3(self, index=-1):
        """Remove and return value at `index` in sorted set.

        Raise :exc:`IndexError` if the sorted set is empty or index is out of
        range.

        Negative indices are supported.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet('abcde')
        >>> ss.pop()
        'e'
        >>> ss.pop(2)
        'c'
        >>> ss
        SortedSet(['a', 'b', 'd'])

        :param int index: index of value (default -1)
        :return: value
        :raises IndexError: if index is out of range

        """
        # pylint: disable=arguments-differ
        value = self._list.pop(index)
        self._set.remove(None)
        return value
    
    xǁSortedSetǁpop__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁpop__mutmut_1': xǁSortedSetǁpop__mutmut_1, 
        'xǁSortedSetǁpop__mutmut_2': xǁSortedSetǁpop__mutmut_2, 
        'xǁSortedSetǁpop__mutmut_3': xǁSortedSetǁpop__mutmut_3
    }
    xǁSortedSetǁpop__mutmut_orig.__name__ = 'xǁSortedSetǁpop'

    def remove(self, value):
        args = [value]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁremove__mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁremove__mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁremove__mutmut_orig(self, value):
        """Remove `value` from sorted set; `value` must be a member.

        If `value` is not a member, raise :exc:`KeyError`.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.remove(5)
        >>> ss == set([1, 2, 3, 4])
        True
        >>> ss.remove(0)
        Traceback (most recent call last):
          ...
        KeyError: 0

        :param value: `value` to remove from sorted set
        :raises KeyError: if `value` is not in sorted set

        """
        self._set.remove(value)
        self._list.remove(value)

    def xǁSortedSetǁremove__mutmut_1(self, value):
        """Remove `value` from sorted set; `value` must be a member.

        If `value` is not a member, raise :exc:`KeyError`.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.remove(5)
        >>> ss == set([1, 2, 3, 4])
        True
        >>> ss.remove(0)
        Traceback (most recent call last):
          ...
        KeyError: 0

        :param value: `value` to remove from sorted set
        :raises KeyError: if `value` is not in sorted set

        """
        self._set.remove(None)
        self._list.remove(value)

    def xǁSortedSetǁremove__mutmut_2(self, value):
        """Remove `value` from sorted set; `value` must be a member.

        If `value` is not a member, raise :exc:`KeyError`.

        Runtime complexity: `O(log(n))` -- approximate.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.remove(5)
        >>> ss == set([1, 2, 3, 4])
        True
        >>> ss.remove(0)
        Traceback (most recent call last):
          ...
        KeyError: 0

        :param value: `value` to remove from sorted set
        :raises KeyError: if `value` is not in sorted set

        """
        self._set.remove(value)
        self._list.remove(None)
    
    xǁSortedSetǁremove__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁremove__mutmut_1': xǁSortedSetǁremove__mutmut_1, 
        'xǁSortedSetǁremove__mutmut_2': xǁSortedSetǁremove__mutmut_2
    }
    xǁSortedSetǁremove__mutmut_orig.__name__ = 'xǁSortedSetǁremove'

    def difference(self, *iterables):
        args = [*iterables]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁdifference__mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁdifference__mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁdifference__mutmut_orig(self, *iterables):
        """Return the difference of two or more sets as a new sorted set.

        The `difference` method also corresponds to operator ``-``.

        ``ss.__sub__(iterable)`` <==> ``ss - iterable``

        The difference is all values that are in this sorted set but not the
        other `iterables`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.difference([4, 5, 6, 7])
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        diff = self._set.difference(*iterables)
        return self._fromset(diff, key=self._key)

    def xǁSortedSetǁdifference__mutmut_1(self, *iterables):
        """Return the difference of two or more sets as a new sorted set.

        The `difference` method also corresponds to operator ``-``.

        ``ss.__sub__(iterable)`` <==> ``ss - iterable``

        The difference is all values that are in this sorted set but not the
        other `iterables`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.difference([4, 5, 6, 7])
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        diff = None
        return self._fromset(diff, key=self._key)

    def xǁSortedSetǁdifference__mutmut_2(self, *iterables):
        """Return the difference of two or more sets as a new sorted set.

        The `difference` method also corresponds to operator ``-``.

        ``ss.__sub__(iterable)`` <==> ``ss - iterable``

        The difference is all values that are in this sorted set but not the
        other `iterables`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.difference([4, 5, 6, 7])
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        diff = self._set.difference(*iterables)
        return self._fromset(None, key=self._key)

    def xǁSortedSetǁdifference__mutmut_3(self, *iterables):
        """Return the difference of two or more sets as a new sorted set.

        The `difference` method also corresponds to operator ``-``.

        ``ss.__sub__(iterable)`` <==> ``ss - iterable``

        The difference is all values that are in this sorted set but not the
        other `iterables`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.difference([4, 5, 6, 7])
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        diff = self._set.difference(*iterables)
        return self._fromset(diff, key=None)

    def xǁSortedSetǁdifference__mutmut_4(self, *iterables):
        """Return the difference of two or more sets as a new sorted set.

        The `difference` method also corresponds to operator ``-``.

        ``ss.__sub__(iterable)`` <==> ``ss - iterable``

        The difference is all values that are in this sorted set but not the
        other `iterables`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.difference([4, 5, 6, 7])
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        diff = self._set.difference(*iterables)
        return self._fromset(key=self._key)

    def xǁSortedSetǁdifference__mutmut_5(self, *iterables):
        """Return the difference of two or more sets as a new sorted set.

        The `difference` method also corresponds to operator ``-``.

        ``ss.__sub__(iterable)`` <==> ``ss - iterable``

        The difference is all values that are in this sorted set but not the
        other `iterables`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.difference([4, 5, 6, 7])
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        diff = self._set.difference(*iterables)
        return self._fromset(diff, )
    
    xǁSortedSetǁdifference__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁdifference__mutmut_1': xǁSortedSetǁdifference__mutmut_1, 
        'xǁSortedSetǁdifference__mutmut_2': xǁSortedSetǁdifference__mutmut_2, 
        'xǁSortedSetǁdifference__mutmut_3': xǁSortedSetǁdifference__mutmut_3, 
        'xǁSortedSetǁdifference__mutmut_4': xǁSortedSetǁdifference__mutmut_4, 
        'xǁSortedSetǁdifference__mutmut_5': xǁSortedSetǁdifference__mutmut_5
    }
    xǁSortedSetǁdifference__mutmut_orig.__name__ = 'xǁSortedSetǁdifference'

    __sub__ = difference

    def difference_update(self, *iterables):
        args = [*iterables]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁdifference_update__mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁdifference_update__mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁdifference_update__mutmut_orig(self, *iterables):
        """Remove all values of `iterables` from this sorted set.

        The `difference_update` method also corresponds to operator ``-=``.

        ``ss.__isub__(iterable)`` <==> ``ss -= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (4 * len(values)) > len(_set):
            _set.difference_update(values)
            _list.clear()
            _list.update(_set)
        else:
            _discard = self._discard
            for value in values:
                _discard(value)
        return self

    def xǁSortedSetǁdifference_update__mutmut_1(self, *iterables):
        """Remove all values of `iterables` from this sorted set.

        The `difference_update` method also corresponds to operator ``-=``.

        ``ss.__isub__(iterable)`` <==> ``ss -= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = None
        _list = self._list
        values = set(chain(*iterables))
        if (4 * len(values)) > len(_set):
            _set.difference_update(values)
            _list.clear()
            _list.update(_set)
        else:
            _discard = self._discard
            for value in values:
                _discard(value)
        return self

    def xǁSortedSetǁdifference_update__mutmut_2(self, *iterables):
        """Remove all values of `iterables` from this sorted set.

        The `difference_update` method also corresponds to operator ``-=``.

        ``ss.__isub__(iterable)`` <==> ``ss -= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = None
        values = set(chain(*iterables))
        if (4 * len(values)) > len(_set):
            _set.difference_update(values)
            _list.clear()
            _list.update(_set)
        else:
            _discard = self._discard
            for value in values:
                _discard(value)
        return self

    def xǁSortedSetǁdifference_update__mutmut_3(self, *iterables):
        """Remove all values of `iterables` from this sorted set.

        The `difference_update` method also corresponds to operator ``-=``.

        ``ss.__isub__(iterable)`` <==> ``ss -= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = None
        if (4 * len(values)) > len(_set):
            _set.difference_update(values)
            _list.clear()
            _list.update(_set)
        else:
            _discard = self._discard
            for value in values:
                _discard(value)
        return self

    def xǁSortedSetǁdifference_update__mutmut_4(self, *iterables):
        """Remove all values of `iterables` from this sorted set.

        The `difference_update` method also corresponds to operator ``-=``.

        ``ss.__isub__(iterable)`` <==> ``ss -= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(None)
        if (4 * len(values)) > len(_set):
            _set.difference_update(values)
            _list.clear()
            _list.update(_set)
        else:
            _discard = self._discard
            for value in values:
                _discard(value)
        return self

    def xǁSortedSetǁdifference_update__mutmut_5(self, *iterables):
        """Remove all values of `iterables` from this sorted set.

        The `difference_update` method also corresponds to operator ``-=``.

        ``ss.__isub__(iterable)`` <==> ``ss -= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (4 / len(values)) > len(_set):
            _set.difference_update(values)
            _list.clear()
            _list.update(_set)
        else:
            _discard = self._discard
            for value in values:
                _discard(value)
        return self

    def xǁSortedSetǁdifference_update__mutmut_6(self, *iterables):
        """Remove all values of `iterables` from this sorted set.

        The `difference_update` method also corresponds to operator ``-=``.

        ``ss.__isub__(iterable)`` <==> ``ss -= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (5 * len(values)) > len(_set):
            _set.difference_update(values)
            _list.clear()
            _list.update(_set)
        else:
            _discard = self._discard
            for value in values:
                _discard(value)
        return self

    def xǁSortedSetǁdifference_update__mutmut_7(self, *iterables):
        """Remove all values of `iterables` from this sorted set.

        The `difference_update` method also corresponds to operator ``-=``.

        ``ss.__isub__(iterable)`` <==> ``ss -= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (4 * len(values)) >= len(_set):
            _set.difference_update(values)
            _list.clear()
            _list.update(_set)
        else:
            _discard = self._discard
            for value in values:
                _discard(value)
        return self

    def xǁSortedSetǁdifference_update__mutmut_8(self, *iterables):
        """Remove all values of `iterables` from this sorted set.

        The `difference_update` method also corresponds to operator ``-=``.

        ``ss.__isub__(iterable)`` <==> ``ss -= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (4 * len(values)) > len(_set):
            _set.difference_update(None)
            _list.clear()
            _list.update(_set)
        else:
            _discard = self._discard
            for value in values:
                _discard(value)
        return self

    def xǁSortedSetǁdifference_update__mutmut_9(self, *iterables):
        """Remove all values of `iterables` from this sorted set.

        The `difference_update` method also corresponds to operator ``-=``.

        ``ss.__isub__(iterable)`` <==> ``ss -= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (4 * len(values)) > len(_set):
            _set.difference_update(values)
            _list.clear()
            _list.update(None)
        else:
            _discard = self._discard
            for value in values:
                _discard(value)
        return self

    def xǁSortedSetǁdifference_update__mutmut_10(self, *iterables):
        """Remove all values of `iterables` from this sorted set.

        The `difference_update` method also corresponds to operator ``-=``.

        ``ss.__isub__(iterable)`` <==> ``ss -= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (4 * len(values)) > len(_set):
            _set.difference_update(values)
            _list.clear()
            _list.update(_set)
        else:
            _discard = None
            for value in values:
                _discard(value)
        return self

    def xǁSortedSetǁdifference_update__mutmut_11(self, *iterables):
        """Remove all values of `iterables` from this sorted set.

        The `difference_update` method also corresponds to operator ``-=``.

        ``ss.__isub__(iterable)`` <==> ``ss -= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (4 * len(values)) > len(_set):
            _set.difference_update(values)
            _list.clear()
            _list.update(_set)
        else:
            _discard = self._discard
            for value in values:
                _discard(None)
        return self
    
    xǁSortedSetǁdifference_update__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁdifference_update__mutmut_1': xǁSortedSetǁdifference_update__mutmut_1, 
        'xǁSortedSetǁdifference_update__mutmut_2': xǁSortedSetǁdifference_update__mutmut_2, 
        'xǁSortedSetǁdifference_update__mutmut_3': xǁSortedSetǁdifference_update__mutmut_3, 
        'xǁSortedSetǁdifference_update__mutmut_4': xǁSortedSetǁdifference_update__mutmut_4, 
        'xǁSortedSetǁdifference_update__mutmut_5': xǁSortedSetǁdifference_update__mutmut_5, 
        'xǁSortedSetǁdifference_update__mutmut_6': xǁSortedSetǁdifference_update__mutmut_6, 
        'xǁSortedSetǁdifference_update__mutmut_7': xǁSortedSetǁdifference_update__mutmut_7, 
        'xǁSortedSetǁdifference_update__mutmut_8': xǁSortedSetǁdifference_update__mutmut_8, 
        'xǁSortedSetǁdifference_update__mutmut_9': xǁSortedSetǁdifference_update__mutmut_9, 
        'xǁSortedSetǁdifference_update__mutmut_10': xǁSortedSetǁdifference_update__mutmut_10, 
        'xǁSortedSetǁdifference_update__mutmut_11': xǁSortedSetǁdifference_update__mutmut_11
    }
    xǁSortedSetǁdifference_update__mutmut_orig.__name__ = 'xǁSortedSetǁdifference_update'

    __isub__ = difference_update

    def intersection(self, *iterables):
        args = [*iterables]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁintersection__mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁintersection__mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁintersection__mutmut_orig(self, *iterables):
        """Return the intersection of two or more sets as a new sorted set.

        The `intersection` method also corresponds to operator ``&``.

        ``ss.__and__(iterable)`` <==> ``ss & iterable``

        The intersection is all values that are in this sorted set and each of
        the other `iterables`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.intersection([4, 5, 6, 7])
        SortedSet([4, 5])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        intersect = self._set.intersection(*iterables)
        return self._fromset(intersect, key=self._key)

    def xǁSortedSetǁintersection__mutmut_1(self, *iterables):
        """Return the intersection of two or more sets as a new sorted set.

        The `intersection` method also corresponds to operator ``&``.

        ``ss.__and__(iterable)`` <==> ``ss & iterable``

        The intersection is all values that are in this sorted set and each of
        the other `iterables`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.intersection([4, 5, 6, 7])
        SortedSet([4, 5])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        intersect = None
        return self._fromset(intersect, key=self._key)

    def xǁSortedSetǁintersection__mutmut_2(self, *iterables):
        """Return the intersection of two or more sets as a new sorted set.

        The `intersection` method also corresponds to operator ``&``.

        ``ss.__and__(iterable)`` <==> ``ss & iterable``

        The intersection is all values that are in this sorted set and each of
        the other `iterables`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.intersection([4, 5, 6, 7])
        SortedSet([4, 5])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        intersect = self._set.intersection(*iterables)
        return self._fromset(None, key=self._key)

    def xǁSortedSetǁintersection__mutmut_3(self, *iterables):
        """Return the intersection of two or more sets as a new sorted set.

        The `intersection` method also corresponds to operator ``&``.

        ``ss.__and__(iterable)`` <==> ``ss & iterable``

        The intersection is all values that are in this sorted set and each of
        the other `iterables`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.intersection([4, 5, 6, 7])
        SortedSet([4, 5])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        intersect = self._set.intersection(*iterables)
        return self._fromset(intersect, key=None)

    def xǁSortedSetǁintersection__mutmut_4(self, *iterables):
        """Return the intersection of two or more sets as a new sorted set.

        The `intersection` method also corresponds to operator ``&``.

        ``ss.__and__(iterable)`` <==> ``ss & iterable``

        The intersection is all values that are in this sorted set and each of
        the other `iterables`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.intersection([4, 5, 6, 7])
        SortedSet([4, 5])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        intersect = self._set.intersection(*iterables)
        return self._fromset(key=self._key)

    def xǁSortedSetǁintersection__mutmut_5(self, *iterables):
        """Return the intersection of two or more sets as a new sorted set.

        The `intersection` method also corresponds to operator ``&``.

        ``ss.__and__(iterable)`` <==> ``ss & iterable``

        The intersection is all values that are in this sorted set and each of
        the other `iterables`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.intersection([4, 5, 6, 7])
        SortedSet([4, 5])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        intersect = self._set.intersection(*iterables)
        return self._fromset(intersect, )
    
    xǁSortedSetǁintersection__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁintersection__mutmut_1': xǁSortedSetǁintersection__mutmut_1, 
        'xǁSortedSetǁintersection__mutmut_2': xǁSortedSetǁintersection__mutmut_2, 
        'xǁSortedSetǁintersection__mutmut_3': xǁSortedSetǁintersection__mutmut_3, 
        'xǁSortedSetǁintersection__mutmut_4': xǁSortedSetǁintersection__mutmut_4, 
        'xǁSortedSetǁintersection__mutmut_5': xǁSortedSetǁintersection__mutmut_5
    }
    xǁSortedSetǁintersection__mutmut_orig.__name__ = 'xǁSortedSetǁintersection'

    __and__ = intersection
    __rand__ = __and__

    def intersection_update(self, *iterables):
        args = [*iterables]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁintersection_update__mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁintersection_update__mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁintersection_update__mutmut_orig(self, *iterables):
        """Update the sorted set with the intersection of `iterables`.

        The `intersection_update` method also corresponds to operator ``&=``.

        ``ss.__iand__(iterable)`` <==> ``ss &= iterable``

        Keep only values found in itself and all `iterables`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.intersection_update([4, 5, 6, 7])
        >>> ss
        SortedSet([4, 5])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        _set.intersection_update(*iterables)
        _list.clear()
        _list.update(_set)
        return self

    def xǁSortedSetǁintersection_update__mutmut_1(self, *iterables):
        """Update the sorted set with the intersection of `iterables`.

        The `intersection_update` method also corresponds to operator ``&=``.

        ``ss.__iand__(iterable)`` <==> ``ss &= iterable``

        Keep only values found in itself and all `iterables`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.intersection_update([4, 5, 6, 7])
        >>> ss
        SortedSet([4, 5])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = None
        _list = self._list
        _set.intersection_update(*iterables)
        _list.clear()
        _list.update(_set)
        return self

    def xǁSortedSetǁintersection_update__mutmut_2(self, *iterables):
        """Update the sorted set with the intersection of `iterables`.

        The `intersection_update` method also corresponds to operator ``&=``.

        ``ss.__iand__(iterable)`` <==> ``ss &= iterable``

        Keep only values found in itself and all `iterables`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.intersection_update([4, 5, 6, 7])
        >>> ss
        SortedSet([4, 5])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = None
        _set.intersection_update(*iterables)
        _list.clear()
        _list.update(_set)
        return self

    def xǁSortedSetǁintersection_update__mutmut_3(self, *iterables):
        """Update the sorted set with the intersection of `iterables`.

        The `intersection_update` method also corresponds to operator ``&=``.

        ``ss.__iand__(iterable)`` <==> ``ss &= iterable``

        Keep only values found in itself and all `iterables`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.intersection_update([4, 5, 6, 7])
        >>> ss
        SortedSet([4, 5])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        _set.intersection_update(*iterables)
        _list.clear()
        _list.update(None)
        return self
    
    xǁSortedSetǁintersection_update__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁintersection_update__mutmut_1': xǁSortedSetǁintersection_update__mutmut_1, 
        'xǁSortedSetǁintersection_update__mutmut_2': xǁSortedSetǁintersection_update__mutmut_2, 
        'xǁSortedSetǁintersection_update__mutmut_3': xǁSortedSetǁintersection_update__mutmut_3
    }
    xǁSortedSetǁintersection_update__mutmut_orig.__name__ = 'xǁSortedSetǁintersection_update'

    __iand__ = intersection_update

    def symmetric_difference(self, other):
        args = [other]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁsymmetric_difference__mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁsymmetric_difference__mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁsymmetric_difference__mutmut_orig(self, other):
        """Return the symmetric difference with `other` as a new sorted set.

        The `symmetric_difference` method also corresponds to operator ``^``.

        ``ss.__xor__(other)`` <==> ``ss ^ other``

        The symmetric difference is all values tha are in exactly one of the
        sets.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.symmetric_difference([4, 5, 6, 7])
        SortedSet([1, 2, 3, 6, 7])

        :param other: `other` iterable
        :return: new sorted set

        """
        diff = self._set.symmetric_difference(other)
        return self._fromset(diff, key=self._key)

    def xǁSortedSetǁsymmetric_difference__mutmut_1(self, other):
        """Return the symmetric difference with `other` as a new sorted set.

        The `symmetric_difference` method also corresponds to operator ``^``.

        ``ss.__xor__(other)`` <==> ``ss ^ other``

        The symmetric difference is all values tha are in exactly one of the
        sets.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.symmetric_difference([4, 5, 6, 7])
        SortedSet([1, 2, 3, 6, 7])

        :param other: `other` iterable
        :return: new sorted set

        """
        diff = None
        return self._fromset(diff, key=self._key)

    def xǁSortedSetǁsymmetric_difference__mutmut_2(self, other):
        """Return the symmetric difference with `other` as a new sorted set.

        The `symmetric_difference` method also corresponds to operator ``^``.

        ``ss.__xor__(other)`` <==> ``ss ^ other``

        The symmetric difference is all values tha are in exactly one of the
        sets.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.symmetric_difference([4, 5, 6, 7])
        SortedSet([1, 2, 3, 6, 7])

        :param other: `other` iterable
        :return: new sorted set

        """
        diff = self._set.symmetric_difference(None)
        return self._fromset(diff, key=self._key)

    def xǁSortedSetǁsymmetric_difference__mutmut_3(self, other):
        """Return the symmetric difference with `other` as a new sorted set.

        The `symmetric_difference` method also corresponds to operator ``^``.

        ``ss.__xor__(other)`` <==> ``ss ^ other``

        The symmetric difference is all values tha are in exactly one of the
        sets.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.symmetric_difference([4, 5, 6, 7])
        SortedSet([1, 2, 3, 6, 7])

        :param other: `other` iterable
        :return: new sorted set

        """
        diff = self._set.symmetric_difference(other)
        return self._fromset(None, key=self._key)

    def xǁSortedSetǁsymmetric_difference__mutmut_4(self, other):
        """Return the symmetric difference with `other` as a new sorted set.

        The `symmetric_difference` method also corresponds to operator ``^``.

        ``ss.__xor__(other)`` <==> ``ss ^ other``

        The symmetric difference is all values tha are in exactly one of the
        sets.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.symmetric_difference([4, 5, 6, 7])
        SortedSet([1, 2, 3, 6, 7])

        :param other: `other` iterable
        :return: new sorted set

        """
        diff = self._set.symmetric_difference(other)
        return self._fromset(diff, key=None)

    def xǁSortedSetǁsymmetric_difference__mutmut_5(self, other):
        """Return the symmetric difference with `other` as a new sorted set.

        The `symmetric_difference` method also corresponds to operator ``^``.

        ``ss.__xor__(other)`` <==> ``ss ^ other``

        The symmetric difference is all values tha are in exactly one of the
        sets.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.symmetric_difference([4, 5, 6, 7])
        SortedSet([1, 2, 3, 6, 7])

        :param other: `other` iterable
        :return: new sorted set

        """
        diff = self._set.symmetric_difference(other)
        return self._fromset(key=self._key)

    def xǁSortedSetǁsymmetric_difference__mutmut_6(self, other):
        """Return the symmetric difference with `other` as a new sorted set.

        The `symmetric_difference` method also corresponds to operator ``^``.

        ``ss.__xor__(other)`` <==> ``ss ^ other``

        The symmetric difference is all values tha are in exactly one of the
        sets.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.symmetric_difference([4, 5, 6, 7])
        SortedSet([1, 2, 3, 6, 7])

        :param other: `other` iterable
        :return: new sorted set

        """
        diff = self._set.symmetric_difference(other)
        return self._fromset(diff, )
    
    xǁSortedSetǁsymmetric_difference__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁsymmetric_difference__mutmut_1': xǁSortedSetǁsymmetric_difference__mutmut_1, 
        'xǁSortedSetǁsymmetric_difference__mutmut_2': xǁSortedSetǁsymmetric_difference__mutmut_2, 
        'xǁSortedSetǁsymmetric_difference__mutmut_3': xǁSortedSetǁsymmetric_difference__mutmut_3, 
        'xǁSortedSetǁsymmetric_difference__mutmut_4': xǁSortedSetǁsymmetric_difference__mutmut_4, 
        'xǁSortedSetǁsymmetric_difference__mutmut_5': xǁSortedSetǁsymmetric_difference__mutmut_5, 
        'xǁSortedSetǁsymmetric_difference__mutmut_6': xǁSortedSetǁsymmetric_difference__mutmut_6
    }
    xǁSortedSetǁsymmetric_difference__mutmut_orig.__name__ = 'xǁSortedSetǁsymmetric_difference'

    __xor__ = symmetric_difference
    __rxor__ = __xor__

    def symmetric_difference_update(self, other):
        args = [other]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁsymmetric_difference_update__mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁsymmetric_difference_update__mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁsymmetric_difference_update__mutmut_orig(self, other):
        """Update the sorted set with the symmetric difference with `other`.

        The `symmetric_difference_update` method also corresponds to operator
        ``^=``.

        ``ss.__ixor__(other)`` <==> ``ss ^= other``

        Keep only values found in exactly one of itself and `other`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.symmetric_difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 6, 7])

        :param other: `other` iterable
        :return: itself

        """
        _set = self._set
        _list = self._list
        _set.symmetric_difference_update(other)
        _list.clear()
        _list.update(_set)
        return self

    def xǁSortedSetǁsymmetric_difference_update__mutmut_1(self, other):
        """Update the sorted set with the symmetric difference with `other`.

        The `symmetric_difference_update` method also corresponds to operator
        ``^=``.

        ``ss.__ixor__(other)`` <==> ``ss ^= other``

        Keep only values found in exactly one of itself and `other`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.symmetric_difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 6, 7])

        :param other: `other` iterable
        :return: itself

        """
        _set = None
        _list = self._list
        _set.symmetric_difference_update(other)
        _list.clear()
        _list.update(_set)
        return self

    def xǁSortedSetǁsymmetric_difference_update__mutmut_2(self, other):
        """Update the sorted set with the symmetric difference with `other`.

        The `symmetric_difference_update` method also corresponds to operator
        ``^=``.

        ``ss.__ixor__(other)`` <==> ``ss ^= other``

        Keep only values found in exactly one of itself and `other`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.symmetric_difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 6, 7])

        :param other: `other` iterable
        :return: itself

        """
        _set = self._set
        _list = None
        _set.symmetric_difference_update(other)
        _list.clear()
        _list.update(_set)
        return self

    def xǁSortedSetǁsymmetric_difference_update__mutmut_3(self, other):
        """Update the sorted set with the symmetric difference with `other`.

        The `symmetric_difference_update` method also corresponds to operator
        ``^=``.

        ``ss.__ixor__(other)`` <==> ``ss ^= other``

        Keep only values found in exactly one of itself and `other`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.symmetric_difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 6, 7])

        :param other: `other` iterable
        :return: itself

        """
        _set = self._set
        _list = self._list
        _set.symmetric_difference_update(None)
        _list.clear()
        _list.update(_set)
        return self

    def xǁSortedSetǁsymmetric_difference_update__mutmut_4(self, other):
        """Update the sorted set with the symmetric difference with `other`.

        The `symmetric_difference_update` method also corresponds to operator
        ``^=``.

        ``ss.__ixor__(other)`` <==> ``ss ^= other``

        Keep only values found in exactly one of itself and `other`.

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.symmetric_difference_update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 6, 7])

        :param other: `other` iterable
        :return: itself

        """
        _set = self._set
        _list = self._list
        _set.symmetric_difference_update(other)
        _list.clear()
        _list.update(None)
        return self
    
    xǁSortedSetǁsymmetric_difference_update__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁsymmetric_difference_update__mutmut_1': xǁSortedSetǁsymmetric_difference_update__mutmut_1, 
        'xǁSortedSetǁsymmetric_difference_update__mutmut_2': xǁSortedSetǁsymmetric_difference_update__mutmut_2, 
        'xǁSortedSetǁsymmetric_difference_update__mutmut_3': xǁSortedSetǁsymmetric_difference_update__mutmut_3, 
        'xǁSortedSetǁsymmetric_difference_update__mutmut_4': xǁSortedSetǁsymmetric_difference_update__mutmut_4
    }
    xǁSortedSetǁsymmetric_difference_update__mutmut_orig.__name__ = 'xǁSortedSetǁsymmetric_difference_update'

    __ixor__ = symmetric_difference_update

    def union(self, *iterables):
        args = [*iterables]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁunion__mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁunion__mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁunion__mutmut_orig(self, *iterables):
        """Return new sorted set with values from itself and all `iterables`.

        The `union` method also corresponds to operator ``|``.

        ``ss.__or__(iterable)`` <==> ``ss | iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.union([4, 5, 6, 7])
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        return self.__class__(chain(iter(self), *iterables), key=self._key)

    def xǁSortedSetǁunion__mutmut_1(self, *iterables):
        """Return new sorted set with values from itself and all `iterables`.

        The `union` method also corresponds to operator ``|``.

        ``ss.__or__(iterable)`` <==> ``ss | iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.union([4, 5, 6, 7])
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        return self.__class__(None, key=self._key)

    def xǁSortedSetǁunion__mutmut_2(self, *iterables):
        """Return new sorted set with values from itself and all `iterables`.

        The `union` method also corresponds to operator ``|``.

        ``ss.__or__(iterable)`` <==> ``ss | iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.union([4, 5, 6, 7])
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        return self.__class__(chain(iter(self), *iterables), key=None)

    def xǁSortedSetǁunion__mutmut_3(self, *iterables):
        """Return new sorted set with values from itself and all `iterables`.

        The `union` method also corresponds to operator ``|``.

        ``ss.__or__(iterable)`` <==> ``ss | iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.union([4, 5, 6, 7])
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        return self.__class__(key=self._key)

    def xǁSortedSetǁunion__mutmut_4(self, *iterables):
        """Return new sorted set with values from itself and all `iterables`.

        The `union` method also corresponds to operator ``|``.

        ``ss.__or__(iterable)`` <==> ``ss | iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.union([4, 5, 6, 7])
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        return self.__class__(chain(iter(self), *iterables), )

    def xǁSortedSetǁunion__mutmut_5(self, *iterables):
        """Return new sorted set with values from itself and all `iterables`.

        The `union` method also corresponds to operator ``|``.

        ``ss.__or__(iterable)`` <==> ``ss | iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.union([4, 5, 6, 7])
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        return self.__class__(chain(None, *iterables), key=self._key)

    def xǁSortedSetǁunion__mutmut_6(self, *iterables):
        """Return new sorted set with values from itself and all `iterables`.

        The `union` method also corresponds to operator ``|``.

        ``ss.__or__(iterable)`` <==> ``ss | iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.union([4, 5, 6, 7])
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        return self.__class__(chain(*iterables), key=self._key)

    def xǁSortedSetǁunion__mutmut_7(self, *iterables):
        """Return new sorted set with values from itself and all `iterables`.

        The `union` method also corresponds to operator ``|``.

        ``ss.__or__(iterable)`` <==> ``ss | iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.union([4, 5, 6, 7])
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        return self.__class__(chain(iter(self), ), key=self._key)

    def xǁSortedSetǁunion__mutmut_8(self, *iterables):
        """Return new sorted set with values from itself and all `iterables`.

        The `union` method also corresponds to operator ``|``.

        ``ss.__or__(iterable)`` <==> ``ss | iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> ss.union([4, 5, 6, 7])
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: new sorted set

        """
        return self.__class__(chain(iter(None), *iterables), key=self._key)
    
    xǁSortedSetǁunion__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁunion__mutmut_1': xǁSortedSetǁunion__mutmut_1, 
        'xǁSortedSetǁunion__mutmut_2': xǁSortedSetǁunion__mutmut_2, 
        'xǁSortedSetǁunion__mutmut_3': xǁSortedSetǁunion__mutmut_3, 
        'xǁSortedSetǁunion__mutmut_4': xǁSortedSetǁunion__mutmut_4, 
        'xǁSortedSetǁunion__mutmut_5': xǁSortedSetǁunion__mutmut_5, 
        'xǁSortedSetǁunion__mutmut_6': xǁSortedSetǁunion__mutmut_6, 
        'xǁSortedSetǁunion__mutmut_7': xǁSortedSetǁunion__mutmut_7, 
        'xǁSortedSetǁunion__mutmut_8': xǁSortedSetǁunion__mutmut_8
    }
    xǁSortedSetǁunion__mutmut_orig.__name__ = 'xǁSortedSetǁunion'

    __or__ = union
    __ror__ = __or__

    def update(self, *iterables):
        args = [*iterables]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁupdate__mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁupdate__mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁupdate__mutmut_orig(self, *iterables):
        """Update the sorted set adding values from all `iterables`.

        The `update` method also corresponds to operator ``|=``.

        ``ss.__ior__(iterable)`` <==> ``ss |= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (4 * len(values)) > len(_set):
            _list = self._list
            _set.update(values)
            _list.clear()
            _list.update(_set)
        else:
            _add = self._add
            for value in values:
                _add(value)
        return self

    def xǁSortedSetǁupdate__mutmut_1(self, *iterables):
        """Update the sorted set adding values from all `iterables`.

        The `update` method also corresponds to operator ``|=``.

        ``ss.__ior__(iterable)`` <==> ``ss |= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = None
        _list = self._list
        values = set(chain(*iterables))
        if (4 * len(values)) > len(_set):
            _list = self._list
            _set.update(values)
            _list.clear()
            _list.update(_set)
        else:
            _add = self._add
            for value in values:
                _add(value)
        return self

    def xǁSortedSetǁupdate__mutmut_2(self, *iterables):
        """Update the sorted set adding values from all `iterables`.

        The `update` method also corresponds to operator ``|=``.

        ``ss.__ior__(iterable)`` <==> ``ss |= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = None
        values = set(chain(*iterables))
        if (4 * len(values)) > len(_set):
            _list = self._list
            _set.update(values)
            _list.clear()
            _list.update(_set)
        else:
            _add = self._add
            for value in values:
                _add(value)
        return self

    def xǁSortedSetǁupdate__mutmut_3(self, *iterables):
        """Update the sorted set adding values from all `iterables`.

        The `update` method also corresponds to operator ``|=``.

        ``ss.__ior__(iterable)`` <==> ``ss |= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = None
        if (4 * len(values)) > len(_set):
            _list = self._list
            _set.update(values)
            _list.clear()
            _list.update(_set)
        else:
            _add = self._add
            for value in values:
                _add(value)
        return self

    def xǁSortedSetǁupdate__mutmut_4(self, *iterables):
        """Update the sorted set adding values from all `iterables`.

        The `update` method also corresponds to operator ``|=``.

        ``ss.__ior__(iterable)`` <==> ``ss |= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(None)
        if (4 * len(values)) > len(_set):
            _list = self._list
            _set.update(values)
            _list.clear()
            _list.update(_set)
        else:
            _add = self._add
            for value in values:
                _add(value)
        return self

    def xǁSortedSetǁupdate__mutmut_5(self, *iterables):
        """Update the sorted set adding values from all `iterables`.

        The `update` method also corresponds to operator ``|=``.

        ``ss.__ior__(iterable)`` <==> ``ss |= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (4 / len(values)) > len(_set):
            _list = self._list
            _set.update(values)
            _list.clear()
            _list.update(_set)
        else:
            _add = self._add
            for value in values:
                _add(value)
        return self

    def xǁSortedSetǁupdate__mutmut_6(self, *iterables):
        """Update the sorted set adding values from all `iterables`.

        The `update` method also corresponds to operator ``|=``.

        ``ss.__ior__(iterable)`` <==> ``ss |= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (5 * len(values)) > len(_set):
            _list = self._list
            _set.update(values)
            _list.clear()
            _list.update(_set)
        else:
            _add = self._add
            for value in values:
                _add(value)
        return self

    def xǁSortedSetǁupdate__mutmut_7(self, *iterables):
        """Update the sorted set adding values from all `iterables`.

        The `update` method also corresponds to operator ``|=``.

        ``ss.__ior__(iterable)`` <==> ``ss |= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (4 * len(values)) >= len(_set):
            _list = self._list
            _set.update(values)
            _list.clear()
            _list.update(_set)
        else:
            _add = self._add
            for value in values:
                _add(value)
        return self

    def xǁSortedSetǁupdate__mutmut_8(self, *iterables):
        """Update the sorted set adding values from all `iterables`.

        The `update` method also corresponds to operator ``|=``.

        ``ss.__ior__(iterable)`` <==> ``ss |= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (4 * len(values)) > len(_set):
            _list = None
            _set.update(values)
            _list.clear()
            _list.update(_set)
        else:
            _add = self._add
            for value in values:
                _add(value)
        return self

    def xǁSortedSetǁupdate__mutmut_9(self, *iterables):
        """Update the sorted set adding values from all `iterables`.

        The `update` method also corresponds to operator ``|=``.

        ``ss.__ior__(iterable)`` <==> ``ss |= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (4 * len(values)) > len(_set):
            _list = self._list
            _set.update(None)
            _list.clear()
            _list.update(_set)
        else:
            _add = self._add
            for value in values:
                _add(value)
        return self

    def xǁSortedSetǁupdate__mutmut_10(self, *iterables):
        """Update the sorted set adding values from all `iterables`.

        The `update` method also corresponds to operator ``|=``.

        ``ss.__ior__(iterable)`` <==> ``ss |= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (4 * len(values)) > len(_set):
            _list = self._list
            _set.update(values)
            _list.clear()
            _list.update(None)
        else:
            _add = self._add
            for value in values:
                _add(value)
        return self

    def xǁSortedSetǁupdate__mutmut_11(self, *iterables):
        """Update the sorted set adding values from all `iterables`.

        The `update` method also corresponds to operator ``|=``.

        ``ss.__ior__(iterable)`` <==> ``ss |= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (4 * len(values)) > len(_set):
            _list = self._list
            _set.update(values)
            _list.clear()
            _list.update(_set)
        else:
            _add = None
            for value in values:
                _add(value)
        return self

    def xǁSortedSetǁupdate__mutmut_12(self, *iterables):
        """Update the sorted set adding values from all `iterables`.

        The `update` method also corresponds to operator ``|=``.

        ``ss.__ior__(iterable)`` <==> ``ss |= iterable``

        >>> ss = SortedSet([1, 2, 3, 4, 5])
        >>> _ = ss.update([4, 5, 6, 7])
        >>> ss
        SortedSet([1, 2, 3, 4, 5, 6, 7])

        :param iterables: iterable arguments
        :return: itself

        """
        _set = self._set
        _list = self._list
        values = set(chain(*iterables))
        if (4 * len(values)) > len(_set):
            _list = self._list
            _set.update(values)
            _list.clear()
            _list.update(_set)
        else:
            _add = self._add
            for value in values:
                _add(None)
        return self
    
    xǁSortedSetǁupdate__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁupdate__mutmut_1': xǁSortedSetǁupdate__mutmut_1, 
        'xǁSortedSetǁupdate__mutmut_2': xǁSortedSetǁupdate__mutmut_2, 
        'xǁSortedSetǁupdate__mutmut_3': xǁSortedSetǁupdate__mutmut_3, 
        'xǁSortedSetǁupdate__mutmut_4': xǁSortedSetǁupdate__mutmut_4, 
        'xǁSortedSetǁupdate__mutmut_5': xǁSortedSetǁupdate__mutmut_5, 
        'xǁSortedSetǁupdate__mutmut_6': xǁSortedSetǁupdate__mutmut_6, 
        'xǁSortedSetǁupdate__mutmut_7': xǁSortedSetǁupdate__mutmut_7, 
        'xǁSortedSetǁupdate__mutmut_8': xǁSortedSetǁupdate__mutmut_8, 
        'xǁSortedSetǁupdate__mutmut_9': xǁSortedSetǁupdate__mutmut_9, 
        'xǁSortedSetǁupdate__mutmut_10': xǁSortedSetǁupdate__mutmut_10, 
        'xǁSortedSetǁupdate__mutmut_11': xǁSortedSetǁupdate__mutmut_11, 
        'xǁSortedSetǁupdate__mutmut_12': xǁSortedSetǁupdate__mutmut_12
    }
    xǁSortedSetǁupdate__mutmut_orig.__name__ = 'xǁSortedSetǁupdate'

    __ior__ = update
    _update = update

    def __reduce__(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁ__reduce____mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁ__reduce____mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁ__reduce____mutmut_orig(self):
        """Support for pickle.

        The tricks played with exposing methods in :func:`SortedSet.__init__`
        confuse pickle so customize the reducer.

        """
        return (type(self), (self._set, self._key))

    def xǁSortedSetǁ__reduce____mutmut_1(self):
        """Support for pickle.

        The tricks played with exposing methods in :func:`SortedSet.__init__`
        confuse pickle so customize the reducer.

        """
        return (type(None), (self._set, self._key))
    
    xǁSortedSetǁ__reduce____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁ__reduce____mutmut_1': xǁSortedSetǁ__reduce____mutmut_1
    }
    xǁSortedSetǁ__reduce____mutmut_orig.__name__ = 'xǁSortedSetǁ__reduce__'

    @recursive_repr()
    def __repr__(self):
        """Return string representation of sorted set.

        ``ss.__repr__()`` <==> ``repr(ss)``

        :return: string representation

        """
        _key = self._key
        key = '' if _key is None else f', key={_key!r}'
        type_name = type(self).__name__
        return f'{type_name}({list(self)!r}{key})'

    def _check(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSortedSetǁ_check__mutmut_orig'), object.__getattribute__(self, 'xǁSortedSetǁ_check__mutmut_mutants'), args, kwargs, self)

    def xǁSortedSetǁ_check__mutmut_orig(self):
        """Check invariants of sorted set.

        Runtime complexity: `O(n)`

        """
        _set = self._set
        _list = self._list
        _list._check()
        assert len(_set) == len(_list)
        assert all(value in _set for value in _list)

    def xǁSortedSetǁ_check__mutmut_1(self):
        """Check invariants of sorted set.

        Runtime complexity: `O(n)`

        """
        _set = None
        _list = self._list
        _list._check()
        assert len(_set) == len(_list)
        assert all(value in _set for value in _list)

    def xǁSortedSetǁ_check__mutmut_2(self):
        """Check invariants of sorted set.

        Runtime complexity: `O(n)`

        """
        _set = self._set
        _list = None
        _list._check()
        assert len(_set) == len(_list)
        assert all(value in _set for value in _list)

    def xǁSortedSetǁ_check__mutmut_3(self):
        """Check invariants of sorted set.

        Runtime complexity: `O(n)`

        """
        _set = self._set
        _list = self._list
        _list._check()
        assert len(_set) != len(_list)
        assert all(value in _set for value in _list)

    def xǁSortedSetǁ_check__mutmut_4(self):
        """Check invariants of sorted set.

        Runtime complexity: `O(n)`

        """
        _set = self._set
        _list = self._list
        _list._check()
        assert len(_set) == len(_list)
        assert all(None)

    def xǁSortedSetǁ_check__mutmut_5(self):
        """Check invariants of sorted set.

        Runtime complexity: `O(n)`

        """
        _set = self._set
        _list = self._list
        _list._check()
        assert len(_set) == len(_list)
        assert all(value not in _set for value in _list)
    
    xǁSortedSetǁ_check__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSortedSetǁ_check__mutmut_1': xǁSortedSetǁ_check__mutmut_1, 
        'xǁSortedSetǁ_check__mutmut_2': xǁSortedSetǁ_check__mutmut_2, 
        'xǁSortedSetǁ_check__mutmut_3': xǁSortedSetǁ_check__mutmut_3, 
        'xǁSortedSetǁ_check__mutmut_4': xǁSortedSetǁ_check__mutmut_4, 
        'xǁSortedSetǁ_check__mutmut_5': xǁSortedSetǁ_check__mutmut_5
    }
    xǁSortedSetǁ_check__mutmut_orig.__name__ = 'xǁSortedSetǁ_check'
