import inspect
import math
import re
import sys
from pathlib import Path


class Profiler:
    def __init__(self):
        self.call_stack = []
        self.trace_log = []

    def profile(self, frame, event, arg):
        if event == "call":
            func_name = frame.f_code.co_name

            # co_varnames contains all local variable names in order:
            # positional args, keyword-only args, *args, **kwargs, then locals
            # the argument count fields tell us exactly where args end
            code = frame.f_code
            n_positional = code.co_argcount
            n_keyword_only = code.co_kwonlyargcount

            arg_names = set(code.co_varnames[:n_positional + n_keyword_only])

            # also include *args and **kwargs if present
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
                "caller": self.call_stack[-2] if len(self.call_stack) > 1 else None
            })

        elif event == "return":
            func_name = frame.f_code.co_name
            exc = sys.exc_info()
            is_exception_exit = exc[0] is not None
            self.trace_log.append({
                "event": "return",
                "function": func_name,
                "return_value": arg,
                "exception": exc[1] if is_exception_exit else None,
                "exception_type": exc[0] if is_exception_exit else None,
                "is_exception_exit": is_exception_exit
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

# TODO: this smells, some of these functions do p. much the same thing. In need of a refactor, but not a priority now

def instance_vars_equal(obj1, obj2):
    vars1 = vars(obj1)
    vars2 = vars(obj2)

    return return_value_equivalence(vars1, vars2)

def is_user_object(var):
    # checks if a variable is a user-defined object
    builtin_types = (int, float, complex, str, bool, bytes,
                     list, tuple, set, dict, frozenset, type(None))

    return not isinstance(var, builtin_types) and hasattr(var, "__dict__")


def get_instance_state(val):
    """If func is a bound method, return its instance's __dict__, else None."""
    if inspect.ismethod(val):
        return vars(val.__self__).copy()
    if is_user_object(val):
        return vars(val).copy()
    return None


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

        # skip fields that are user-defined objects — these are infrastructure,
        # not meaningful state we can compare structurally
        if is_user_object(val_a) or is_user_object(val_b):
            continue

        if not return_value_equivalence(val_a, val_b):
            raise AssertionError(
                f"Instance state mismatch on field {key!r}: "
                f"{val_a!r} != {val_b!r}"
            )


STUB_PREFIX = "__stub_"
# todo refactor
"""
def logs_are_equivalent(log_a, log_b, args_a, args_b, kwargs_a=None, kwargs_b=None):
    top_func_name_a = log_a[0]['function']
    top_func_name_b = log_b[0]['function']

    # check final return value
    log_a_returns = []
    log_b_returns = []
    for entry in log_a:
        if entry['event'] == 'return' and entry['function'] == top_func_name_a:
            log_a_returns.append(entry)
    for entry in log_b:
        if entry['event'] == 'return' and entry['function'] == top_func_name_b:
            log_b_returns.append(entry)

    if log_a_returns and log_b_returns:
        if not return_value_equivalence(log_a_returns[-1]['return_value'], log_b_returns[-1]['return_value']):
            return False, (
                f"Function A: {top_func_name_a}({args_a}) = {log_a_returns[-1]['return_value']!r}, "
                f"Function B: {top_func_name_b}({args_b}) = {log_b_returns[-1]['return_value']!r}"
            )

    # f-functions (observers) check
    f_functions = {f"f{i}" for i in range(100)}

    f_returns_a = {}
    for entry in log_a:
        if entry['event'] == 'return' and entry['function'] in f_functions:
            if entry['function'] not in f_returns_a:
                f_returns_a[entry['function']] = entry['return_value']

    seen_in_b = set()
    for entry in log_b:
        if entry['event'] == 'return' and entry['function'] in f_functions:
            if entry['function'] in seen_in_b:
                continue
            if entry['function'] not in f_returns_a:
                raise AssertionError(
                    f"Function {entry['function']} not called by {top_func_name_a}, this should never happen"
                )
            if not return_value_equivalence(entry['return_value'], f_returns_a[entry['function']]):
                return False, (
                    f"Mismatch: Observer {entry['function']} observed differing outputs. "
                    f"A: {f_returns_a[entry['function']]!r}, B: {entry['return_value']!r}"
                )
            seen_in_b.add(entry['function'])

    # --- new stub interaction check ---
    ok, msg = check_stub_interactions_equivalent(log_a, log_b)
    if not ok:
        return False, msg

    return True, ""
"""
def logs_are_equivalent(log_a, log_b, args_a, args_b, kwargs_a=None, kwargs_b=None):
    """
    Checks that the trace log of functions func_a and func_b are contextually equivalent in 2 main steps
    1. Check that the final return value of func_a() `eq` func_b()
    2. Check that forall f in f_functions, f() in log_a `eq` f() in log_b
            where f_functions are 'observer' functions to func_a and func_b defined in construct_dummies()
            for example, f5 is def f5(): return g(f4), f4 is def f4(): return g(f3), and so on where g is func_a or func_b

    """

    # potentially we can devise a set of function parameters to top_level_a and top_level_b, filter out any function calls and returns from functions
    # other than top_level_a, top_level_b, and their param functions

    top_func_name_a = log_a[0]['function']
    top_func_name_b = log_b[0]['function']
    callable_params_a = set()
    callable_params_b = set()
    top_call_a = log_a[0]
    top_call_b = log_b[0]
    for argname in top_call_a['arguments'].keys():
        if callable(top_call_a['arguments'][argname]):
            callable_params_a.add(top_call_a['arguments'][argname].__name__)

    for argname in top_call_b['arguments'].keys():
        if callable(top_call_b['arguments'][argname]):
            callable_params_b.add(top_call_b['arguments'][argname].__name__)

    if callable_params_a != callable_params_b:
        return False, f"{top_func_name_a} took different callable arguments to {top_func_name_b}: {callable_params_a} != {callable_params_b}"

    relevant_functions = callable_params_a
    relevant_functions.add(top_func_name_a)
    relevant_functions.add(top_func_name_b)

    filtered_log_a = []
    filtered_log_b = []
    for entry in log_a:
        if entry['function'] in relevant_functions:
            filtered_log_a.append(entry)
    for entry in log_b:
        if entry['function'] in relevant_functions:
            filtered_log_b.append(entry)

    #if callable(args_a[0]) and "h2" in args_a[0].__name__:
    #    import pdb;pdb.set_trace()

    if len(filtered_log_a) > len(filtered_log_b):
        return False, f"{top_func_name_a} called its argument more than {top_func_name_b}: {top_func_name_a}: {filtered_log_a} != {top_func_name_b}: {filtered_log_b}"
    if len(filtered_log_a) < len(filtered_log_b):
        return False, f"{top_func_name_b} called its arguments more than {top_func_name_a}: {top_func_name_a}: {filtered_log_a} != {top_func_name_b}: {filtered_log_b}"
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
            if kwargs_a != {}:
                return False, (
                    f"Function A: {top_func_name_a}({args_a}, {kwargs_a}) = {log_a_returns[-1]['return_value']!r}, "
                    f"Function B: {top_func_name_b}({args_b}, {kwargs_b}) = {log_b_returns[-1]['return_value']!r}")
            return False, (
                f"Function A: {top_func_name_a}{args_a} = {log_a_returns[-1]['return_value']!r}, "
                f"Function B: {top_func_name_b}{args_b} = {log_b_returns[-1]['return_value']!r}")

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

def check_stub_interactions_equivalent(log_a, log_b):
    """
    Extracts all stub call/return sequences from each log and compares them pairwise.
    Stubs are matched by name — both sides instantiate stubs from the same plan so
    stub_0 in log_a corresponds to stub_0 in log_b.
    """
    def extract_stub_interactions(log):
        # dict of stub_name -> list of ('call', args) | ('return', value) in order
        interactions = {}
        for entry in log:
            name = entry['function']
            if not name.startswith(STUB_PREFIX):
                continue
            if name not in interactions:
                interactions[name] = []
            if entry['event'] == 'call':
                interactions[name].append(('call', entry.get('arguments', {})))
            elif entry['event'] == 'return':
                interactions[name].append(('return', entry['return_value']))
        return interactions

    stubs_a = extract_stub_interactions(log_a)
    stubs_b = extract_stub_interactions(log_b)

    all_stubs = sorted(set(stubs_a) | set(stubs_b))

    for stub_name in all_stubs:
        if stub_name not in stubs_a:
            return False, f"Stub {stub_name} was called in B but never in A"
        if stub_name not in stubs_b:
            return False, f"Stub {stub_name} was called in A but never in B"

        seq_a = stubs_a[stub_name]
        seq_b = stubs_b[stub_name]

        if len(seq_a) != len(seq_b):
            calls_a = sum(1 for e in seq_a if e[0] == 'call')
            calls_b = sum(1 for e in seq_b if e[0] == 'call')
            return False, (
                f"Stub {stub_name} called {calls_a} times in A but {calls_b} times in B"
            )

        for i, (entry_a, entry_b) in enumerate(zip(seq_a, seq_b)):
            kind_a, val_a = entry_a
            kind_b, val_b = entry_b
            if kind_a != kind_b:
                return False, (
                    f"Stub {stub_name} interaction {i} type mismatch: {kind_a} vs {kind_b}"
                )
            if not return_value_equivalence(val_a, val_b):
                return False, (
                    f"Stub {stub_name} {kind_a} mismatch at interaction {i}: "
                    f"A={val_a!r}, B={val_b!r}"
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