import inspect
import sys
from typing import Optional, Callable

from hypothesis import given, strategies as st, settings, event
from hypothesis.strategies import data as st_data
from src.EquivalenceChecker import EquivalenceChecker, run
from src.FuzzingStrategy import build_args_strategy, configure
from src.Profiler import value_equivalence, record_failure, CoverageRecorder
from src.StateUtils import snapshot_object_state


def generate_operation_strategy(obj1, obj2):
    # for now, only consider take non-dunder methods
    all_methods = get_object_methods(obj1)
    # for now, we work with a strict notion of class equivalence, reject if their methods don't align
    # maybe we can come up with something more forgiving in future
    if get_object_methods(obj2) != all_methods:
        # in future, provide more info on the method mismatch
        raise TypeError(f"{obj1.__class__} and {obj2.__class__} have different methods")

    strats = []
    for method in all_methods.keys():
        strats.append(st.tuples(st.just(method), build_args_strategy(getattr(obj1, method))))
    return st.one_of(strats) if strats else None

def generate_sequence_strategy(obj1, obj2, max_size=20):
    operation_strategy = generate_operation_strategy(obj1, obj2)
    if operation_strategy is None:
        # the class has no public methods
        return st.just([])
    sequence_strategy = st.lists(operation_strategy, min_size=1, max_size=max_size)
    return sequence_strategy

def create_class_equivalence_test(class1, class2, max_size=20, coverage_target_func: Optional[Callable] = None,
    coverage_recorder: CoverageRecorder=None, higher_order=True):
    configure(higher_order=higher_order)

    init_strategy = build_args_strategy(class1)
    # create uninitialised instances just for method inspection since we dont actually have constructor args yet
    probe_a = class1.__new__(class1)
    probe_b = class2.__new__(class2)
    sequence_strategy = generate_sequence_strategy(probe_a, probe_b, max_size=max_size)

    @given(init_strategy, sequence_strategy, st_data())
    @settings(max_examples=1000)
    def test_class_equivalence(init_inputs, ops, data):
        """
        ops should be in the form [(method, args), (method, args)]
        """

        init_args, init_kwargs = init_inputs if init_inputs else ((), {})
        if coverage_recorder:
            coverage_recorder.increment_iterations()
        result_a = run(class1, init_args, init_kwargs)
        result_b = run(class2, init_args, init_kwargs,
                       coverage_target_func=coverage_target_func)

        if coverage_recorder and result_b.covered_lines:
            coverage_recorder.increment_method_calls()
            coverage_recorder.merge(result_b.covered_lines)
        if not result_a.ok or not result_b.ok:
            return
        object_a = result_a.value
        object_b = result_b.value

        unique_test_id = f"{class1.__name__}_{class2.__name__}"
        recorded_calls = []
        try:
            state_a = vars(object_a) if hasattr(object_a, '__dict__') else {}
            state_b = vars(object_b) if hasattr(object_b, '__dict__') else {}
            if not value_equivalence(state_a, state_b):
                raise AssertionError(
                    f"Instance state mismatch after construction:\n"
                    f"  {class1.__name__}({init_args}, {init_kwargs}): {state_a}\n"
                    f"  {class2.__name__}({init_args}, {init_kwargs}): {state_b}"
                )

            METHOD = 0
            ARGS = 1

            for op in ops:
                func_name = op[METHOD]
                func_a = getattr(object_a, func_name)
                func_b = getattr(object_b, func_name)
                raw_args, raw_kwargs = op[ARGS]

                checker = EquivalenceChecker(
                    func_a, func_b, data,
                    coverage_target=coverage_target_func,
                )
                try:
                    checker.check(raw_args, raw_kwargs)
                    if coverage_recorder:
                        coverage_recorder.increment_method_calls()
                finally:
                    if coverage_recorder and checker.covered_lines:
                        coverage_recorder.merge(checker.covered_lines)

                # check observable dunders
                _assert_dunder_equivalence(object_a, object_b)
            # also needed here if the class has no actual methods other than dunders (BST.Node for example)
            _assert_dunder_equivalence(object_a, object_b)


        except AssertionError as e:
            if coverage_recorder:
                final_state = vars(object_a) if hasattr(object_a, '__dict__') else {}
                coverage_recorder.record_input_sequence(
                    init_args, init_kwargs,
                    recorded_calls,
                    final_state,
                )
            record_failure(class1.__name__, e, unique_test_id)
            raise

    return test_class_equivalence


def get_object_methods(obj):
    methods = {}
    for name, method in inspect.getmembers(obj, predicate=inspect.ismethod):
        if name.startswith("__") :   # excludes __dunder__
            continue
        sig = inspect.signature(method)
        params = [
            p for p in sig.parameters.values()
            if p.name != "self"
        ]
        methods[name] = len(params)
    return methods

OBSERVABLE_DUNDERS = [
    ("__repr__", repr),
    ("__str__", str),
    ("__len__", len),
    ("__bool__", bool),
]

def _assert_dunder_equivalence(obj_a, obj_b):
    for dunder_name, builtin_fn in OBSERVABLE_DUNDERS:
        # only check if the class explicitly defines it
        if dunder_name not in type(obj_a).__dict__:
            continue
        try:
            val_a = builtin_fn(obj_a)
            val_b = builtin_fn(obj_b)
        except Exception:
            continue
        if not value_equivalence(val_a, val_b):
            raise AssertionError(
                f"{dunder_name} mismatch after method call:\n"
                f"  A: {val_a!r}\n"
                f"  B: {val_b!r}"
            )