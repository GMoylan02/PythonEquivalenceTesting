import inspect
from hypothesis import given, strategies as st, settings, Phase, assume
from TestFunctions import *

"""
Similar to GeneralFunctionEquivalence.py, except instead of performing type inference on function arguments to create
a fuzzing strategy, this approach creates a fuzzing strategy by just trying every type it can for function arguments
"""

def get_universal_strategy():
    primitives = st.one_of(
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(),
        st.booleans(),
        st.none(),
    )

    # recursive strategy that can build any combination of primitives and lists/dicts of primitives
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
    arg_strategies = []

    for param_name, param in sig.parameters.items():
        # TODO support args and kwargs
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue

        if param.annotation != inspect.Parameter.empty:
            # use type hint if exists
            try:
                arg_strategies.append(st.from_type(param.annotation))
            except Exception:
                # fallback if the type hint is too complex or not supported
                arg_strategies.append(get_universal_strategy())
        else:
            # use universal strat if no type hint
            arg_strategies.append(get_universal_strategy())
    return st.tuples(*arg_strategies)

def make_equivalence_test(func_a, func_b):
    args_strategy = build_args_strategy(func_a)

    @given(args_strategy)
    @settings(max_examples=1000)
    def test_equivalence(args):
        try:
            res_a = func_a(*args)
        except TypeError:
            # tell hypothesis to avoid this type in future iterations
            # This should help to cut down on unnecessary iterations, but has the side effect of making it so
            # hypothesis will not be able to catch situations where func_b handles a certain argument type, but func_a
            # cannot handle this type. this is probably fine though, at least for now
            assume(False)
        except Exception as e_a:
            # If A crashes with a non-TypeError, B must crash with the same type
            try:
                func_b(*args)
            except Exception as e_b:
                assert type(e_a) == type(e_b)
                return
            raise e_a

        try:
            res_b = func_b(*args)
        except TypeError:
            # If A succeeded but B failed with TypeError
            # this implies A handled a type B couldn't
            # This might need to be reconsidered in future
            raise AssertionError(f"{func_a.__name__} accepted {args} but {func_b.__name__} raised TypeError")
        except Exception as e_b:
             raise AssertionError(f"{func_a.__name__} returned {res_a} but {func_b.__name__} crashed with {e_b}")

        assert res_a == res_b, f"Mismatch: {res_a} != {res_b} for inputs {args}"

    return test_equivalence


test_dedupe = make_equivalence_test(dedupe_buggy, dedupe_correct)

if __name__ == "__main__":
    try:
        test_dedupe()
        # The intended bug between dedupe_buggy, dedupe_correct is that dedupe_buggy breaks when xs is of
        # type list[int|None] whereas dedupe_correct still works

        # This framework instead finds that these dedupe functions differ when xs is a dict {'': 0}
        # This is technically true, but i didnt write these functions expecting for a dict to be passed in
        # I still think this is good behaviour though
    except AssertionError as e:
        print(f"Found bug\n{e}")
        
