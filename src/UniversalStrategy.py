import inspect
from hypothesis import given, strategies as st, settings, Phase, assume, event

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

        def run(fn, args):
            try:
                return ("ok", fn(*args))
            except Exception as e:
                return ("err", e)
        status_a, out_a = run(func_a, args)
        status_b, out_b = run(func_b, args)
        error_msg = (f"Mismatch: \n"
                     f"  {func_a.__name__} output: {out_a}\n"
                     f"  {func_b.__name__} output: {out_b}\n"
                     f"  for inputs {args}")

        if status_a == "ok" and status_b == "ok":
            event("both succeeded")
            assert out_a == out_b, error_msg
        elif status_a == "err" and status_b == "err":
            event("both raised exception")
            assert type(out_a) == type(out_b), error_msg
        else:
            event("domain mismatch")
            raise AssertionError(error_msg)

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
        
