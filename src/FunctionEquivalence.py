import sys

from hypothesis import given, settings

from src.EquivalenceChecker import run_and_test_equivalence
from src.FuzzingStrategy import build_args_strategy
from src.Profiler import record_failure
from src.StateUtils import snapshot_module_state, restore_module_state
from hypothesis.strategies import data as st_data


def make_function_equivalence_test(func_a, func_b, reset_module_state=False, log_failure=False):
    input_strategy = build_args_strategy(func_a)

    module_a = sys.modules.get(func_a.__module__)
    module_b = sys.modules.get(func_b.__module__)

    unique_test_id = f"{func_a.__name__}_{func_b.__name__}"

    if reset_module_state:
        snap_a = snapshot_module_state(module_a) if module_a else {}
        snap_b = snapshot_module_state(module_b) if module_b else {}

    # todo add module wide global state check (not applicable to hobbit suite)

    @given(input_strategy, st_data())
    @settings(max_examples=1000, deadline=None)
    def equivalence_test(inputs, data):
        if reset_module_state:
            if module_a: restore_module_state(module_a, snap_a)
            if module_b: restore_module_state(module_b, snap_b)
        raw_args, raw_kwargs = inputs
        if log_failure:
            try:
                run_and_test_equivalence(func_a, func_b, raw_args, raw_kwargs, data)
            except AssertionError as e:
                record_failure(module_a.__name__, e, unique_test_id)
                raise
        else:
            run_and_test_equivalence(func_a, func_b, raw_args, raw_kwargs, data)

    return equivalence_test