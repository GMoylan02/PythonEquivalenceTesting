import sys
from typing import Optional, Callable

from hypothesis import given, settings

from src.EquivalenceChecker import EquivalenceChecker
from src.FuzzingStrategy import build_args_strategy, configure
from src.Profiler import record_failure, CoverageRecorder
from src.StateUtils import snapshot_module_state, restore_module_state
from hypothesis.strategies import data as st_data


def make_function_equivalence_test(func_a, func_b, reset_module_state=False, log_failure=False,
    coverage_target_func: Optional[Callable] = None, coverage_recorder: CoverageRecorder=None, higher_order=True):
    configure(higher_order=higher_order)
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
        if coverage_recorder:
            coverage_recorder.increment_iterations()
        raw_args, raw_kwargs = inputs
        checker = EquivalenceChecker(
            func_a, func_b, data,
            coverage_target=coverage_target_func,
        )
        try:
            checker.check(raw_args, raw_kwargs)
        except AssertionError as e:
            if log_failure:
                record_failure(module_a.__name__, e, unique_test_id)
            raise
        finally:
            if coverage_recorder and checker.covered_lines:
                coverage_recorder.merge(checker.covered_lines)

    return equivalence_test