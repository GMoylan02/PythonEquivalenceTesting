from pathlib import Path

from hypothesis import given, strategies as st, settings, Phase, assume, event, HealthCheck
from hypothesis.strategies import data as st_data
import inspect
import os
from types import ModuleType
from typing import Callable, Dict


import random
from src.EquivTestingExceptions import ClassMethodMismatch
from src.StateUtils import snapshot_module_state, restore_module_state
from src.UniversalStrategy import build_args_strategy, run_and_test_equivalence
import importlib
import sys


# we currently log failures to count the no. of ineqs in a test suite, this ensures we only log
# once per failure
already_logged = False

FAIL_MARKER = Path("hypofuzz_failures.log")

def record_failure(exc):
    global already_logged
    if not already_logged:
        with FAIL_MARKER.open("a") as f:
            f.write(repr(exc) + "\n")
            already_logged = True


def get_module_functions(module: ModuleType) -> Dict[str, Callable]:
    functions = {
        name: fn
        for name, fn in inspect.getmembers(module, inspect.isfunction)
        if fn.__module__ == module.__name__
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

def generate_operation_strategy(module_a: ModuleType, module_b: ModuleType):
    paired_funcs = pair_functions(module_a, module_b)

    strats = []
    for name in paired_funcs.keys():
        strats.append(st.tuples(st.just(name), build_args_strategy(paired_funcs[name][0])))
    operation_strategy = st.one_of(strats)
    return operation_strategy

def generate_sequence_strategy(module_a: ModuleType, module_b: ModuleType, max_size=20):
    operation_strategy = generate_operation_strategy(module_a, module_b)
    sequence_strategy = st.lists(operation_strategy, min_size=1, max_size=max_size)
    return sequence_strategy

def create_program_equivalence_test(module_a: ModuleType, module_b: ModuleType, *, iterations=10, reset_state=False):
    sequence_strategy = generate_sequence_strategy(module_a, module_b, iterations)

    if reset_state:
        snap_a = snapshot_module_state(module_a) if module_a else {}
        snap_b = snapshot_module_state(module_b) if module_b else {}

    @given(sequence_strategy, st_data())
    @settings(max_examples=500)
    def test_program_equivalence(ops, data):
        """
        ops should be in the form [(method, args), (method, args)]
        """
        try:
            # todo can try to find a way to generalise this slightly, as this pattern is repeated in ClassEquivalence
            if reset_state:
                """
                Some ramblings/examples for global variable equivalence in plain english for my own sanity: 
                
                if module_a alters a global variable x after running n steps, but module_b
                does not alter any global variable x after running n steps, they are INEQUIVALENT.
                
                if they both alter a global variable x in the same way after n steps, they are EQUIVALENT.
                
                if module_a contains the definition of a global variable x, but it does not change, and module_b does not
                define any global variables, then both modules states have changed (or not changed) in the same way and 
                they are INEQUIVALENT.
                
                if module_a alters a global string variable s after running n steps, but module_b alters a global int
                variable x after running n steps, they are INEQUIVALENT.
                
                This can be boiled down to checking if state_A equals state_B after n steps, given 
                neither are the starting state.
                """
                current_state_a = snapshot_module_state(module_a) if module_a else {}
                current_state_b = snapshot_module_state(module_b) if module_b else {}
                if current_state_a != current_state_b and (current_state_a != snap_a and current_state_b != snap_a):
                    # todo also might need to think about nonlocal variables for nested functions
                    event(f"State of {module_a.__name__} and {module_b.__name__} are different")
                    raise AssertionError(f"State of {module_a.__name__} and {module_b.__name__} are different:"
                                         f"{current_state_a} != {current_state_b}")
                if module_a: restore_module_state(module_a, snap_a)
                if module_b: restore_module_state(module_b, snap_b)
            METHOD = 0
            ARGS = 1
            paired_funcs = pair_functions(module_a, module_b)
            for op in ops:
                func_name = op[METHOD]
                func_a, func_b = paired_funcs[func_name]
                raw_args, raw_kwargs = op[ARGS]
                run_and_test_equivalence(func_a, func_b, raw_args, raw_kwargs, data)
        except AssertionError as e:
            record_failure(e)
            raise


    return test_program_equivalence

#test_fns = create_program_equivalence_test(call_nested_param_ineq_A, call_nested_param_ineq_B, iterations=10)
