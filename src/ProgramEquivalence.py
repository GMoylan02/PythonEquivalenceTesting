import inspect
import UniversalStrategy
import os
from types import ModuleType
from typing import Callable, Dict
from src.SampleCodeForEquivTest import TestFunctions
from src.UniversalStrategy import run_and_test_equivalence
from src.programs.inequiv import (call_nested_param_ineq_B,
                                  call_nested_param_ineq_A,
                                  holik_file_lock_param_e_large_A,
                                  holik_file_lock_param_e_large_B)
import sys
from StateUtils import snapshot_module_state, restore_module_state
from hypothesis.stateful import RuleBasedStateMachine, rule, consumes
from hypothesis.stateful import multiple
from hypothesis import strategies as st
from UniversalStrategy import are_equivalent, run, build_args_strategy, instantiate_args, assert_equivalent
from hypothesis import event


def get_module_functions(module: ModuleType) -> Dict[str, Callable]:
    module_file = os.path.abspath(module.__file__)

    functions = {
        name: fn
        for name, fn in inspect.getmembers(module, inspect.isfunction)
        if inspect.getsourcefile(fn) == module_file
    }

    return functions


def create_stateful_tester(module_a, module_b):
    """
    Returns a Hypothesis RuleBasedStateMachine class configured to
    test the two modules against each other in sequences
    """
    funcs_a = get_module_functions(module_a)
    funcs_b = get_module_functions(module_b)

    common_names = sorted(list(set(funcs_a.keys()) & set(funcs_b.keys())))
    if not common_names:
        raise ValueError("No common functions found between modules")

    arg_strategies = {
        name: build_args_strategy(funcs_a[name])
        for name in common_names
    }

    snap_a = snapshot_module_state(module_a)
    snap_b = snapshot_module_state(module_b)

    class ProgramEquivalenceMachine(RuleBasedStateMachine):

        def __init__(self):
            super().__init__()
            restore_module_state(module_a, snap_a)
            restore_module_state(module_b, snap_b)

        @rule(
            data=st.data(),
            fn_name=st.sampled_from(common_names)
        )
        def call_function(self, data, fn_name):
            raw_args, raw_kwargs = data.draw(
                arg_strategies[fn_name],
                label=f"args_for_{fn_name}"
            )
            run_and_test_equivalence(funcs_a[fn_name], funcs_b[fn_name], raw_args, raw_kwargs, data)

    return ProgramEquivalenceMachine


EquivalenceStateMachine = create_stateful_tester(holik_file_lock_param_e_large_A, holik_file_lock_param_e_large_B)

class TestProgramEquivalence(EquivalenceStateMachine.TestCase):
    pass