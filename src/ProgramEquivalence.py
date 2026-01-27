from hypothesis import given, strategies as st, settings, Phase, assume, event, HealthCheck
from hypothesis.strategies import data as st_data
import inspect
import UniversalStrategy
import os
from types import ModuleType
from typing import Callable, Dict
from programs.inequiv import (holik_file_lock_param_e_large_A,
                              holik_file_lock_param_e_large_B,
                              ex4v1_ineq_A, ex4v1_ineq_B,
                              call_nested_param_ineq_A,
                              call_nested_param_ineq_B)
import random
from src.EquivTestingExceptions import ClassMethodMismatch
from src.programs.Ref import Ref
import importlib
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

def create_program_equivalence_test(module_a: ModuleType, module_b: ModuleType, *, iterations=10):
    paired_funcs = pair_functions(module_a, module_b)
    func_names = list(paired_funcs.keys())
    test_fns = {}

    for i in range(iterations):
        name = random.choice(func_names)
        fn_a, fn_b = paired_funcs[name]

        print(f"Testing function equivalence for: {name}")
        test_fn = UniversalStrategy.make_equivalence_test(fn_a, fn_b, reset_state=True)
        test_fns[i] = test_fn

    return test_fns

test_fns = create_program_equivalence_test(call_nested_param_ineq_A, call_nested_param_ineq_B, iterations=1)
for j in test_fns.keys():
    print(f"running iteration {j}")
    try:
        test_fn = test_fns[j]
        test_fn()
    except:
        print(f"failed iteration {j}")
