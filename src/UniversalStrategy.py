import inspect

from hypothesis import given, strategies as st, settings, event
from hypothesis.strategies import data as st_data
from typing import Callable

from src.GenerateFunctions import RecursiveRef, construct_dummies, callable_strategy, preset_functions, \
    GlobalMutatorPlan, create_global_mutator, InterleavedCallerPlan, create_interleaved_caller, CurriedInteractionPlan, \
    create_curried_interaction
from src.Profiler import logs_are_equivalent, assert_instance_states_equivalent
from src.StateUtils import snapshot_module_state, restore_module_state
from src.Profiler import Profiler, return_value_equivalence, record_failure
import sys

already_logged = False
MAX_CALLABLE_DEPTH = 2
MAX_CALLABLE_CALLS = 20
MAX_TUPLE_CALLS = 30

# TODO: The fact that the error messages are all over the place is terrible and needs to be refactored in future

def get_universal_strategy():
    primitives = st.one_of(
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(),
        st.booleans(),
        st.none(),
        callable_strategy(),
        preset_functions(),
        interleaved_caller_strategy(),
        curried_interaction_strategy(),
        global_mutator_strategy()   # not applicable for hobbit suite
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

def global_mutator_strategy():
    return st.builds(GlobalMutatorPlan,
                  increments=st.lists(st.integers(min_value=-10, max_value=105)),
                  string_concats=st.lists(st.text()))

def interleaved_caller_strategy():
    return st.builds(
        InterleavedCallerPlan,
        call_sequence=st.lists(
            st.integers(min_value=0, max_value=9),
            min_size=0,
            max_size=20,
        )
    )

def curried_interaction_strategy():
    return st.builds(
        CurriedInteractionPlan,
        enlist_calls=st.integers(min_value=1, max_value=5),
        run_calls=st.integers(min_value=1, max_value=3),
        post_run_enlist_calls=st.integers(min_value=0, max_value=3),
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
            varargs_strategy = st.lists(elem_strategy).map(tuple)
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

                positional_strategies.append(
                    st.one_of(
                        callable_strategy(),
                        preset_functions(),
                        interleaved_caller_strategy(),
                        global_mutator_strategy(),
                        curried_interaction_strategy()
                        #st.functions(like=lambda *args, **kwargs: None, returns=return_strat)
                    )
                )
                continue
            if is_user_defined_class(param.annotation):
                positional_strategies.append(build_instance_strategy(param.annotation))
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
        args_strategy = st.builds(
            lambda a, v: a + v,
            args_strategy,
            varargs_strategy,
        )

    if not has_kwargs:
        return st.tuples(args_strategy, st.just({}))

    return st.tuples(args_strategy, kwargs_strategy)


def build_instance_strategy(cls):
    """
    Generates instances of cls by fuzzing its __init__ arguments.
    Falls back to universal strategy construction if __init__ is not type annotated
    """
    try:
        init_sig = inspect.signature(cls.__init__)
    except (ValueError, TypeError):
        return st.just(cls())

    arg_strategies = []
    for param_name, param in init_sig.parameters.items():
        if param_name == 'self':
            continue
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue

        if param.annotation != inspect.Parameter.empty:
            if is_user_defined_class(param.annotation):
                # recursively handle nested user-defined types
                arg_strategies.append(build_instance_strategy(param.annotation))
            else:
                try:
                    arg_strategies.append(st.from_type(param.annotation))
                except Exception:
                    arg_strategies.append(get_universal_strategy())
        elif param.default != inspect.Parameter.empty:
            arg_strategies.append(st.just(param.default))
        else:
            arg_strategies.append(get_universal_strategy())

    if not arg_strategies:
        return st.just(cls())

    return st.builds(cls, *arg_strategies)

def is_user_defined_class(annotation):
    return (
        inspect.isclass(annotation)
        and annotation.__module__ not in ('builtins', 'typing')
        and not annotation.__module__.startswith('hypothesis')
    )


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
    @settings(max_examples=500, deadline=None)
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


def assert_equivalent(
        out_a,
        out_b,
        *,
        data,
        depth=0,
):
    if _is_callable_tuple(out_a) and _is_callable_tuple(out_b):
        if depth >= MAX_CALLABLE_DEPTH:
            event("callable tuple depth limit")
            return
        assert_equivalent_callable_tuple(out_a, out_b, data=data, depth=depth)
        return

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

    if isinstance(val, GlobalMutatorPlan):
        return create_global_mutator(target_func, val)

    if isinstance(val, InterleavedCallerPlan):
        return create_interleaved_caller(val)

    if isinstance(val, CurriedInteractionPlan):
        return create_curried_interaction(val)

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
    equivalent_logs, logs_error_msg = logs_are_equivalent(log_a, log_b, args_a, args_b, kwargs_a, kwargs_b)

    # todo low hanging fruit: we can check if the console output of both funcs is equivalent
    # todo low hanging fruit: need to check that if the args to both funcs are altered, they are altered equivalently

    # check that if the function(s) lie in a class, that every class attribute
    # is equivalent
    if not equivalent_logs:
        event(logs_error_msg)
    if status_a == "ok" and status_b == "ok":
        if callable(out_a) and callable(out_b):
            event(f"{func_a.__name__}, {func_b.__name__}: both succeeded and callable")
        else:
            event(f"{func_a.__name__}, {func_b.__name__}: both succeeded")
        assert equivalent_logs, logs_error_msg
        assert_instance_states_equivalent(func_a, func_b)
        assert_equivalent(out_a, out_b, data=data)

    elif status_a == "err" and status_b == "err":
        event(f"{func_a.__name__}, {func_b.__name__} top-level both error: {out_a!r}, {out_b!r}")
        assert equivalent_logs, logs_error_msg
        assert_instance_states_equivalent(func_a, func_b)
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

def generate_tuple_operation_strategy(tuple_a, tuple_b):
    strats = []
    for i, function in enumerate(tuple_a):
        strats.append(st.tuples(st.just(i), build_args_strategy(function)))
    operation_strategy = st.one_of(strats)
    return operation_strategy
