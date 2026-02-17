from pathlib import Path

from hypothesis import given, strategies as st, settings, Phase, assume, event, HealthCheck
from hypothesis.strategies import data as st_data
import inspect
import os
from types import ModuleType
from typing import Callable, Dict


import random
from src.EquivTestingExceptions import ClassMethodMismatch
from src.Profiler import return_value_equivalence, record_failure
from src.StateUtils import snapshot_module_state, restore_module_state
from src.UniversalStrategy import build_args_strategy, run_and_test_equivalence
import importlib
import sys


def get_module_functions(module: ModuleType) -> Dict[str, Callable]:
    functions = {
        name: fn
        for name, fn in inspect.getmembers(module, inspect.isfunction)
        if fn.__module__ == module.__name__
    }

    return functions


def get_module_methods(module):
    """
        Returns a dictionary of all functions and class methods in the module.
        Keys are 'FunctionName' or 'ClassName.MethodName'.
        """
    found_funcs = {}

    # 1. Scan Top-Level Functions
    for name, obj in inspect.getmembers(module, inspect.isfunction):
        found_funcs[name] = obj

    # 2. Scan Classes
    for cls_name, cls_obj in inspect.getmembers(module, inspect.isclass):
        # Only scan classes defined in this module (skip imports)
        if cls_obj.__module__ != module.__name__:
            continue

        # Scan methods inside the class
        for method_name, method_obj in inspect.getmembers(cls_obj):
            # We want functions (unbound methods)
            if inspect.isfunction(method_obj) or inspect.ismethod(method_obj):
                # Create a unique key: "ClassName.MethodName"
                key_name = f"{cls_name}.{method_name}"
                found_funcs[key_name] = method_obj

    return found_funcs

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
        snap_a = snapshot_module_state(module_a) if module_a and reset_state else {}
        snap_b = snapshot_module_state(module_b) if module_b and reset_state else {}

        unique_test_id = f"{module_a.__name__}_{module_b.__name__}"
        try:
            METHOD = 0
            ARGS = 1
            paired_funcs = pair_functions(module_a, module_b)

            for op in ops:
                func_name = op[METHOD]
                func_a, func_b = paired_funcs[func_name]
                raw_args, raw_kwargs = op[ARGS]
                run_and_test_equivalence(func_a, func_b, raw_args, raw_kwargs, data)

                if reset_state:
                    current_state_a = snapshot_module_state(module_a) if module_a else {}
                    current_state_b = snapshot_module_state(module_b) if module_b else {}
                    if not return_value_equivalence(current_state_a, current_state_b):
                        msg = (f"State Divergence in {func_name}:\n"
                               f"A: {current_state_a}\n"
                               f"B: {current_state_b}")
                        event(msg)
                        raise AssertionError(msg)

        except AssertionError as e:
            record_failure(module_a.__name__, e, unique_test_id)
            raise

        finally:
            if reset_state:
                if module_a: restore_module_state(module_a, snap_a)
                if module_b: restore_module_state(module_b, snap_b)

    return test_program_equivalence

#test_fns = create_program_equivalence_test(call_nested_param_ineq_A, call_nested_param_ineq_B, iterations=10)
