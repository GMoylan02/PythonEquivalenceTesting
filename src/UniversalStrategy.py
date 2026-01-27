import copy
import inspect
from dataclasses import dataclass

from hypothesis import given, strategies as st, settings, Phase, assume, event, HealthCheck
from hypothesis.strategies import data as st_data
from typing import Callable, get_origin, get_args
from programs.equiv.bsearch_eq_1 import make_bsearch_eq_1, make_bsearch_eq_2
from TestFunctions import *
from src.Profiler import are_equivalent
from src.StateUtils import snapshot_module_state, restore_module_state
from src.programs.inequiv.bsearch_ineq_1 import make_bsearch_ineq_1_1, make_bsearch_ineq_1_2
from src.programs.inequiv.bsearch_ineq_2 import make_bsearch_ineq_2_1, make_bsearch_ineq_2_2
from src.programs.inequiv.bsearch_ineq_3 import make_bsearch_ineq_3_1, make_bsearch_ineq_3_2
from src.programs.inequiv.bsearch_ineq_4 import make_bsearch_ineq_4_1, make_bsearch_ineq_4_2
from src.programs.inequiv.bsearch_ineq_5 import make_bsearch_ineq_5_1, make_bsearch_ineq_5_2
from src.programs.inequiv import call_nested_param_ineq_B, call_nested_param_ineq_A
from src.programs.inequiv.ex3_4_e_ineq import make_v1_lhs, make_v1_rhs
from src.programs.inequiv.ex3_5_e_ineq import v2_lhs, v2_rhs
from Profiler import Profiler
import sys

MAX_CALLABLE_DEPTH = 2
MAX_CALLABLE_CALLS = 20

"""
Similar to GeneralFunctionEquivalence.py, except instead of performing type inference on function arguments to create
a fuzzing strategy, this approach creates a fuzzing strategy by just trying every type it can for function arguments
"""


@dataclass
class RecursiveRef:
    index: int


def instantiate_value(val, target_func):
    """
    Recursively traverses val. If a RecursiveRef is found, constructs the
    dummy functions bound to target_func and returns the specific index
    """
    if isinstance(val, RecursiveRef):
        dummies = construct_dummies(target_func, limit=val.index + 1)
        return dummies[val.index]

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

def get_universal_strategy(func):
    primitives = st.one_of(
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(),
        st.booleans(),
        st.none(),
        callable_strategy()
    )

    # recursive strategy that can build any combination of primitives and lists/dicts of primitives
    # can be thought of as the following recursive definition
    # strat = int|str|float|bool|None|list[strat]|dict[str,strat]|tuple[strat]
    return st.recursive(
        primitives,
        lambda children: st.one_of(
            st.lists(children),
            st.tuples(children),
            st.dictionaries(st.text(), children),
        ),
        max_leaves=10
    )


def build_args_strategy(func):
    """
    Inspects a function and returns a strategy that generates
    a tuple of arguments matching the function's signature.
    """
    sig = inspect.signature(func)
    positional_strategies = []
    has_varargs = False
    has_kwargs = False
    varargs_strategy = None
    kwargs_strategy = None

    for param_name, param in sig.parameters.items():
        if param.kind == param.VAR_POSITIONAL:
            has_varargs = True
            elem_strategy = (
                st.from_type(param.annotation)
                if param.annotation is not inspect.Parameter.empty
                else get_universal_strategy(func)
            )
            varargs_strategy = elem_strategy
            continue
        if param.kind == param.VAR_KEYWORD:
            has_kwargs = True
            value_strategy = (
                st.from_type(param.annotation)
                if param.annotation is not inspect.Parameter.empty
                else get_universal_strategy(func)
            )
            kwargs_strategy = st.dictionaries(
                    keys=st.text(min_size=1),
                    values=value_strategy,
                )

            continue

        if param.annotation != inspect.Parameter.empty:
            if param.annotation == Callable:
                # TODO: NB experiment with hypothesis inbuilt functions strategy

                # TODO: also very important that we add some mechanism for detecting callable arguments WITHOUT
                #   type annotations
                positional_strategies.append(callable_strategy(func))
                continue
            try:
                # use type hint if exists
                positional_strategies.append(st.from_type(param.annotation))
            except Exception:
                # fallback if the type hint is too complex or not supported (maybe change this to exception)
                positional_strategies.append(get_universal_strategy(func))
        else:
            # use universal strat if no type hint
            positional_strategies.append(get_universal_strategy(func))
    args_strategy = st.tuples(*positional_strategies)
    if has_varargs:
        varargs_strategy = varargs_strategy or st.just(())
        args_strategy = st.builds(
            lambda a, v: a + v,
            args_strategy,
            varargs_strategy,
        )

    if not has_kwargs:
        return st.tuples(args_strategy, st.just({}))

    kwargs_strategy = kwargs_strategy or st.just({})
    return st.tuples(args_strategy, kwargs_strategy)


def make_equivalence_test(func_a, func_b, reset_state=False):
    input_strategy = build_args_strategy(func_a)

    module_a = sys.modules.get(func_a.__module__)
    module_b = sys.modules.get(func_b.__module__)

    if reset_state:
        snap_a = snapshot_module_state(module_a) if module_a else {}
        snap_b = snapshot_module_state(module_b) if module_b else {}

    @given(input_strategy, st_data())
    @settings(max_examples=1000, deadline=None)
    def equivalence_test(inputs, data):
        if reset_state:
            if module_a: restore_module_state(module_a, snap_a)
            if module_b: restore_module_state(module_b, snap_b)
        raw_args, raw_kwargs = inputs
        # todo make this bit of code less duplicated
        args_a, kwargs_a = instantiate_args(raw_args, raw_kwargs, func_a)
        args_b, kwargs_b = instantiate_args(raw_args, raw_kwargs, func_b)
        status_a, out_a, log_a = run(func_a, args_a, kwargs_a)
        status_b, out_b, log_b = run(func_b, args_b, kwargs_b)
        equivalent_logs, index = are_equivalent(log_a, log_b)
        if not equivalent_logs:
            event(f"logs mismatch at index {index}: {log_a[index]}, {log_b[index]}")
        if status_a == "ok" and status_b == "ok":
            if callable(out_a) and callable(out_b):
                event(f"result: {out_a.__name__}, {out_b.__name__}")
            else:
                event(f"result: {out_a!r}, {out_b!r}")
            assert equivalent_logs, f"index {index}, {log_a[index]!r} != {log_b[index]!r}"
            assert_equivalent(out_a, out_b, data=data)

        elif status_a == "err" and status_b == "err":
            event(f"top-level both error: {out_a!r}, {out_b!r}")
            assert equivalent_logs, f"index {index}, {log_a[index]!r} != {log_b[index]!r}"
            assert type(out_a) is type(out_b)

        else:
            event(f"top-level domain mismatch: {out_a}, {out_b}, args={raw_args}")
            raise AssertionError(
                f"Mismatch:\n"
                f"A: {out_a}\n"
                f"B: {out_b}\n"
                f"args={raw_args}"
            )

    return equivalence_test


def assert_equivalent(
        out_a,
        out_b,
        *,
        data,
        depth=0,
):
    if not callable(out_a) or not callable(out_b):
        assert out_a == out_b, f"{out_a!r} != {out_b!r}"
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
        args_a, kwargs_a = instantiate_args(raw_args, raw_kwargs, out_a)
        args_b, kwargs_b = instantiate_args(raw_args, raw_kwargs, out_b)
        status_a, res_a, log_a = run(out_a, args_a, kwargs_a)
        status_b, res_b, log_b = run(out_b, args_b, kwargs_b)
        equivalent_logs, index = are_equivalent(log_a, log_b)
        if not equivalent_logs:
            event(f"logs mismatch at index {index}: {log_a[index]}, {log_b[index]}")
        if status_a == "ok" and status_b == "ok":
            event(f"callable both ok: {res_a}, {res_b}")
            assert equivalent_logs, f"index {index}, {log_a[index]!r} != {log_b[index]!r}"
            assert_equivalent(res_a, res_b, data=data, depth=depth + 1)

        elif status_a == "err" and status_b == "err":
            event(f"callable both error: {res_a!r}, {res_b!r}")
            assert equivalent_logs, f"index {index}, {log_a[index]!r} != {log_b[index]!r}"    # duplicated assert to ensure event() called
            assert type(res_a) is type(res_b)

        else:
            event(f"Status mismatch: {status_a}, {status_b}")
            raise AssertionError(
                f"Callable mismatch:\n"
                f"A: {res_a}\n"
                f"B: {res_b}\n"
                f"args={raw_args}"
            )


def run(fn, args, kwargs=None):
    profiler = Profiler()
    try:
        sys.setprofile(profiler.profile)
        if kwargs is None:
            result = fn(*args)
        else:
            result = fn(*args, **kwargs)
        log = profiler.trace_log
        sys.setprofile(None)
        profiler.clear_logs()
        return "ok", result, log
    except Exception as e:
        log = profiler.trace_log
        sys.setprofile(None)
        profiler.clear_logs()
        return "err", e, log


# plan: as part of fuzzing, if a func g take a callable we give it either f0, f1, or f2, but we need to make it so if we pass f2
# or f1, that f2 calls g with f1, f1 calls g with f0 and so on
# i cant think of how to make this approach work if g takes more than 1 argument though but its a start
def construct_dummies(g, limit=10):
    def f0(): pass
    functions = [f0]
    for i in range(limit-1):
        prev = functions[-1]
        def make_f(prev_fn, idx):
            def fi():
                g(prev_fn)
            fi.__name__ = f"f{idx+1}"
            return fi
        functions.append(make_f(prev, i))
    return functions

@st.composite
def callable_strategy(draw, min_limit=1, max_limit=100):
    idx = draw(st.integers(min_value=min_limit, max_value=max_limit))
    return RecursiveRef(index=idx)


"""
try:

    test_nested = make_equivalence_test(make_call_lhs, make_call_rhs)
    test_nested()

except AssertionError as e:
    print(f"Found bug\n{e}")

"""