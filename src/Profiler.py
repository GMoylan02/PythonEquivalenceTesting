import inspect
import math
import re
import sys
from pathlib import Path
from typing import Any

from src.DummyObject import DummyObject

MAX_OBJECT_DEPTH = 2

class Profiler:
    def __init__(self):
        self.trace_log = []
        self.call_stack = []
        self.call_depth = 0
        self.top_level_depth = None

    def trace(self, frame, event, arg):
        if event == "call":
            func_name = frame.f_code.co_name
            self.call_depth += 1

            # first call is always the top-level HOF
            if self.top_level_depth is None:
                self.top_level_depth = self.call_depth

            code = frame.f_code
            n_positional = code.co_argcount
            n_keyword_only = code.co_kwonlyargcount
            arg_names = set(code.co_varnames[:n_positional + n_keyword_only])
            if code.co_flags & inspect.CO_VARARGS:
                arg_names.add(code.co_varnames[n_positional + n_keyword_only])
            if code.co_flags & inspect.CO_VARKEYWORDS:
                idx = n_positional + n_keyword_only + bool(code.co_flags & inspect.CO_VARARGS)
                arg_names.add(code.co_varnames[idx])

            args_snapshot = {
                k: v for k, v in frame.f_locals.items()
                if k in arg_names
            }

            self.call_stack.append(func_name)
            self.trace_log.append({
                "event": "call",
                "function": func_name,
                "arguments": args_snapshot,
                "caller": self.call_stack[-2] if len(self.call_stack) > 1 else None,
                "depth": self.call_depth
            })

        elif event == "return":
            func_name = frame.f_code.co_name
            self.trace_log.append({
                "event": "return",
                "function": func_name,
                "return_value": arg,
                "depth": self.call_depth
            })
            self.call_depth -= 1
            if self.call_stack:
                self.call_stack.pop()

        elif event == "exception":
            exc_type, exc_value, _ = arg
            func_name = frame.f_code.co_name

            # only record if propagating at or above the top-level HOF frame
            # deeper exceptions may still be caught internally
            if self.top_level_depth is not None and self.call_depth <= self.top_level_depth:
                self.trace_log.append({
                    "event": "exception",
                    "function": func_name,
                    "exception_type": exc_type,
                    "exception": exc_value,
                    "depth": self.call_depth
                })

        return self.trace

    def clear_logs(self):
        self.trace_log = []
        self.call_stack = []
        self.call_depth = 0
        self.top_level_depth = None

function_re = r"<function.{1,100}at 0x.{1,100}>"

def is_function(val):
    return re.match(function_re, str(val)) is not None

address_re = re.compile(r' at 0x[0-9a-fA-F]+')

def normalise_string(s):
    """Strip memory addresses from string representations of objects."""
    return address_re.sub(' at 0x?', s)

def value_equivalence(value_a, value_b, visited=None):
    """
    Recursively check if two return values are equivalent, allowing them to any combination of primitives,
    objects of a user-defined class, or containers of these
    """
    if value_a is None and value_b is None:
        return True
    if value_a is None or value_b is None:
        return False
    if visited is None:
        visited = set()

    # Generally speaking we don't reach this condition unless return_a and return_b are one of the numbered dummies
    # from callable_strategy, in which case we should correctly consider them equivalent.
    # there is a very niche possibility that we reach here without dummy functions, in which case we should still
    # consider them equivalent as we can't say they are inequivalent without proper fuzzing, but this is not ideal
    pair = (id(value_a), id(value_b))
    if pair in visited:
        return True
    visited.add(pair)
    if is_function(value_a) and is_function(value_b):
        return True
    if is_function(value_a) != is_function(value_b):
        return False
    if type(value_a) != type(value_b):
        return False
    if type(value_a) == float and (math.isnan(value_a) and math.isnan(value_b)):
        return True
    if isinstance(value_a, str):
        return normalise_string(value_a) == normalise_string(value_b)
    if isinstance(value_a, dict):
        if set(value_a.keys()) != set(value_b.keys()):
            return False
        return all(value_equivalence(value_a[k], value_b[k], visited) for k in value_a)
    if isinstance(value_a, (list, tuple)):
        if len(value_a) != len(value_b):
            return False
        return all(value_equivalence(x, y, visited) for x, y in zip(value_a, value_b))
    # this works in most cases, unless these are any objects that contain cycles like DLLs, then we can potentially
    # recurse infinitely here trying to check equivalence
    #if depth < MAX_OBJECT_DEPTH and is_user_object(value_a) and is_user_object(value_b):
    if is_user_object(value_a) and is_user_object(value_b):
        return value_equivalence(vars(value_a), vars(value_b), visited)
    return value_a == value_b


def is_user_object(var):
    # checks if a variable is a user-defined object
    builtin_types = (int, float, complex, str, bool, bytes,
                     list, tuple, set, dict, frozenset, type(None))

    return not isinstance(var, builtin_types) and hasattr(var, "__dict__")


def get_instance_state(val):
    """Returns the instance __dict__ if val is a bound method or user object, else None."""
    if inspect.ismethod(val):
        obj = val.__self__
    elif is_user_object(val):
        obj = val
    else:
        return None

    if hasattr(obj, '__slots__'):
        return {slot: getattr(obj, slot) for slot in obj.__slots__ if hasattr(obj, slot)}
    return vars(obj).copy()


def assert_instance_states_equivalent(func_a, func_b):
    """
    If func_a and func_b are bound to an object, assert that every instance variable of their objects are equivalent
    """
    state_a = get_instance_state(func_a)
    state_b = get_instance_state(func_b)

    # neither is a bound method, nothing to check
    if state_a is None and state_b is None:
        return

    # one is a method and one isn't
    if (state_a is None) != (state_b is None):
        raise AssertionError(
            f"One function is a bound method and the other is not: " # todo
            f"{func_a!r} vs {func_b!r}"
        )

    # compare field by field for a useful error message
    all_keys = set(state_a) | set(state_b)
    for key in sorted(all_keys):
        if key not in state_a:
            raise AssertionError(f"Instance state mismatch: key {key!r} only in B")
        if key not in state_b:
            raise AssertionError(f"Instance state mismatch: key {key!r} only in A")

        val_a = state_a[key]
        val_b = state_b[key]

        if not value_equivalence(val_a, val_b):
            raise AssertionError(
                f"Instance state mismatch on field {key!r}: "
                f"{val_a!r} != {val_b!r}"
            )

# TODO HIGH PRIORITY: this needs to be optimised, it is currently multiple o(n) passes but can be so much better
# this is called during every single fuzz so this being inefficient directly worsens the equivalence tester
def logs_are_equivalent(log_a: list[dict], log_b: list[dict], args_a: tuple, args_b: tuple,
                    kwargs_a: dict=None, kwargs_b: dict=None,
                        top_func_name_a: str=None, top_func_name_b: str=None, strict_exceptions: bool=True):
    if not log_a or not log_b:
        return True, ""
    # resolve top-level function names
    if top_func_name_a is None:
        top_func_name_a = log_a[0]['function']
    if top_func_name_b is None:
        top_func_name_b = log_b[0]['function']


    # set of all parameters to top_func_a and top_func_b that are callable
    callable_params_a = set()
    callable_params_b = set()

    top_call_a = next(
        (e for e in log_a if e['event'] == 'call' and e['function'] == top_func_name_a),
        None
    )
    top_call_b = next(
        (e for e in log_b if e['event'] == 'call' and e['function'] == top_func_name_b),
        None
    )

    if top_call_a is None or top_call_b is None:
        return True, ""

    for argname in top_call_a['arguments'].keys():
        if callable(top_call_a['arguments'][argname]) and not isinstance(top_call_a['arguments'][argname], DummyObject):
            callable_params_a.add(top_call_a['arguments'][argname].__name__)

    for argname in top_call_b['arguments'].keys():
        if callable(top_call_b['arguments'][argname]) and not isinstance(top_call_b['arguments'][argname], DummyObject):
            callable_params_b.add(top_call_b['arguments'][argname].__name__)

    # arity check for housekeeping, i dont think this ever happens because it should get caught upstream
    if callable_params_a != callable_params_b:
        return False, f"{top_func_name_a} took different callable arguments to {top_func_name_b}: {callable_params_a} != {callable_params_b}"

    relevant_functions = callable_params_a

    # create filtered versions of the logs containing only calls/returns relating to observer functions
    filtered_log_a = []
    filtered_log_b = []
    for entry in log_a:
        if entry['function'] in relevant_functions:
            filtered_log_a.append(entry)
    for entry in log_b:
        if entry['function'] in relevant_functions:
            filtered_log_b.append(entry)

    # todo these error messages are not quite accurate
    if len(filtered_log_a) > len(filtered_log_b):
        return False, f"{top_func_name_a} called its argument more than {top_func_name_b}"
    if len(filtered_log_a) < len(filtered_log_b):
        return False, f"{top_func_name_b} called its arguments more than {top_func_name_a}"

    # check observable equivalence of exceptions
    # todo we arent actually checking the exception message

    ok, msg = exceptions_are_equivalent(log_a, log_b, strict_exceptions=strict_exceptions)
    if not ok:
        return False, msg

    for entry_a, entry_b in zip(filtered_log_a, filtered_log_b):
        # check that for all callable args to the top level HOFs, they are called with equivalent args themselves
        if "arguments" in entry_a and not value_equivalence(entry_a['arguments'], entry_b['arguments']):
            func_a = entry_a['function']
            func_b = entry_b['function']
            return False, f"Observer argument mismatch: {func_a} received arguments {entry_a['arguments']} when {func_b} received arguments {entry_b['arguments']}"

        # check that for all callable args to the top level HOFs, they return the same values
        if "return_value" in entry_a and not value_equivalence(entry_a['return_value'], entry_b['return_value']):
            func_a = entry_a['function']
            func_b = entry_b['function']
            return False, f"Observer return mismatch: {top_func_name_a}.{func_a} returned a different value from {top_func_name_b}.{func_b}"

    log_a_returns = []
    log_b_returns = []

    # check that the final return value from top_func_name_a should be equal to the final return from top_func_name_b
    i = 0
    while i < max(len(log_a), len(log_b)):
        if i < len(log_a) and log_a[i]['event'] == 'return' and log_a[i]['function'] == top_func_name_a:
            log_a_returns.append(log_a[i])
        if i < len(log_b) and log_b[i]['event'] == 'return' and log_b[i]['function'] == top_func_name_b:
            log_b_returns.append(log_b[i])
        i += 1

    # this checks that neither func_a nor func_b exceeded the python recursion limit. if one or both DID exceed it,
    # we still want to proceed with the checks after this
    if len(log_a_returns) > 0 and len(log_b_returns) > 0:

        if not value_equivalence(log_a_returns[-1]['return_value'], log_b_returns[-1]['return_value']):
            if kwargs_a != {}:
                return False, (
                    f"Function A: {top_func_name_a}({args_a}, {kwargs_a}) = {log_a_returns[-1]['return_value']!r}, "
                    f"Function B: {top_func_name_b}({args_b}, {kwargs_b}) = {log_b_returns[-1]['return_value']!r}")
            return False, (
                f"Function A: {top_func_name_a}{args_a} = {log_a_returns[-1]['return_value']!r}, "
                f"Function B: {top_func_name_b}{args_b} = {log_b_returns[-1]['return_value']!r}")
    return True, ""


def count_exceptions(log, func_name):
    return sum(
        1 for entry in log
        if entry['event'] == 'exception' and entry['function'] == func_name
    )

def count_boundary_exceptions(log):
    return sum(1 for entry in log if entry['event'] == 'exception')


def exceptions_are_equivalent(log_a, log_b, strict_exceptions=True):
    """
    Check if the observable exceptions in log_a and log_b are equivalent
    In this context, observable means they make it to the top level HOF, rather than being caught somewhere down
    the line by some observer function
    """
    excs_a = [e for e in log_a if e['event'] == 'exception']
    excs_b = [e for e in log_b if e['event'] == 'exception']

    # check boundary exceptions
    if len(excs_a) != len(excs_b):
        return False, (
            f"Boundary exception count mismatch: "
            f"A raised {len(excs_a)}, B raised {len(excs_b)}"
        )

    # only check exception types if the function is annotated
    if strict_exceptions:
        for i, (ea, eb) in enumerate(zip(excs_a, excs_b)):
            if ea['exception_type'] != eb['exception_type']:
                return False, (
                    f"Exception type mismatch at boundary exception {i}: "
                    f"A raised {ea['exception_type'].__name__}, "
                    f"B raised {eb['exception_type'].__name__}"
                )

    return True, ""

FAIL_MARKER = Path("hypofuzz_failures.log")
def record_failure(module_name, exc, unique_id):
    entry = f"{unique_id}|{module_name}: {repr(exc)}\n"

    FAIL_MARKER.touch(exist_ok=True)

    with FAIL_MARKER.open("r", encoding="utf-8") as f:
        for line in f:
            if line.startswith(f"{unique_id}|"):
                return

    with FAIL_MARKER.open("a", encoding="utf-8") as f:
        f.write(entry)
        f.flush()