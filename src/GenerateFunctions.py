import inspect
from dataclasses import dataclass
from typing import Callable, List

from hypothesis import strategies as st
from abc import ABC, abstractmethod


class CallablePlan(ABC):
    @abstractmethod
    def build(self) -> Callable:
        """Instantiate the plan into a concrete callable"""
        ...

@dataclass
class InterleavedCallerPlan(CallablePlan):
    """
    Describes an interleaved call sequence for a function.
    call_sequence is a list of indices (into *funcs) dictating which argument
    to call at each step, in order
    """
    call_sequence: list[int]  # e.g. [0, 1, 0, 0, 1, 2]

    def build(self) -> Callable:
        """
        returns a function that accepts any number of callables and calls them
        in the order given by plan.call_sequence
        """
        def interleaved_caller(*funcs):
            if not funcs:
                return
            results = [funcs[idx % len(funcs)]()
                       for idx in self.call_sequence]
            return results[-1] if results else None
        return interleaved_caller

@dataclass
class FlatCombinerPlan(CallablePlan):
    """
    Generates f for HOFs of the form: lambda f: f(enlist)(run)

    1. f(enlist):
      Calls enlist(inner) 'enlist_calls' times, where inner appends to a shared log
      Returns the function 'phase2'

    2.  phase2(run):
      Calls run() 'run_calls' times
      Optionally calls enlist(inner) 'post_run_enlist_calls' more times
      (exercises whether run resets the running flag).
      Returns the log
    """
    enlist_calls: int
    run_calls: int
    # we call enlist after run to probe for un-reset flags
    # e.g  "if not (running[0] == 0)"
    post_run_enlist_calls: int

    def build(self):
        def f(enlist):
            log = []

            def operation():
                log.append(1)

            for _ in range(self.enlist_calls):
                enlist(operation)

            def run_phase(run):
                for _ in range(self.run_calls):
                    try:
                        run()
                    except Exception as e:
                        log.append(('run_raised', type(e).__name__))

                # probe whether running flag was cleared
                for _ in range(self.post_run_enlist_calls):
                    enlist(operation)

                return tuple(log)

            return run_phase

        return f


@dataclass
class RecursiveRef:
    index: int


# plan: as part of fuzzing, if a func g take a callable we give it either f0, f1, or f2, but we need to make it so if we pass f2
# or f1, that f2 calls g with f1, f1 calls g with f0 and so on
def construct_dummies(g, limit=20):
    def f0(): pass
    functions = [f0]
    for i in range(limit-1):
        prev = functions[-1]
        def make_f(prev_fn, idx):
            func_definition = f"""
def f{idx+1}(*args, **kwargs):
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

# set of preset functions that catch a large proportion of HOF cases

def h1(n):
    return n

def h2(g):
    g(1)
    g(1)

def h3(g):
    g(5)
    return g(5)

def h4(f, g):
    f()
    g()

def h5(g):
    g()

def h6(*args, **kwargs):
    return None

@st.composite
def preset_functions(draw):
    funcs = [h1, h2, h3, h6]
    return draw(st.sampled_from(funcs))


@dataclass
class GlobalMutatorPlan:
    """
    Represents a deterministic sequence of mutations to apply.
    Hypothesis generates this. instantiate_value consumes it.
    NB: CURRENTLY NOT USED
    """
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


# todo idea: generate functions that take varargs, give the function logic to iterate over its args, check type, and dynamically
# perform action on that arg depending on its signature
