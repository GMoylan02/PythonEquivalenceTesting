import math
import re
from pathlib import Path


class Profiler:
    def __init__(self):
        self.call_stack = []
        self.trace_log = []

    def profile(self, frame, event, arg):
        if event == "call":
            func_name = frame.f_code.co_name
            filter_re = r"<.{0,200} at 0x.{0,200}>"
            args_snapshot = {}
            for k, v in frame.f_locals.items():
                # generally speaking this should work. assume every local that is not a reference is an argument
                # todo that said, this is probably prone to error and should be made more robust in future
                # todo this can be used in future for a more correct contextual equivalence, but it is currently not used in any logic
                if not re.match(filter_re, str(v)):
                    args_snapshot[k] = v
            self.call_stack.append(func_name)
            self.trace_log.append({
                "event": "call",
                "function": func_name,
                "arguments": args_snapshot,
                # perhaps re-examine this in future as it might be wrong
                "caller": self.call_stack[-2] if len(self.call_stack) > 1 else None
            })

        elif event == "return":
            func_name = frame.f_code.co_name
            self.trace_log.append({
                "event": "return",
                "function": func_name,
                "return_value": arg
            })
            self.call_stack.pop()

        return self.profile

    def clear_logs(self):
        self.trace_log = []
        self.call_stack = []

function_re = r"<function.{1,100}at 0x.{1,100}>"

def is_function(val):
    return re.match(function_re, str(val)) is not None

supported_containers = (list, tuple, dict)

def datastruct_equivalence(ds_a, ds_b):
    if type(ds_a) == type(ds_b):
        if type(ds_a) == list:
            return list_equivalence(ds_a, ds_b)
        if type(ds_a) == dict:
            return dict_equivalence(ds_a, ds_b)
        if type(ds_a) == tuple:
            return list_equivalence(list(ds_a), list(ds_b))
    return False

def list_equivalence(list_a, list_b):
    if len(list_a) != len(list_b):
        return False
    for i in range(len(list_a)):
        if not return_value_equivalence(list_a[i], list_b[i]):
            return False
    return True

def dict_equivalence(dict_a, dict_b):
    """This works provided dict keys can only be strings"""
    if len(dict_a.keys()) != len(dict_b.keys()):
        return False
    for k in dict_a.keys():
        if not return_value_equivalence(dict_a[k], dict_b[k]):
            return False
    return True


def return_value_equivalence(return_a, return_b):
    """
    Recursively check if two return values are equivalent, allowing them to any combination of primitives,
    objects of a user-defined class, or containers of these
    """

    # Generally speaking we don't reach this condition unless return_a and return_b are one of the numbered dummies
    # from callable_strategy, in which case we should correctly consider them equivalent.
    # there is a very niche possibility that we reach here without dummy functions, in which case we should still
    # consider them equivalent as we can't say they are inequivalent without proper fuzzing, but this is not ideal
    if is_function(return_a) and is_function(return_b):
        return True
    if is_function(return_a) != is_function(return_b):
        return False
    if type(return_a) != type(return_b):
        return False
    if type(return_a) == float and (math.isnan(return_a) and math.isnan(return_b)):
        return True
    if type(return_a) in supported_containers:
        return datastruct_equivalence(return_a, return_b)
    # this works in most cases, unless these are any objects that contain cycles like DLLs, then we can potentially
    # recurse infinitely here trying to check equivalence
    if is_user_object(return_a) and is_user_object(return_b):
        return instance_vars_equal(return_a, return_b)
    if return_a != return_b:
        return False
    return True

def instance_vars_equal(obj1, obj2):
    vars1 = vars(obj1)
    vars2 = vars(obj2)

    return return_value_equivalence(vars1, vars2)

def is_user_object(var):
    # checks if a variable is a user-defined object
    builtin_types = (int, float, complex, str, bool, bytes,
                     list, tuple, set, dict, frozenset, type(None))

    return not isinstance(var, builtin_types) and hasattr(var, "__dict__")


def are_equivalent(log_a, log_b):
    """
    Checks that the trace log of functions func_a and func_b are contextually equivalent in 2 main steps
    1. Check that the final return value of func_a() `eq` func_b()
    2. Check that forall f in f_functions, f() in log_a `eq` f() in log_b
            where f_functions are 'observer' functions to func_a and func_b defined in construct_dummies()
            for example, f5 is def f5(): return g(f4), f4 is def f4(): return g(f3), and so on where g is func_a or func_b

    """
    top_func_name_a = log_a[0]['function']
    top_func_name_b = log_b[0]['function']
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

        if not return_value_equivalence(log_a_returns[-1]['return_value'], log_b_returns[-1]['return_value']):
            return False, (f"Mismatch: "
                f"Function A: {top_func_name_a} = {log_a_returns[-1]['return_value']!r}, "
                f"Function B: {top_func_name_b} = {log_b_returns[-1]['return_value']!r}")

    # f_functions are functions used for testing deep recursion. this logic serves to check that
    # forall f in f_functions, f in log_a == f in log_b
    # this is only a valid equivalence check because we know that each f{i} is defined as: return g(f{i-1})
    # where g is the top level function in log_a and log_b that we are testing for equivalence.
    # thus, if the return value of f{i} differs across log_a and log_b, we know that an observable call to g resulted in
    # a different output, implying the two implementations of g are not contextually equivalent
    f_functions = []
    for i in range(100):
        f_functions.append(f"f{i}")

    f_function_returns_in_log_A = {}    # return values of each of the f within log A
    for i in range(len(log_a)):
        if log_a[i]['event'] == 'return' and log_a[i]['function'] in f_functions:
            if log_a[i]['function'] in f_function_returns_in_log_A:     # skip functions we have already seen
                continue
            f_function_returns_in_log_A[log_a[i]['function']] = log_a[i]['return_value']

    f_functions_seen_in_B = []      # used to skip functions in b we have already seen
    for i in range(len(log_b)):
        if log_b[i]['event'] == 'return' and log_b[i]['function'] in f_functions:
            if log_b[i]['function'] in f_functions_seen_in_B:   # skip functions we have already seen
                continue
            if log_b[i]['function'] not in f_function_returns_in_log_A.keys():
                # we should never get here, this means that log_b called some f_function that log_a never called
                raise AssertionError(f"Function {log_b[i]['function']} not called by {top_func_name_a}, this should never happen")

            if not return_value_equivalence(log_b[i]['return_value'], f_function_returns_in_log_A[log_a[i]['function']]):
                return False, (f"Mismatch: Observer {log_a[i]['function']} observed {top_func_name_a} giving differing outputs "
                    f"Within Function A: {log_a[i]['function']} => {f_function_returns_in_log_A[log_a[i]['function']]!r}, "
                    f"Within Function B: {log_b[i]['function']} => {log_b[i]['return_value']!r}")
            f_functions_seen_in_B.append(log_b[i]['function'])

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