import inspect
import math
import re
import sys
from dataclasses import dataclass
from typing import Any, Literal, Callable
from hypothesis import strategies as st, event

from src.DummyObject import DummyObject
from src.FuzzingStrategy import generate_tuple_operation_strategy, build_args_strategy
from src.GenerateFunctions import RecursiveRef, construct_dummies, GlobalMutatorPlan, create_global_mutator, \
    CallablePlan
from src.Profiler import Profiler, logs_are_equivalent, is_user_object, value_equivalence

MAX_CALLABLE_DEPTH = 2
MAX_CALLABLE_CALLS = 20
MAX_TUPLE_CALLS = 30
# exceptions that almost always indicate a bad input rather than a logic divergence
# may cause us to throw away real divergences occasionally
INPUT_TYPE_ERRORS = {
    "not supported between instances of",
    "unsupported operand type",
    "argument must be",
    "must be a",
    "cannot be interpreted as",
    "object is not subscriptable",
    "object is not iterable",
}


@dataclass
class RunResult:
    status: Literal["ok", "err"]
    value: Any
    log: list
    func_name: str

    @property
    def ok(self) -> bool:
        return self.status == "ok"

    @property
    def exc(self) -> Exception | None:
        return self.value if not self.ok else None


def run(fn, args, kwargs=None) -> RunResult:
    profiler = Profiler()
    try:
        sys.settrace(profiler.trace)
        result = fn(*args) if not kwargs else fn(*args, **kwargs)
        if inspect.isgenerator(result):
            result = list(result)
        sys.settrace(None)
        log = profiler.trace_log
        profiler.clear_logs()
        return RunResult("ok", result, log, fn.__name__)
    except Exception as e:
        sys.settrace(None)
        log = profiler.trace_log
        profiler.clear_logs()
        return RunResult("err", e, log, fn.__name__)


class EquivalenceChecker:
    """
    Encapsulates a single differential fuzzing check between two functions.
    Instantiate once per function pair, call check() for each set of arguments.
    """

    def __init__(self, func_a: Callable, func_b: Callable, data):
        self.func_a = func_a
        self.func_b = func_b
        self.data = data
        # we want to treat non-annotated functions less strictly as more likely than not the types we pass in will be
        # problematic. without this, we could have false positives stemming from simple order of operations differences
        self.strict = has_type_annotations(func_a)
        self.equivalent_logs = True
        self.logs_error_msg = ""

    def check(self, raw_args, raw_kwargs) -> None:
        args_a, kwargs_a = instantiate_args(raw_args, raw_kwargs, self.func_a)
        args_b, kwargs_b = instantiate_args(raw_args, raw_kwargs, self.func_b)

        a = run(self.func_a, args_a, kwargs_a)
        b = run(self.func_b, args_b, kwargs_b)

        self.equivalent_logs, self.logs_error_msg = logs_are_equivalent(
            a.log, b.log,
            args_a, args_b,
            kwargs_a, kwargs_b,
            a.func_name, b.func_name,
            strict_exceptions=self.strict,
        )

        # invariants check after the main check in each branch, to ensure event() is called first before exiting
        if a.ok and b.ok:
            self._handle_both_ok(a, args_a, kwargs_a, b, args_b, kwargs_b)
            self._check_shared_invariants(a, args_a, kwargs_a, b, args_b, kwargs_b)
        elif not a.ok and not b.ok:
            self._handle_both_errored(a, args_a, kwargs_a, b, args_b, kwargs_b)
            self._check_shared_invariants(a, args_a, kwargs_a, b, args_b, kwargs_b)
        else:
            self._handle_domain_mismatch(a, args_a, kwargs_a, b, args_b, kwargs_b)


    def _check_shared_invariants(self, a, args_a, kwargs_a, b, args_b, kwargs_b) -> None:
        assert self.equivalent_logs, self.logs_error_msg
        assert_instance_states_equivalent(self.func_a, self.func_b)
        assert_inputs_equivalent(
            self.func_a, self.func_b,
            args_a, args_b,
            kwargs_a, kwargs_b,
        )

    # both returned normally
    def _handle_both_ok(self, a, args_a, kwargs_a, b, args_b, kwargs_b) -> None:
        if callable(a.value) and callable(b.value):
            event("both ok: callable output")
        else:
            event("both ok")

        assert_outputs_equivalent(a.value, b.value, data=self.data)

    # both raised exceptions
    def _handle_both_errored(self, a, args_a, kwargs_a, b, args_b, kwargs_b) -> None:
        # if the inputs were bad (eg wrong type), we don't count it as an inequivalence
        both_bad_input = is_bad_input_exception(a.exc) and is_bad_input_exception(b.exc)
        types_match = type(a.exc) is type(b.exc)

        if not types_match and self.strict and not both_bad_input:
            event("both errored: exception type mismatch")
        else:
            event("both errored: equivalent")

        if self.strict and not both_bad_input:
            assert types_match, (
                f"Exception type mismatch:\n"
                f"  A: {format_call(self.func_a.__name__, args_a, kwargs_a, a.exc)}\n"
                f"  B: {format_call(self.func_b.__name__, args_b, kwargs_b, b.exc)}"
            )

    # one returned normally, one raised an exception
    def _handle_domain_mismatch(self, a, args_a, kwargs_a, b, args_b, kwargs_b) -> None:
        # again, wrongly typed inputs can cause false inequivalences if not guarded for
        errored = b if not b.ok else a
        if is_bad_input_exception(errored.exc):
            event("skipping: bad input TypeError")
            return

        which = "a ok b errored" if a.ok else "b ok a errored"
        event(f"domain mismatch: {which}")
        raise AssertionError(
            f"Domain mismatch:\n"
            f"  A: {format_call(self.func_a.__name__, args_a, kwargs_a, a.value)}\n"
            f"  B: {format_call(self.func_b.__name__, args_b, kwargs_b, b.value)}"
        )


def run_and_test_equivalence(func_a, func_b, raw_args, raw_kwargs, data) -> None:
    EquivalenceChecker(func_a, func_b, data).check(raw_args, raw_kwargs)


def instantiate_value(val, target_func):
    """
    Recursively traverses val. If a RecursiveRef is found, constructs the
    dummy functions bound to target_func and returns the specific index
    """
    if isinstance(val, RecursiveRef):
        dummies = construct_dummies(target_func, limit=val.index + 1)
        return dummies[val.index]

    if isinstance(val, GlobalMutatorPlan):
        return create_global_mutator(target_func, val)

    if isinstance(val, CallablePlan):
        return val.build()

    if isinstance(val, list):
        return [instantiate_value(x, target_func) for x in val]
    if isinstance(val, tuple):
        return tuple(instantiate_value(x, target_func) for x in val)
    if isinstance(val, dict):
        return {k: instantiate_value(v, target_func) for k, v in val.items()}

    return val


def instantiate_args(args, kwargs, target_func):
    return (
        instantiate_value(args, target_func),
        instantiate_value(kwargs, target_func)
    )


def format_call(name, args, kwargs, result):
    args_str = repr(args) if len(repr(args)) < 200 else f"<args len={len(args)}>"
    result_str = repr(result) if len(repr(result)) < 200 else f"<{type(result).__name__}>"
    if kwargs:
        return f"{name}({args_str}, **{kwargs!r}) = {result_str}"
    return f"{name}({args_str}) = {result_str}"


def has_type_annotations(func):
    """Returns True if any parameter of func has a type annotation."""
    try:
        sig = inspect.signature(func)
        return any(
            p.annotation is not inspect.Parameter.empty
            for p in sig.parameters.values()
        )
    except (ValueError, TypeError):
        return False


def is_bad_input_exception(exc):
    """Check if an exception is due to badly typed or malformed input"""
    if not isinstance(exc, TypeError):
        return False
    msg = str(exc)
    return any(phrase in msg for phrase in INPUT_TYPE_ERRORS)


def _is_callable_tuple(val):
    """Given a tuple, returns true if every element is a function"""
    return isinstance(val, tuple) and len(val) > 0 and all(callable(f) for f in val)


def assert_equivalent_callable_tuple(tuple_a, tuple_b, *, data, depth=0):
    """
    Given two tuples of callables that share state internally, test them by
    drawing a random interleaved call sequence and asserting that each paired
    call produces equivalent outputs on both sides.
    """
    if len(tuple_a) != len(tuple_b):
        raise AssertionError(
            f"Returned tuples have different lengths: {len(tuple_a)} vs {len(tuple_b)}"
        )

    # Verify all signatures match pairwise
    for i, (fa, fb) in enumerate(zip(tuple_a, tuple_b)):
        if inspect.signature(fa) != inspect.signature(fb):
            raise AssertionError(
                f"Returned callables at index {i} have different signatures: "
                f"{inspect.signature(fa)} vs {inspect.signature(fb)}"
            )

    operation_strategy = generate_tuple_operation_strategy(tuple_a, tuple_b)
    sequence_strategy = st.lists(operation_strategy, min_size=1, max_size=MAX_TUPLE_CALLS)

    ops = data.draw(sequence_strategy)
    for op in ops:
        idx = op[0]
        raw_args, raw_kwargs = op[1]
        run_and_test_equivalence(tuple_a[idx], tuple_b[idx], raw_args, raw_kwargs, data)


def assert_inputs_equivalent(func_a, func_b, args_a, args_b, kwargs_a, kwargs_b):
    args_equivalent = value_equivalence(args_a, args_b)
    kwargs_equivalent = value_equivalence(kwargs_a, kwargs_b)
    if not args_equivalent or not kwargs_equivalent:
        raise AssertionError(
            f"{func_a.__name__} and {func_b.__name__} have inequivalent arguments after running: "
            f"{args_a!r}, {args_b!r}, {kwargs_a!r}, {kwargs_b!r}"
        )


def assert_outputs_equivalent(
        out_a,
        out_b,
        *,
        data,
        depth=0,
):
    """
    Assert that the outputs from a pair of functions are equivalent when performing differential fuzzing.

    Case 1: The outputs are a pair of tuples of functions - In this case we perform interleaved calls of the functions
        to catch stateful differences in function execution
    Case 2: The outputs are simple values or containers of values - Pass them through value_equivalence
    Case 3: The outputs are both functions - Perform differential fuzzing on both
    """
    if _is_callable_tuple(out_a) and _is_callable_tuple(out_b):
        if depth >= MAX_CALLABLE_DEPTH:
            event("callable tuple depth limit")
            return
        assert_equivalent_callable_tuple(out_a, out_b, data=data, depth=depth)
        return

    if not callable(out_a) or not callable(out_b) or isinstance(out_a, DummyObject) or isinstance(out_b, DummyObject):
        assert value_equivalence(out_a, out_b), f"{out_a!r} != {out_b!r}"
        return

    if depth >= MAX_CALLABLE_DEPTH:
        event("callable depth limit")
        return

    event(f"callable depth {depth}")
    if inspect.signature(out_a) != inspect.signature(out_b):
        raise AssertionError("Returned callables have different signatures")

    input_strategy = build_args_strategy(out_a)

    for _ in range(MAX_CALLABLE_CALLS):
        raw_args, raw_kwargs = data.draw(input_strategy, label=f"callable_args_d{depth}")
        run_and_test_equivalence(out_a, out_b, raw_args, raw_kwargs, data)


def get_instance_state(val):
    """Returns the instance __dict__ if val is a bound method or user object, else None."""
    if inspect.ismethod(val):
        obj = val.__self__
    elif is_user_object(val):
        obj = val
    else:
        return None

    if hasattr(obj, '__slots__'):
        return {slot: getattr(obj, slot) for slot in obj.__slots__ if hasattr(obj, slot)}
    return vars(obj).copy()


def assert_instance_states_equivalent(func_a, func_b):
    """
    If func_a and func_b are bound to an object, assert that every instance variable of their objects are equivalent
    """
    state_a = get_instance_state(func_a)
    state_b = get_instance_state(func_b)

    # neither is a bound method, nothing to check
    if state_a is None and state_b is None:
        return

    # one is a method and one isn't
    if (state_a is None) != (state_b is None):
        raise AssertionError(
            f"One function is a bound method and the other is not: " # todo
            f"{func_a!r} vs {func_b!r}"
        )

    # compare field by field for a useful error message
    all_keys = set(state_a) | set(state_b)
    for key in sorted(all_keys):
        if key not in state_a:
            raise AssertionError(f"Instance state mismatch: key {key!r} only in B")
        if key not in state_b:
            raise AssertionError(f"Instance state mismatch: key {key!r} only in A")

        val_a = state_a[key]
        val_b = state_b[key]

        if not value_equivalence(val_a, val_b):
            raise AssertionError(
                f"Instance state mismatch on field {key!r}: "
                f"{val_a!r} != {val_b!r}"
            )