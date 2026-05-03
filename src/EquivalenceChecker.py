import functools
import inspect
import math
import re
import sys
from dataclasses import dataclass
from typing import Any, Literal, Callable, Optional
from hypothesis import strategies as st, event

from src.DummyObject import DummyObject
from src.FuzzingStrategy import generate_tuple_operation_strategy, build_args_strategy
from src.GenerateFunctions import RecursiveRef, construct_dummies, GlobalMutatorPlan, create_global_mutator, \
    CallablePlan
from src.Profiler import Profiler, logs_are_equivalent, is_user_object, value_equivalence, \
    exception_messages_are_equivalent

MAX_CALLABLE_DEPTH = 2
MAX_CALLABLE_CALLS = 30
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
    "has no len()"
}

# cache function signatures since inspecting is slow
inspect.signature = functools.lru_cache(maxsize=None)(inspect.signature)

@dataclass
class RunResult:
    status: Literal["ok", "err"]
    value: Any
    log: list
    func_name: str
    covered_lines: frozenset = frozenset()  # lines hit in the coverage-target function

    @property
    def ok(self) -> bool:
        return self.status == "ok"

    @property
    def exc(self) -> Exception | None:
        return self.value if not self.ok else None


def run(fn, args, kwargs=None, coverage_target_func=None) -> RunResult:
    """
    Execute fn(*args, **kwargs) under the Profiler tracer
    """
    profiler = Profiler(coverage_target_func=coverage_target_func)

    try:
        sys.settrace(profiler.trace)
        result = fn(*args) if not kwargs else fn(*args, **kwargs)

        if inspect.isgenerator(result):
            result = list(result)

        sys.settrace(None)
        log = profiler.trace_log
        covered = frozenset(profiler.covered_lines)
        profiler.clear_logs()
        return RunResult("ok", result, log, fn.__name__, covered)

    except Exception as e:
        sys.settrace(None)
        log = profiler.trace_log
        covered = frozenset(profiler.covered_lines)
        profiler.clear_logs()
        return RunResult("err", e, log, fn.__name__, covered)


class EquivalenceChecker:
    """
    Encapsulates a single differential fuzzing check between two functions
    Instantiate once per function pair, call check() for each set of arguments
    """

    def __init__(
        self,
        func_a: Callable,
        func_b: Callable,
        data,
        coverage_target: Optional[tuple[str, str]] = None,
    ):
        self.func_a = func_a
        self.func_b = func_b
        self.data = data
        self.coverage_target = coverage_target
        # we want to treat non-annotated functions less strictly as more likely than not the types we pass in will be
        # problematic. without this, we could have false positives stemming from simple order of operations differences
        self.strict = has_type_annotations(func_a)
        self.equivalent_logs = True
        self.logs_error_msg = ""
        self.args_a: tuple = ()
        self.args_b: tuple = ()
        self.kwargs_a: dict = {}
        self.kwargs_b: dict = {}
        # accumulates covered lines across all check() calls
        self.covered_lines: set[int] = set()

    def check(self, raw_args, raw_kwargs) -> None:
        self.args_a, self.kwargs_a = instantiate_args(raw_args, raw_kwargs, self.func_a)
        self.args_b, self.kwargs_b = instantiate_args(raw_args, raw_kwargs, self.func_b)

        a = run(self.func_a, self.args_a, self.kwargs_a)

        # coverage target is always b for experiments
        b = run(self.func_b, self.args_b, self.kwargs_b, coverage_target_func=self.coverage_target)

        self.result_a = a
        self.result_b = b

        # Merge newly-covered lines from this single call
        self.covered_lines.update(b.covered_lines)

        self.equivalent_logs, self.logs_error_msg = logs_are_equivalent(
            a.log, b.log,
            self.args_a, self.args_b,
            self.kwargs_a, self.kwargs_b,
            a.func_name, b.func_name,
            strict_exceptions=self.strict,
        )

        # invariants check after the main check in each branch, to ensure event() is called first before exiting
        if a.ok and b.ok:
            self._handle_both_ok(a, b)
            self._check_shared_invariants()
        elif not a.ok and not b.ok:
            self._handle_both_errored(a, b)
            self._check_shared_invariants()
        else:
            self._handle_domain_mismatch(a, b)

    def _format_a(self, result) -> str:
        return format_call(self.func_a.__name__, self.args_a, self.kwargs_a, result)

    def _format_b(self, result) -> str:
        return format_call(self.func_b.__name__, self.args_b, self.kwargs_b, result)

    def _context_header(self) -> str:
        """One-liner that identifies where a failure occurred"""
        return (
            f"  A: {self._format_a('?')}\n"
            f"  B: {self._format_b('?')}"
        )

    def _check_shared_invariants(self) -> None:
        assert self.equivalent_logs, self.logs_error_msg
        self._assert_instance_states_equivalent()
        self._assert_inputs_equivalent()

    def _assert_inputs_equivalent(self) -> None:
        args_ok = value_equivalence(self.args_a, self.args_b)
        kwargs_ok = value_equivalence(self.kwargs_a, self.kwargs_b)
        if not args_ok or not kwargs_ok:
            raise AssertionError(
                f"{self.func_a.__name__} and {self.func_b.__name__} "
                f"have inequivalent arguments after running:\n"
                f"  A args:   {self.args_a!r}   kwargs: {self.kwargs_a!r}\n"
                f"  B args:   {self.args_b!r}   kwargs: {self.kwargs_b!r}"
            )

    def _assert_instance_states_equivalent(self) -> None:
        state_a = get_instance_state(self.func_a)
        state_b = get_instance_state(self.func_b)

        if state_a is None and state_b is None:
            return

        if (state_a is None) != (state_b is None):
            raise AssertionError(
                f"One function is a bound method and the other is not: "
                f"{self.func_a!r} vs {self.func_b!r}"
            )

        all_keys = set(state_a) | set(state_b)
        for key in sorted(all_keys):
            if key not in state_a:
                raise AssertionError(f"Instance state mismatch: key {key!r} only in B\n{self._context_header()}")
            if key not in state_b:
                raise AssertionError(f"Instance state mismatch: key {key!r} only in A\n{self._context_header()}")
            if not value_equivalence(state_a[key], state_b[key]):
                raise AssertionError(
                    f"Instance state mismatch on field {key!r}: "
                    f"{state_a[key]!r} != {state_b[key]!r}\n"
                    f"{self._context_header()}"
                )

    def _assert_outputs_equivalent(
            self,
            out_a,
            out_b,
            *,
            depth=0,
    ):
        """
        Assert that the outputs from a pair of functions are equivalent when performing differential fuzzing

        Case 1: The outputs are a pair of tuples of functions: case perform interleaved calls of the functions
            to catch stateful differences in function execution
        Case 2: The outputs are simple values or containers of values: pass them through value_equivalence
        Case 3: The outputs are both functions: perform differential fuzzing on both
        """
        if _is_callable_tuple(out_a) and _is_callable_tuple(out_b):
            if depth >= MAX_CALLABLE_DEPTH:
                event("callable tuple depth limit")
                return
            self._assert_equivalent_callable_tuple(out_a, out_b, depth=depth)
            return

        if not callable(out_a) or not callable(out_b) or isinstance(out_a, DummyObject) or isinstance(out_b,
                                                                                                      DummyObject):
            if not value_equivalence(out_a, out_b):
                raise AssertionError(
                    f"Output mismatch:\n"
                    f"  {self._format_a(out_a)}\n"
                    f"  {self._format_b(out_b)}"
                )
            return

        if depth >= MAX_CALLABLE_DEPTH:
            event("callable depth limit")
            return

        event(f"callable depth {depth}")
        if inspect.signature(out_a) != inspect.signature(out_b):
            raise AssertionError(
                f"Returned callables have different signatures:\n"
                f"  {self._format_a(inspect.signature(out_a))}\n"
                f"  {self._format_b(inspect.signature(out_b))}"
            )

        input_strategy = build_args_strategy(out_a)

        for _ in range(MAX_CALLABLE_CALLS):
            raw_args, raw_kwargs = self.data.draw(input_strategy, label=f"callable_args_d{depth}")
            run_and_test_equivalence(out_a, out_b, raw_args, raw_kwargs, self.data,
                                     coverage_target_func=self.coverage_target)

    def _assert_equivalent_callable_tuple(self, tuple_a, tuple_b, *, depth=0):
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

        ops = self.data.draw(sequence_strategy)
        for op in ops:
            idx = op[0]
            raw_args, raw_kwargs = op[1]
            run_and_test_equivalence(tuple_a[idx], tuple_b[idx], raw_args, raw_kwargs, self.data,
                                     coverage_target_func=self.coverage_target)

    # both returned normally
    def _handle_both_ok(self, a, b) -> None:
        if callable(a.value) and callable(b.value):
            event("both ok: callable output")
        else:
            event("both ok")
        self._assert_outputs_equivalent(a.value, b.value)

    def _handle_both_errored(self, a, b) -> None:
        both_bad_input = is_bad_input_exception(a.exc) and is_bad_input_exception(b.exc)
        either_bad_input = is_bad_input_exception(a.exc) or is_bad_input_exception(b.exc)
        types_match = type(a.exc) is type(b.exc)

        if not types_match and self.strict and not both_bad_input:
            event("both errored: exception type mismatch")
        else:
            event("both errored: equivalent")

        if self.strict and not both_bad_input:
            assert types_match, (
                f"Exception type mismatch:\n"
                f"  {self._format_a(a.exc)}\n"
                f"  {self._format_b(b.exc)}"
            )

        if types_match and not either_bad_input:
            msgs_ok, msgs_err = exception_messages_are_equivalent(a.exc, b.exc)
            if not msgs_ok:
                event("both errored: message mismatch")
                raise AssertionError(msgs_err)

    # one returned normally, one raised an exception
    def _handle_domain_mismatch(self, a, b) -> None:
        # again, wrongly typed inputs can cause false inequivalences if not guarded for
        errored = b if not b.ok else a
        if is_bad_input_exception(errored.exc):
            event("skipping: bad input TypeError")
            return

        which = "a ok b errored" if a.ok else "b ok a errored"
        event(f"domain mismatch: {which}")
        raise AssertionError(
            f"Domain mismatch:\n"
            f"  A: {format_call(self.func_a.__name__, self.args_a, self.kwargs_a, a.value)}\n"
            f"  B: {format_call(self.func_b.__name__, self.args_b, self.kwargs_b, b.value)}"
        )


def run_and_test_equivalence(
    func_a,
    func_b,
    raw_args,
    raw_kwargs,
    data,
    coverage_target_func: Optional[Callable] = None,
) -> set[int]:
    """
    Run one differential check and return any newly-covered lines from the mutant
    The returned set should be merged into the caller's long-lived coverage accumulator
    """
    checker = EquivalenceChecker(func_a, func_b, data, coverage_target=coverage_target_func)
    checker.check(raw_args, raw_kwargs)
    return checker.covered_lines


def instantiate_value(val, target_func):
    """
    Recursively traverses val. If a RecursiveRef is found, constructs the
    dummy functions bound to target_func and returns the specific index
    """
    if isinstance(val, RecursiveRef):
        dummies = construct_dummies(
            target_func,
            limit=val.index + 1
        )
        return dummies[val.index]

    if isinstance(val, GlobalMutatorPlan):
        return create_global_mutator(target_func, val)

    if isinstance(val, CallablePlan):
        return val.build()

    if isinstance(val, list):
        return [instantiate_value(x, target_func) for x in val]
    if isinstance(val, tuple):
        return tuple(instantiate_value(x, target_func)
                     for x in val)
    if isinstance(val, dict):
        return {k: instantiate_value(v, target_func)
                for k, v in val.items()}

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
    """Returns True if any parameter of func has a type annotation"""
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


def get_instance_state(val):
    if inspect.ismethod(val):
        obj = val.__self__
        if isinstance(obj, type):
            # if val is a @classmethod, val.__self__ is the class and not the instance
            return None
    elif is_user_object(val):
        obj = val
    else:
        return None

    if hasattr(obj, '__dict__'):
        return vars(obj).copy()

    result = {}
    for cls in type(obj).__mro__:
        for slot in getattr(cls, '__slots__', ()):
            if slot in ('__dict__', '__weakref__'):
                continue
            if slot not in result:
                try:
                    result[slot] = getattr(obj, slot)
                except AttributeError:
                    pass
    return result
