import inspect
import string
from typing import Callable, get_origin, get_args
from hypothesis import given, strategies as st
from src.TestFunctions import quickSort, add_A, add_B, add_C, add_D, mergeSort, dedupe_correct, dedupe_buggy
from src.misc.TypeInference import infer_argument_types

"""
This file implements a very basic general equivalence check across
any two functions.

It is assumed that both functions have the same parity, with near equivalent
argument types. (e.g number types tend to all get treated the same)
"""

def strategy(param):
    if param is int:
        return st.integers(-1000, 1000)
    if param is float:
        return st.floats(allow_nan=False, allow_infinity=False)
    if param is bool:
        return st.booleans()
    if param is str:
        return st.text(string.ascii_letters)

    origin = get_origin(param)
    args = get_args(param)
    if origin is list:
        if len(args) == 1:
            return st.lists(strategy(args[0]), max_size=10)
        else:
            return st.lists(st.one_of(*(strategy(a) for a in args)), max_size=10)
    if origin is tuple and len(args) > 0:
        return st.tuples(*(strategy(a) for a in args))
    if origin is dict and len(args) == 2:
        key_s, val_s = strategy(args[0]), strategy(args[1])
        return st.dictionaries(key_s, val_s, max_size=10)
    if origin is set and len(args) == 1:
        return st.sets(strategy(args[0]), max_size=10)
    if origin is set:
        if len(args) == 1:
            return st.sets(strategy(args[0]), max_size=10)
        else:
            return st.sets(st.one_of(*(strategy(a) for a in args)), max_size=10)
    return st.none()


def build_args(func: Callable):
    signature = inspect.signature(func)
    # {funcName: parameterType}
    strats = {}
    for name, param in signature.parameters.items():
        if param.annotation is not inspect._empty:
            strats[name] = strategy(param.annotation)
            #strats.append(strategy(param.annotation))
        else:
            strats[name] = None
            #strats.append(st.none())
    return strats

def generate_equivalence_test(f1, f2, filename):
    """Simple equivalence test generator
        Assumes equal arity and parameters across f1 and f2
        Ignore side effects"""
    # Should add check that strategy across f1 and f2 is equivalent or comparable in some way
    strategy = build_args(f1)
    python_code = ""
    with open(filename, "r", encoding="utf-8") as f:
        python_code = f.read()
    argument_types = infer_argument_types(python_code, f1.__name__)
    print(argument_types)

    for argument in argument_types.keys():
        print(argument)
        print(argument_types[argument])
        try:
            match argument_types[argument]:
                case "int":
                    strategy[argument] = st.integers(-1000, 1000)
                case "float":
                    strategy[argument] = st.floats(allow_nan=False, allow_infinity=False)
                case "bool":
                    strategy[argument] = st.booleans()
                case "str":
                    strategy[argument] = st.text(string.ascii_letters)
                case "list":
                    print('got here')
                    strategy[argument] = st.lists()
                case "tuple":
                    strategy[argument] = st.tuples()
                case "dict":
                    strategy[argument] = st.dictionaries()
                case "set":
                    strategy[argument] = st.sets()
            #strategy[argument] = argument_types[argument]
        except KeyError as e:
            print(f"Expected argument {argument} not found in function {f1.__name__}")
    #print(strategy)

    #strategy = infer_strategy(f1)
    print(f"strategy = {strategy}")
    # TODO finish


    @given(strategy)
    def test(args):
        try:
            return1 = f1(*args)
        except Exception as e:
            ex1 = type(e)
        else:
            ex1 = None

        try:
            return2 = f2(*args)
        except Exception as e:
            ex2 = type(e)
        else:
            ex2 = None

        if ex1 is None and ex2 is None:
            assert return1 == return2
        else:
            assert ex1 == ex2
    return test



# Fails as both functions are not equivalent
#test = generate_equivalence_test(add_A, add_B)

"""For this example, the test arguments are generated based on add_C which takes 
a float. This test still passes though since floats can be passed into add_A just
fine. Type annotations aren't enforced in any way by python."""
#test2 = generate_equivalence_test(add_C, add_A)

# With the current implementation, this causes hypofuzz to crash as add_D takes a string
#test3 = generate_equivalence_test(add_D, add_A)

#testSort = generate_equivalence_test(quickSort, mergeSort)

#testDedupe = generate_equivalence_test(dedupe_correct, dedupe_buggy)
#infer_strategy(quickSort)

test = generate_equivalence_test(dedupe_correct, dedupe_buggy, "../TestFunctions.py")








