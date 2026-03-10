import inspect
import typing

from hypothesis import strategies as st
from typing import Callable

from src.DummyObject import DummyObject
from src.GenerateFunctions import (callable_strategy, preset_functions, GlobalMutatorPlan, InterleavedCallerPlan,
                                   FlatCombinerPlan)

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
        *_all_callable_strategies(),
        dummy_object_strategy()
       # global_mutator_strategy()   # not applicable for hobbit suite
    )

    # recursive strategy that can build any combination of primitives and lists/dicts of primitives
    # can be thought of as the following recursive definition
    # universal_strat = int|str|float|bool|None|Callable|dummy|list[universal_strat]|dict[str,universal_strat]|tuple[universal_strat]
    return st.recursive(
        primitives,
        lambda children: st.one_of(
            st.lists(children),
            st.tuples(children),
            st.dictionaries(st.text(), children),
        ),
        max_leaves=10
    )

def _all_callable_strategies():
    return [
        callable_strategy(),
        preset_functions(),
        interleaved_caller_strategy(),
        flat_combiner_strategy(),
        #global_mutator_strategy()  temporarily commented out
    ]

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


def flat_combiner_strategy():
    return st.builds(
        FlatCombinerPlan,
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
        elif param.default != inspect.Parameter.empty:
            positional_strategies.append(strategy_from_default(param.default))
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
    return st.one_of(*_all_callable_strategies())


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
            # tuple[X, ...]: variable length homogeneous tuple
            return st.lists(strategy_from_annotation(args[0])).map(tuple)
        # tuple[X, Y, Z]: fixed length heterogeneous tuple
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
            arg_strategies.append(strategy_from_default(param.default))
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


def strategy_from_default(default):
    """
    Infers a strategy from the type of a default value,
    broadening the search beyond just the default itself.
    """
    t = type(default)
    if t is bool:  # must check before int since bool is a subclass of int
        return st.booleans()
    if t is int:
        return st.integers()
    if t is float:
        return st.floats(allow_nan=False, allow_infinity=False)
    if t is str:
        return st.text()
    if t is list:
        return st.lists(get_universal_strategy())
    if t is dict:
        return st.dictionaries(st.text(), get_universal_strategy())
    if t is tuple:
        return st.tuples(get_universal_strategy())
    if t is type(None):
        return get_universal_strategy()
    if is_user_defined_class(t):
        return build_instance_strategy(t)
    return get_universal_strategy()
