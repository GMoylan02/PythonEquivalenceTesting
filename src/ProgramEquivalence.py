import inspect
import UniversalStrategy
import os
from types import ModuleType
from typing import Callable, Dict
from src.SampleCodeForEquivTest import TestFunctions
import sys


def get_module_functions(module: ModuleType) -> Dict[str, Callable]:
    module_file = os.path.abspath(module.__file__)

    functions = {
        name: fn
        for name, fn in inspect.getmembers(module, inspect.isfunction)
        if inspect.getsourcefile(fn) == module_file
    }

    return functions

def pair_functions(module_a: ModuleType, module_b: ModuleType):
    funcs_a = get_module_functions(module_a)
    funcs_b = get_module_functions(module_b)

    names_a = set(funcs_a.keys())
    names_b = set(funcs_b.keys())

    if names_a != names_b:
        missing_in_a = names_b - names_a
        missing_in_b = names_a - names_b
        raise ValueError(
            f"Modules have different top-level functions.\n"
            f"Missing in A: {missing_in_a}\n"
            f"Missing in B: {missing_in_b}"
        )
    paired = {name: (funcs_a[name], funcs_b[name]) for name in names_a}
    return paired

def create_program_equivalence_suite(module_a: ModuleType, module_b: ModuleType, *, iterations=10):
    paired_funcs = pair_functions(module_a, module_b)
    test_suite = {}
    for name, (fn_a, fn_b) in paired_funcs.items():

        test_fn = UniversalStrategy.make_equivalence_test(
            fn_a,
            fn_b,
            reset_state=True
        )
        test_suite[name] = test_fn

    return test_suite

test_suite = create_program_equivalence_suite(TestFunctions, TestFunctions)

current_module = sys.modules[__name__]

for func_name, test_func in test_suite.items():
    test_name = f"test_equivalence_{func_name}"

    test_func.__name__ = test_name

    setattr(current_module, test_name, test_func)