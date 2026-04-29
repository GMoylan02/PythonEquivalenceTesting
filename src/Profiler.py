import collections
import dis
import inspect
import json
import math
import os
import re
import sys
import tempfile
import traceback
from dataclasses import field, dataclass
from pathlib import Path
from typing import Optional, Callable, Iterator

from src.DummyObject import DummyObject

MAX_OBJECT_DEPTH = 2


class Profiler:
    def __init__(self, coverage_target_func: Optional[Callable] = None):
        self.trace_log = []
        self.call_stack = []
        self.top_level_frame = None
        self.callable_params: set[str] = set()

        self._coverage_code = None
        if coverage_target_func is not None:
            fn = coverage_target_func
            if hasattr(fn, '__func__'):  # unwrap bound method
                fn = fn.__func__
            self._coverage_code = getattr(fn, '__code__', None)

        self.covered_lines: set[int] = set()

    def trace(self, frame, event, arg):
        """
        Global trace — Python only calls this for 'call' events on new frames.
        Return self._local_trace to opt into return/exception for this frame.
        Return None to suppress all tracing inside this frame entirely.
        """
        func_name = frame.f_code.co_name

        if self._coverage_code is not None and frame.f_code is self._coverage_code:
            self.covered_lines.add(frame.f_lineno)
            return self._coverage_local_trace

        if self.top_level_frame is None:
            # First call is always the top-level HOF
            self.top_level_frame = frame
            args_snapshot = self._snapshot_args(frame)
            for val in args_snapshot.values():
                if callable(val) and not isinstance(val, DummyObject):
                    self.callable_params.add(val.__name__)
            self.call_stack.append(func_name)
            self.trace_log.append({
                "event": "call",
                "function": func_name,
                "arguments": args_snapshot,
                "caller": None,
            })
            return self._local_trace

        # Only trace callable params called directly from the HOF frame
        if frame.f_back is self.top_level_frame and func_name in self.callable_params:
            args_snapshot = self._snapshot_args(frame)
            self.call_stack.append(func_name)
            self.trace_log.append({
                "event": "call",
                "function": func_name,
                "arguments": args_snapshot,
                "caller": self.call_stack[-2] if len(self.call_stack) > 1 else None,
            })
            return self._local_trace

        return None

    def _coverage_local_trace(self, frame, event, arg):
        """
        Local trace installed only for the coverage-target frame.
        Records every line event so we know which lines were actually executed.
        This is separate from _local_trace so HOF profiling and coverage tracking
        are completely independent, neither can accidentally interfere with the other.
        """
        if event == "line":
            self.covered_lines.add(frame.f_lineno)
        # Always return self to keep tracing every line inside this frame,
        # including lines inside any nested calls that Python traces back here.
        return self._coverage_local_trace

    def _local_trace(self, frame, event, arg):
        """
        Local trace. only fires for frames that returned self._local_trace above.
        Never called for frames that returned None.
        """
        func_name = frame.f_code.co_name

        if event == "return":
            self.trace_log.append({
                "event": "return",
                "function": func_name,
                "return_value": arg,
            })
            if self.call_stack:
                self.call_stack.pop()

        elif event == "exception":
            # Only record exceptions propagating at the HOF level
            if frame is self.top_level_frame:
                exc_type, exc_value, _ = arg
                self.trace_log.append({
                    "event": "exception",
                    "function": func_name,
                    "exception_type": exc_type,
                    "exception": exc_value,
                })

        return self._local_trace

    def _snapshot_args(self, frame) -> dict:
        code = frame.f_code
        n_pos = code.co_argcount
        n_kw = code.co_kwonlyargcount
        arg_names = set(code.co_varnames[:n_pos + n_kw])
        if code.co_flags & inspect.CO_VARARGS:
            arg_names.add(code.co_varnames[n_pos + n_kw])
        if code.co_flags & inspect.CO_VARKEYWORDS:
            idx = n_pos + n_kw + bool(code.co_flags & inspect.CO_VARARGS)
            arg_names.add(code.co_varnames[idx])
        return {k: v for k, v in frame.f_locals.items() if k in arg_names}

    def clear_logs(self):
        self.trace_log = []
        self.call_stack = []
        self.top_level_frame = None
        self.callable_params = set()
        # deliberately do not reset covered_lines

address_re = re.compile(r' at 0x[0-9a-fA-F]+')

def normalise_string(s):
    """Strip memory addresses from string representations of objects."""
    return address_re.sub(' at 0x?', s)

number_re = re.compile(r'-?\d+(\.\d+)?')
qualname_re = re.compile(r'[\w]+(?:\.(?:<locals>|<[^>]+>|\w+))*(?=\(\))')

def normalise_exception_message(msg: str) -> str:
    """
    Simplify exception messages for comparison, without this, messages like "index x out of range" would raise
    false inequivalences
    """
    msg = address_re.sub('0x?', msg)
    msg = qualname_re.sub('func', msg)
    msg = number_re.sub('#', msg)
    return msg.casefold().strip()

def exception_messages_are_equivalent(exc_a: Exception, exc_b: Exception) -> tuple[bool, str]:
    """
    Compare the normalised messages of two exceptions of the same type
    """
    msg_a = str(exc_a).strip()
    msg_b = str(exc_b).strip()

    if not msg_a and not msg_b:
        return True, ""
    if bool(msg_a) != bool(msg_b):
        return False, (
            f"Exception message presence mismatch: "
            f"A raised {type(exc_a).__name__}({msg_a!r}), "
            f"B raised {type(exc_b).__name__}({msg_b!r})"
        )

    norm_a = normalise_exception_message(msg_a)
    norm_b = normalise_exception_message(msg_b)

    if norm_a != norm_b:
        return False, (
            f"Exception message mismatch:\n"
            f"  A: {type(exc_a).__name__}({msg_a!r})\n"
            f"  B: {type(exc_b).__name__}({msg_b!r})"
        )

    return True, ""


@dataclass
class _LogInfo:
    # trace log frame of the top level function call
    top_call: dict | None = None
    # all params passed to the top level func that are themselves callable
    callable_params: set = field(default_factory=set)
    # filtered version of log containing only calls/returns relating to observer functions
    filtered_log: list = field(default_factory=list)
    # list of all returns from the top level function
    top_level_returns: list = field(default_factory=list)
    # list of all exceptions
    exceptions: list = field(default_factory=list)

# we want to collect all relevant info on a log in a single pass and store them, rather than making multiple passes
def _parse_log(log: list[dict], top_func_name: str) -> _LogInfo:
    parsed = _LogInfo()
    for entry in log:
        event = entry["event"]
        func = entry["function"]
        if parsed.top_call is None:
            if event == "call" and func == top_func_name:
                parsed.top_call = entry
                arguments = entry["arguments"].values()
                for arg in arguments:
                    if callable(arg) and not isinstance(arg, DummyObject):
                        parsed.callable_params.add(arg.__name__)
            continue

        if func in parsed.callable_params:
            parsed.filtered_log.append(entry)

        if event == "return" and func == top_func_name:
            parsed.top_level_returns.append(entry)

        elif event == "exception":
            parsed.exceptions.append(entry)

    return parsed


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

    log_info_a = _parse_log(log_a, top_func_name_a)
    log_info_b = _parse_log(log_b, top_func_name_b)

    if log_info_a.top_call is None or log_info_b.top_call is None:
        return True, ""

    if log_info_a.callable_params != log_info_b.callable_params:
        return False, (
            f"{top_func_name_a} took different callable arguments to {top_func_name_b}: "
            f"{log_info_a.callable_params} != {log_info_b.callable_params}"
        )

    if len(log_info_a.filtered_log) > len(log_info_b.filtered_log):
        return False, f"{top_func_name_a} called its argument more than {top_func_name_b}"
    if len(log_info_a.filtered_log) < len(log_info_b.filtered_log):
        return False, f"{top_func_name_b} called its arguments more than {top_func_name_a}"

    ok, msg = exceptions_are_equivalent(log_info_a.exceptions, log_info_b.exceptions,
                                        strict_exceptions=strict_exceptions)
    if not ok:
        return False, msg
    
    for entry_a, entry_b in zip(log_info_a.filtered_log, log_info_b.filtered_log):
        if "arguments" in entry_a and not value_equivalence(entry_a["arguments"], entry_b["arguments"]):
            return False, (
                f"Observer argument mismatch: {entry_a['function']} received {entry_a['arguments']} "
                f"when {entry_b['function']} received {entry_b['arguments']}"
            )
        if "return_value" in entry_a and not value_equivalence(entry_a["return_value"], entry_b["return_value"]):
            return False, (
                f"Observer return mismatch: {top_func_name_a}.{entry_a['function']} returned a "
                f"different value from {top_func_name_b}.{entry_b['function']}"
            )

    # todo this is redundant
    if log_info_a.top_level_returns and log_info_b.top_level_returns:
        returns_a = log_info_a.top_level_returns[-1]["return_value"]
        returns_b = log_info_b.top_level_returns[-1]["return_value"]
        if not value_equivalence(returns_a, returns_b):
            if kwargs_a:
                return False, (
                    f"Function A: {top_func_name_a}({args_a}, {kwargs_a}) = {returns_a!r}, "
                    f"Function B: {top_func_name_b}({args_b}, {kwargs_b}) = {returns_b!r}"
                )
            return False, (
                f"Function A: {top_func_name_a}{args_a} = {returns_a!r}, "
                f"Function B: {top_func_name_b}{args_b} = {returns_b!r}"
            )

    return True, ""


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


def is_user_object(var):
    # checks if a variable is a user-defined object
    builtin_types = (int, float, complex, str, bool, bytes,
                     list, tuple, set, dict, frozenset, type(None))

    return not isinstance(var, builtin_types) and hasattr(var, "__dict__")


function_re = r"<function.{1,100}at 0x.{1,100}>"

def is_function(val):
    return re.match(function_re, str(val)) is not None


def value_equivalence(value_a, value_b, visited=None):
    """
    Recursively check if two return values are equivalent, allowing them to any combination of primitives,
    objects of a user-defined class, or containers of these
    """
    if value_a is value_b:
        return True

    if value_a is None or value_b is None:
        return False

    if isinstance(value_a, type) and isinstance(value_b, type):
        # if both values are classes, just return True
        return True

    if isinstance(value_a, Iterator) and isinstance(value_b, Iterator):
        # return True for iterators
        return True

    if is_user_object(value_a):
        return value_equivalence(vars(value_a), vars(value_b), visited)

    if type(value_a) is not type(value_b):
        if not (isinstance(value_a, (int, float)) and isinstance(value_b, (int, float))):
            return False

    fa, fb = is_function(value_a), is_function(value_b)
    if fa and fb:
        return True
    if fa != fb:
        return False

    if type(value_a) is float and math.isnan(value_a) and math.isnan(value_b):
        return True

    if isinstance(value_a, str):
        return normalise_string(value_a) == normalise_string(value_b)

    if visited is None:
        visited = set()

    pair = (id(value_a), id(value_b))
    if pair in visited:
        return True
    visited.add(pair)

    if isinstance(value_a, dict):
        if value_a.keys() != value_b.keys():
            return False
        return all(
            value_equivalence(value_a[k], value_b[k], visited)
            for k in value_a
        )

    if isinstance(value_a, (list, tuple)):
        if len(value_a) != len(value_b):
            return False
        return all(
            value_equivalence(x, y, visited)
            for x, y in zip(value_a, value_b)
        )

    return value_a == value_b

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

class CoverageRecorder:
    """
    Accumulates line coverage data for a single mutant function
    ClassEquivalence and FunctionEquivalence write this to self.coverage_file
    """
    def __init__(self, target_func, coverage_file):
        self.coverage_file = coverage_file
        self.covered_lines: set[int] = set()
        # fuzz iterations
        self.iterations = 0
        # for class equivalence, one iteration consists of multiple method calls as we have to sequence calls
        self.method_calls = 0
        fn = getattr(target_func, "__func__", target_func)
        code = getattr(fn, "__code__", None)
        self.total_lines = []
        setup_error = None

        self.failing_init_args = None
        self.failing_init_kwargs = None
        self.failing_method_calls = None

        if code is not None:
            try:
                body_lines = set()
                try:
                    for _, _, ln in code.co_lines():
                        if ln is not None:
                            body_lines.add(ln)
                except AttributeError:
                    for _, ln in dis.findlinestarts(code):
                        if ln is not None:
                            body_lines.add(ln)
                self.total_lines = sorted(body_lines | {code.co_firstlineno})
            except Exception:
                setup_error = traceback.format_exc()

        if setup_error:
            self._write_with_error(setup_error)
        else:
            self._write()

    def increment_iterations(self):
        self.iterations += 1
        self._write()

    def increment_method_calls(self):
        self.method_calls += 1
        self._write()

    def merge(self, new_lines):
        if not new_lines:
            return
        self.covered_lines.update(new_lines)
        self._write()

    def record_input_sequence(self, init_args, init_kwargs, ops, final_state=None):
        """
        Record the constructor args, method call sequence, and method args that caused
        an inequivalence. From this data, we can potentially construct test cases automatically
        """
        self.failing_init_args = init_args
        self.failing_init_kwargs = init_kwargs
        self.failing_method_calls = ops
        self.failing_final_state = final_state
        self._write()

    def _build_report(self):
        payload = {
            "lines_covered": sorted(self.covered_lines),
            "lines_total": self.total_lines,
            "iterations": self.iterations,
            "total_method_calls": self.method_calls,
        }
        if self.failing_init_args is not None:
            # These fields remain unused in the final project, the 'future work' section of the thesis describes
            # using mutation testing results to automatically generate tests: this would have been used for that
            # experiment, but I axed it due to time constraints
            payload["failing_init_args"] = self._make_serializable(self.failing_init_args)
            payload["failing_init_kwargs"] = self._make_serializable(self.failing_init_kwargs)
            payload["failing_method_calls"] = self._make_serializable(self.failing_method_calls)
        return payload

    def _write(self):
        try:
            data = json.dumps(self._build_report())
            tmp_path = self.coverage_file + ".tmp"
            with open(tmp_path, 'w', encoding='utf-8') as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, self.coverage_file)
        except Exception as e:
            print(f"[CoverageRecorder] _write failed: {e}", file=sys.stderr)

    def _write_with_error(self, setup_error: str):
        payload = {
            "lines_covered": [],
            "lines_total": self.total_lines,
            "iterations": self.iterations,
            "total_method_calls": self.method_calls,
            "setup_error": setup_error,
            "failing_init_args": self.failing_init_args,
            "failing_init_kwargs": self.failing_init_kwargs,
            "failing_method_calls": self.failing_method_calls,
            "failing_final_state": self.failing_final_state,
        }
        try:
            with open(self.coverage_file, 'w', encoding='utf-8') as f:
                json.dump(payload, f)
        except Exception:
            pass

    def _make_serializable(self, obj, depth=0):
        if depth > 5:
            return {"__repr__": repr(obj)}
        if obj is None or isinstance(obj, (bool, int, float, str)):
            return obj
        if isinstance(obj, tuple):
            return {"__tuple__": [self._make_serializable(x, depth + 1) for x in obj]}
        if isinstance(obj, list):
            return [self._make_serializable(x, depth + 1) for x in obj]
        if isinstance(obj, dict):
            return {str(k): self._make_serializable(v, depth + 1) for k, v in obj.items()}
        return {"__repr__": repr(obj)}