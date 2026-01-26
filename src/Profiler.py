import re


class Profiler:
    def __init__(self):
        self.call_stack = []
        self.trace_log = []

    def profile(self, frame, event, arg):
        if event == "call":
            func_name = frame.f_code.co_name
            self.call_stack.append(func_name)
            self.trace_log.append({
                "event": "call",
                "function": func_name,
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


def are_equivalent(log_a, log_b):
    top_func_name_a = log_a[0]['function']
    top_func_name_b = log_b[0]['function']
    function_re = r"<function.{1,100}<locals>.{1,100}at 0x.{1,100}>"

    def is_function(val):
        return re.match(function_re, str(val)) is not None
    log_a_returns = []
    log_b_returns = []
    i = 0
    while i < max(len(log_a), len(log_b)):
        # for the nth return from top level in log_a, the nth return from top level in log_b needs to have same value
        # unless it is a func
        # they also need same number of calls and returns to top level??
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
        if is_function(return_a) and is_function(return_b):
            continue
        if is_function(return_a) != is_function(return_b):
            return False, index
        if return_a != return_b:
            return False, index

    return True, -1
