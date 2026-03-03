import inspect
import typing

from hypothesis import strategies as st
from typing import Callable

from src.DummyObject import DummyObject
from src.GenerateFunctions import (callable_strategy, preset_functions, GlobalMutatorPlan, InterleavedCallerPlan,
                                   CurriedInteractionPlan)

already_logged = False

"""
The logic surrounding custom strategies
"""


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
        dummy_object_strategy()
       # global_mutator_strategy()   # not applicable for hobbit suite
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


@st.composite
def dummy_object_strategy(draw, max_depth=3):
    val = draw(st.one_of(st.integers(), st.none(), st.text(max_size=5)))
    return DummyObject(depth=0, max_depth=max_depth, val=val)


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
                strategy_from_annotation(param.annotation)
                if param.annotation is not inspect.Parameter.empty
                else get_universal_strategy()
            )
            varargs_strategy = st.lists(elem_strategy).map(tuple)
            continue

        if param.kind == param.VAR_KEYWORD:
            has_kwargs = True
            value_strategy = (
                strategy_from_annotation(param.annotation)
                if param.annotation is not inspect.Parameter.empty
                else get_universal_strategy()
            )
            kwargs_strategy = st.dictionaries(
                keys=st.text(min_size=1),
                values=value_strategy,
            )
            continue

        if param.annotation != inspect.Parameter.empty:
            positional_strategies.append(strategy_from_annotation(param.annotation))
        else:
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


def callable_strategy_for_annotation():
    return st.one_of(
        callable_strategy(),
        preset_functions(),
        interleaved_caller_strategy(),
        #global_mutator_strategy(),
        curried_interaction_strategy()
    )


def strategy_from_annotation(annotation):
    """
    Recursively resolves a type annotation to a strategy, using custom
    callable strategies wherever Callable appears inside containers.
    """
    if annotation is inspect.Parameter.empty:
        return get_universal_strategy()

    if annotation is Callable:
        return callable_strategy_for_annotation()

    if is_user_defined_class(annotation):
        return build_instance_strategy(annotation)

    origin = typing.get_origin(annotation)
    args = typing.get_args(annotation)

    if origin is tuple:
        if not args:
            # bare tuple, no inner type info
            return st.tuples()
        if len(args) == 2 and args[1] is Ellipsis:
            # tuple[X, ...] — variable length homogeneous tuple
            return st.lists(strategy_from_annotation(args[0])).map(tuple)
        # tuple[X, Y, Z] — fixed length heterogeneous tuple
        return st.tuples(*[strategy_from_annotation(a) for a in args])

    if origin is list:
        inner = strategy_from_annotation(args[0]) if args else get_universal_strategy()
        return st.lists(inner)

    if origin is dict:
        k_strat = strategy_from_annotation(args[0]) if args else st.text()
        v_strat = strategy_from_annotation(args[1]) if len(args) > 1 else get_universal_strategy()
        return st.dictionaries(k_strat, v_strat)

    if origin is typing.Union:
        return st.one_of(*[strategy_from_annotation(a) for a in args])

    # fallback to hypothesis native resolution
    try:
        return st.from_type(annotation)
    except Exception:
        return get_universal_strategy()


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


def generate_tuple_operation_strategy(tuple_a, tuple_b):
    strats = []
    for i, function in enumerate(tuple_a):
        strats.append(st.tuples(st.just(i), build_args_strategy(function)))
    operation_strategy = st.one_of(strats)
    return operation_strategy
