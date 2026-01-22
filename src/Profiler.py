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
    # we want to compare logs without caring about if the top level function names are the same
    # we also don't want to compare outputs here if the outputs are functions
    if len(log_a) != len(log_b):
        # shouldn't be possible but just in case
        return False, -1
    top_func_name_a = log_a[0]['function']
    top_func_name_b = log_b[0]['function']
    is_top_level = lambda x, y: x == top_func_name_a and y == top_func_name_b
    function_re = r"<function.{1,100}<locals>.{1,100}at 0x.{1,100}>"    # todo something here is wrong
    is_function = lambda x, y: (re.match(function_re, x) is not None
                                and re.match(function_re, y) is not None)

    for i in range(len(log_a)):
        if log_a[i].keys() != log_b[i].keys():
            return False, i
        if log_a[i]['event'] != log_b[i]['event']:
            return False, i
        if (log_a[i]['function'] != log_b[i]['function']
                and not is_top_level(log_a[i]['function'], log_b[i]['function'])):
            # function names in logs must be the same unless they refer to the top level functions
            return False, i
        if ('caller' in log_a[i] and log_a[i]['caller'] != log_b[i]['caller']
                and not is_top_level(log_a[i]['caller'], log_b[i]['caller'])):
            # callers must be the same unless the callers are the top level functions
            return False, i
        if ("return_value" in log_a[i] and log_a[i]['return_value'] != log_b[i]['return_value']
                and not is_function(str(log_a[i]['return_value']), str(log_b[i]['return_value']))):
            # return values must be the same unless return values are themselves functions
            return False, i

    return True, -1
