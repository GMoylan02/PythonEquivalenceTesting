import inspect
import sys
import types
from dataclasses import dataclass
from typing import Callable, List, Any

from hypothesis import strategies as st


@dataclass
class RecursiveRef:
    index: int


# plan: as part of fuzzing, if a func g take a callable we give it either f0, f1, or f2, but we need to make it so if we pass f2
# or f1, that f2 calls g with f1, f1 calls g with f0 and so on
# i cant think of how to make this approach work if g takes more than 1 argument though but its a start
def construct_dummies(g, limit=10):
    def f0(): pass
    functions = [f0]
    for i in range(limit-1):
        prev = functions[-1]
        def make_f(prev_fn, idx):
            func_definition = f"""
def f{idx+1}():
    return g(prev_fn)
"""
            local_vars = {}
            exec(func_definition, {"g": g, "prev_fn": prev_fn}, local_vars)
            # This seems like a pretty horrible way to generate functions on the fly, but it is necessary to have
            # meaningful function names in the logs when testing equivalence
            return local_vars[f"f{idx + 1}"]
        functions.append(make_f(prev, i))
    return functions

@st.composite
def callable_strategy(draw, min_limit=1, max_limit=20):
    idx = draw(st.integers(min_value=min_limit, max_value=max_limit))
    return RecursiveRef(index=idx)

def h1(n):
    return n

def h2(g):
    g()

def h3(g):
    g(5)
    return g(5)

def h4(f, g):
    f()
    g()

@st.composite
def preset_functions(draw):
    funcs = [h1, h2, h3, h4]
    return draw(st.sampled_from(funcs))


@dataclass
class GlobalMutatorPlan:
    """
    Represents a deterministic sequence of mutations to apply.
    Hypothesis generates this. instantiate_value consumes it.
    """
    # todo come up with sensible mutations for other types
    increments: List[int]
    string_concats: List[str]



def create_global_mutator(target_func, plan: GlobalMutatorPlan):
    """
    Creates a function that gets passed as an argument to the function being tested that mutates global state
    """
    module = inspect.getmodule(target_func)
    if not module:
        return lambda *a, **k: None

    increments_stream = iter(plan.increments)
    string_concats_stream = iter(plan.string_concats)

    def mutator(*args, **kwargs):
        """
        The function that gets passed as an argument when testing, mutates global variables in its scope
        """
        for name, value in list(vars(module).items()):
            # todo probably exclude upper snake case variables as well (constants)
            # todo can streamline this flow
            if type(value) is int and not name.startswith("__"):
                try:
                    inc = next(increments_stream)
                    setattr(module, name, value + inc)
                except StopIteration:
                    return None
            if type(value) is bool and not name.startswith("__"):
                setattr(module, name, not value)
            if type(value) is str and not name.startswith("__"):
                try:
                    concat = next(string_concats_stream)
                    setattr(module, name, value + concat)
                except StopIteration:
                    return None
            if type(value) is list and not name.startswith("__"):
                try:
                    concat = next(increments_stream)
                    setattr(module, name, value + concat)
                except StopIteration:
                    return None
            if value is None and not name.startswith("__"):
                try:
                    num = next(increments_stream)
                    setattr(module, name, num)
                except StopIteration:
                    return None
        return None

    return mutator
