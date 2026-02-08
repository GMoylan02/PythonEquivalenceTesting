import inspect
from dataclasses import dataclass
from functools import wraps
from pathlib import Path

from hypothesis import given, strategies as st, settings, event
from hypothesis.strategies import data as st_data
from typing import Callable

from src.GenerateFunctions import RecursiveRef, construct_dummies, callable_strategy, preset_functions
from src.Profiler import are_equivalent
from src.StateUtils import snapshot_module_state, restore_module_state
from src.Profiler import Profiler, return_value_equivalence
import sys


MAX_CALLABLE_DEPTH = 2
MAX_CALLABLE_CALLS = 20


def get_universal_strategy():
    primitives = st.one_of(
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(),
        st.booleans(),
        st.none(),
        callable_strategy(),
        preset_functions()
        #st.functions()
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
                else get_universal_strategy()
            )
            varargs_strategy = elem_strategy
            continue
        if param.kind == param.VAR_KEYWORD:
            has_kwargs = True
            value_strategy = (
                st.from_type(param.annotation)
                if param.annotation is not inspect.Parameter.empty
                else get_universal_strategy()
            )
            kwargs_strategy = st.dictionaries(
                    keys=st.text(min_size=1),
                    values=value_strategy,
                )

            continue

        if param.annotation != inspect.Parameter.empty:
            if param.annotation == Callable:
                # TODO: NB experiment with hypothesis inbuilt functions strategy

                # TODO: for performance we can add some mechanism for detecting callable arguments WITHOUT
                #   type annotations
                #positional_strategies.append(st.one_of(callable_strategy(func), st.functions()))
                #positional_strategies.append(st.functions())
                #positional_strategies.append(callable_strategy(func))
                return_strat = st.integers()

                positional_strategies.append(
                    st.one_of(
                        callable_strategy(),
                        preset_functions(),
                        #st.functions(like=lambda *args, **kwargs: None, returns=return_strat)
                    )
                )
                continue
            try:
                # use type hint if exists
                positional_strategies.append(st.from_type(param.annotation))
            except Exception:
                # fallback if the type hint is too complex or not supported (maybe change this to exception)
                positional_strategies.append(get_universal_strategy())
        else:
            # use universal strat if no type hint
            positional_strategies.append(get_universal_strategy())
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
    @settings(max_examples=500, deadline=None)
    def equivalence_test(inputs, data):
        if reset_state:
            if module_a: restore_module_state(module_a, snap_a)
            if module_b: restore_module_state(module_b, snap_b)
        raw_args, raw_kwargs = inputs
        run_and_test_equivalence(func_a, func_b, raw_args, raw_kwargs, data)

    return equivalence_test


def assert_equivalent(
        out_a,
        out_b,
        *,
        data,
        depth=0,
):
    if not callable(out_a) or not callable(out_b):
        assert return_value_equivalence(out_a, out_b), f"{out_a!r} != {out_b!r}"
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


def run(fn, args, kwargs=None):
    profiler = Profiler()
    try:
        sys.setprofile(profiler.profile)
        if kwargs == {} or kwargs is None:
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


def run_and_test_equivalence(func_a, func_b, raw_args, raw_kwargs, data):
    args_a, kwargs_a = instantiate_args(raw_args, raw_kwargs, func_a)
    args_b, kwargs_b = instantiate_args(raw_args, raw_kwargs, func_b)
    status_a, out_a, log_a = run(func_a, args_a, kwargs_a)
    status_b, out_b, log_b = run(func_b, args_b, kwargs_b)
    equivalent_logs, logs_error_msg = are_equivalent(log_a, log_b)
    if not equivalent_logs:
        event(logs_error_msg)
    if status_a == "ok" and status_b == "ok":
        if callable(out_a) and callable(out_b):
            event(f"{func_a.__name__}, {func_b.__name__}: both succeeded and callable")
        else:
            event(f"{func_a.__name__}, {func_b.__name__}: both succeeded")
        assert equivalent_logs, logs_error_msg
        assert_equivalent(out_a, out_b, data=data)

    elif status_a == "err" and status_b == "err":
        event(f"{func_a.__name__}, {func_b.__name__} top-level both error: {out_a!r}, {out_b!r}")
        assert equivalent_logs, logs_error_msg
        # todo stop copy pasting this error message
        assert type(out_a) is type(out_b), (
            f"Mismatch: "
            f"Function A: {func_a.__name__}({args_a!r}) = {out_a!r}, "
            f"Function B: {func_b.__name__}({args_b!r}) = {out_b!r}"
        )

    else:
        event(f"{func_a.__name__}, {func_b.__name__} top-level domain mismatch: {out_a}, {out_b}, args={args_a!r}")
        raise AssertionError(
            f"Mismatch: "
            f"Function A: {func_a.__name__}({args_a!r}) = {out_a!r}, "
            f"Function B: {func_b.__name__}({args_b!r}) = {out_b!r}"
        )
