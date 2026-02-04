import math
import re


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
                # todo this can be used in future for a more correct contextual equivalence
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
supported_datastructures = (list, tuple, dict)

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
        if is_function(list_a[i]) and is_function(list_b[i]):
            continue
        if is_function(list_a[i]) or is_function(list_b[i]):
            return False
        if type(list_a[i]) == type(list_b[i]) and type(list_a[i]) in supported_datastructures:
            return datastruct_equivalence(list_a[i], list_b[i])
        if list_a[i] != list_b[i]:
            return False
    return True

def dict_equivalence(dict_a, dict_b):
    """This works provided dict keys can only be strings"""
    if len(dict_a.keys()) != len(dict_b.keys()):
        return False
    for k in dict_a.keys():
        if is_function(dict_a[k]) and is_function(dict_b[k]):
            continue
        if is_function(dict_a[k]) or is_function(dict_b[k]):
            return False
        if type(dict_a[k]) == type(dict_b[k]) and type(dict_a[k]) in supported_datastructures:
            return datastruct_equivalence(dict_a[k], dict_b[k])
        if dict_a[k] != dict_b[k]:
            return False
    return True


def return_value_equivalence(return_a, return_b):
    if is_function(return_a) and is_function(return_b):
        return True
    if is_function(return_a) != is_function(return_b):
        return False
    if type(return_a) != type(return_b):
        return False
    if type(return_a) == float and (math.isnan(return_a) and math.isnan(return_b)):
        return True
    if type(return_a) in supported_datastructures:
        return datastruct_equivalence(return_a, return_b)
    if return_a != return_b:
        return False
    return True


def are_equivalent(log_a, log_b):
    top_func_name_a = log_a[0]['function']
    top_func_name_b = log_b[0]['function']

    log_a_returns = []
    log_b_returns = []
    i = 0
    while i < max(len(log_a), len(log_b)):
        if i < len(log_a) and log_a[i]['event'] == 'return' and log_a[i]['function'] == top_func_name_a:
            log_a_returns.append((i, log_a[i]))
        if i < len(log_b) and log_b[i]['event'] == 'return' and log_b[i]['function'] == top_func_name_b:
            log_b_returns.append((i, log_b[i]))
        i += 1
    if len(log_a_returns) != len(log_b_returns):
        return False, -1
    for i in range(len(log_a_returns)):
        return_a = log_a_returns[i][1]['return_value']
        return_b = log_b_returns[i][1]['return_value']
        index = log_a_returns[i][0]
        if not return_value_equivalence(return_a, return_b):
            return False, index

    return True, -1
