# fuzz_compare.py
# Requires: atheris (Google Atheris)
# This file defines:
#   - Universal: deterministic, lock-on-first-use, nested Universals
#   - TestOneInput: atheris entrypoint that builds args/kwargs of Universals
#   - compare invocation that asserts func_a and func_b behave identically

import sys
import atheris
import traceback
from TestFunctions import *

# ----------------------------
# Replace these two with your functions under test.
# They must be available in this file or imported.
# For demonstration, func_a and func_b are trivial and identical.
# ----------------------------
def func_a(*args, **kwargs):
    # Example behavior: sum of ints in positional args if possible
    total = 0
    for x in args:
        try:
            total += int(x)
        except Exception:
            pass
    return total

def func_b(*args, **kwargs):
    total = 0
    for x in args:
        try:
            if x > 7:
                total += 1
            else:
                total += int(x)
        except Exception:
            pass
    return total

# ----------------------------
# Universal object definition
# ----------------------------
class Universal:
    """
    Universal object driven by an atheris.FuzzedDataProvider.
    Locks into a 'family' on first meaningful use and caches a deterministic
    base value derived from the fuzz bytes. Supports nested Universals for iterables
    and mappings. Callable Universals return another Universal deterministically.
    """
    def __init__(self, fdp):
        self.fdp = fdp
        self._role = None      # e.g., "number", "string", "iterable", "mapping", "callable", "attr:<name>"
        self._value = None     # base cached value (int, str, list of Universals, dict of Universals, Universal for call returns)
        self._call_count = 0   # optional usage if you want per-call variation later

    def __repr__(self):
        return f"<Universal role={self._role!r} value={self._repr_value()}>"

    def _repr_value(self):
        if self._value is None:
            return None
        # Avoid deep recursion in repr; give summary
        if self._role == "number":
            return int(self._value)
        if self._role == "string":
            return self._value
        if self._role == "iterable":
            return f"len={len(self._value)}"
        if self._role == "mapping":
            return f"keys={list(self._value.keys())}"
        if self._role == "callable":
            return "<callable>"
        return "<value>"

    def _ensure_locked(self, role, factory):
        """If not locked, lock to role with factory(); otherwise assert same family."""
        if self._role is None:
            self._role = role
            self._value = factory()
        if self._role != role:
            # Allow some cross-family conversions handled in methods; otherwise error
            return False
        return True

    # -------- number family ----------
    def __int__(self):
        # If locked string, try parsing like int(str_obj) semantics
        if self._role == "string":
            return int(self._value)  # may raise ValueError
        # Lock as number and return integer
        ok = self._ensure_locked("number", lambda: int(self.fdp.ConsumeIntInRange(-1000000, 1000000)))
        if ok:
            return int(self._value)
        # if role differs, but maybe role == "iterable" etc -> try to behave like int(...) of that base
        if self._role == "iterable":
            # int(list) -> TypeError normally; emulate that by raising TypeError
            raise TypeError("int() argument must be a string, a bytes-like object or a number, not 'list'")
        raise TypeError(f"Universal locked as {self._role!r}, cannot cast to int")

    def __float__(self):
        if self._role == "string":
            return float(self._value)
        ok = self._ensure_locked("number", lambda: float(self.fdp.ConsumeFloat()))
        if ok:
            return float(self._value)
        if self._role == "iterable":
            raise TypeError("float() argument must be a string or a number, not 'list'")
        raise TypeError(f"Universal locked as {self._role!r}, cannot cast to float")

    def __bool__(self):
        # bool from number/string/iterable/mapping/callable behave like Python does:
        if self._role == "number":
            return bool(self._value)
        if self._role == "string":
            return bool(self._value)
        if self._role == "iterable":
            return bool(self._value)  # list truthiness
        if self._role == "mapping":
            return bool(self._value)
        if self._role == "callable":
            return True  # functions are truthy
        # Lock as number by default if no prior role (so bool(Univ) is deterministic)
        self._ensure_locked("number", lambda: int(self.fdp.ConsumeIntInRange(0, 1)))
        return bool(self._value)

    # -------- string family ----------
    def __str__(self):
        # If number locked, return its string representation
        if self._role == "number":
            return str(self._value)
        if self._role == "iterable":
            # show list repr when stringified (similar to str(list_obj))
            return str([_repr_for_str(e) for e in self._value])
        if self._role == "mapping":
            return str({k: _repr_for_str(v) for k, v in self._value.items()})
        if self._role == "callable":
            return "<Universal function>"
        # otherwise lock as string
        ok = self._ensure_locked("string", lambda: self.fdp.ConsumeUnicodeNoSurrogates(16))
        if ok:
            return self._value
        raise TypeError(f"Universal locked as {self._role!r}, cannot cast to str")

    def __repr__(self):
        # want a short deterministic repr for debugging
        if self._role is None:
            return "<Universal (unlocked)>"
        return f"<Universal role={self._role} v={_repr_for_str(self._value)}>"

    # -------- iterable family ----------
    def __iter__(self):
        # Lock as iterable, generating a list of nested Universals
        if self._role is None:
            length = self.fdp.ConsumeIntInRange(0, 5)
            # Create nested Universals; each gets the same fdp so will draw deterministically in order
            inner = [Universal(self.fdp) for _ in range(length)]
            self._role = "iterable"
            self._value = inner
            return iter(self._value)
        if self._role == "iterable":
            return iter(self._value)
        # Allow iterating over string: iter(str) returns iterator of chars (but we will yield strings of chars)
        if self._role == "string":
            return iter(self._value)
        raise TypeError(f"Universal locked as {self._role!r}, not iterable")

    def __len__(self):
        if self._role == "iterable":
            return len(self._value)
        if self._role == "string":
            return len(self._value)
        # default behavior: lock as iterable with zero length
        self._ensure_locked("iterable", lambda: [])
        return 0

    def __getitem__(self, key):
        # If mapping, return observed value or Universal; if iterable, support integer indexing
        if self._role == "mapping":
            return self._value[key]
        if self._role == "iterable":
            # accept integer indexing for list of Universals
            return self._value[key]
        if self._role == "string":
            return self._value[key]
        # If not yet locked, create mapping with a few keys
        if self._role is None:
            size = self.fdp.ConsumeIntInRange(0, 4)
            d = {}
            for _ in range(size):
                k = self.fdp.ConsumeUnicodeNoSurrogates(8)
                d[k] = Universal(self.fdp)
            self._role = "mapping"
            self._value = d
            return self._value[key]
        raise TypeError(f"Universal locked as {self._role!r}, not subscriptable")

    # -------- mapping family helpers ----------
    def items(self):
        if self._role == "mapping":
            return self._value.items()
        raise TypeError(f"Universal locked as {self._role!r}, has no items()")

    # -------- attribute / dynamic attr ----------
    def __getattr__(self, name):
        # Return a nested Universal for attribute access; attributes lock as attr:<name>
        # If already locked and not attr, raise
        if self._role is None:
            # lock as attr container
            self._role = f"attr:{name}"
            self._value = Universal(self.fdp)
            return self._value
        # If this Universal is already an attr:<something> and request same name, return cached
        if isinstance(self._role, str) and self._role.startswith("attr:") and self._role == f"attr:{name}":
            return self._value
        # If locked as mapping, try keys
        if self._role == "mapping" and name in self._value:
            return self._value[name]
        # If locked as iterable, allow attribute access to return new Universal (but not recommended)
        # Fallback: raise to signal role mismatch
        raise AttributeError(f"Universal locked as {self._role!r}, no attribute {name!r}")

    # -------- callable family ----------
    def __call__(self, *args, **kwargs):
        # If currently a string that looks like "callable()"? treat as callable? No.
        if self._role == "callable":
            # return the same cached Universal return value for determinism
            return self._value
        if self._role is None:
            # Lock as callable; we decide what the callable returns next.
            # For determinism, the callable returns a cached Universal (could be extended to a list of returns)
            ret = Universal(self.fdp)
            self._role = "callable"
            self._value = ret
            return ret
        # If locked as number/string/iterable... calling it is TypeError
        raise TypeError(f"Universal locked as {self._role!r}, not callable")

    # -------- equality (best-effort) ----------
    def __eq__(self, other):
        # For equality comparisons, try to compare observed values where possible
        try:
            return observe(self) == observe(other)
        except Exception:
            # fallback to identity
            return self is other

# ----------------------------
# Observation helpers
# ----------------------------
def _repr_for_str(x):
    if isinstance(x, Universal):
        # show role but avoid deeper recursion
        return f"<U role={x._role}>"
    return repr(x)

def observe(value):
    """
    Convert a value into a JSON-serializable *observation* that captures
    the deterministic behavior of Universals and plain Python objects.
    Observations are nested structures of primitives, lists and dicts.
    """
    # If it's our Universal, materialize based on locked role
    if isinstance(value, Universal):
        role = value._role
        if role is None:
            # nothing forced it; materialize a representation that includes "unlocked"
            return {"__universal_unlocked__": True}
        if role == "number":
            # value._value is numeric
            return {"__universal__": "number", "value": int(value._value)}
        if role == "string":
            return {"__universal__": "string", "value": str(value._value)}
        if role == "iterable":
            return {"__universal__": "iterable", "value": [observe(v) for v in value._value]}
        if role == "mapping":
            return {"__universal__": "mapping", "value": {k: observe(v) for k, v in value._value.items()}}
        if role and role.startswith("attr:"):
            return {"__universal__": "attr", "name": role.split(":", 1)[1], "value": observe(value._value)}
        if role == "callable":
            # represent callable by what it returns when called (deterministic)
            return {"__universal__": "callable", "returns": observe(value._value)}
        # fallback
        return {"__universal__": "unknown", "role": role}
    # For plain builtins:
    if isinstance(value, (int, float, str, bool, type(None))):
        return value
    if isinstance(value, (list, tuple)):
        return [observe(x) for x in value]
    if isinstance(value, dict):
        return {str(k): observe(v) for k, v in value.items()}
    if isinstance(value, Exception):
        return {"__exception__": type(value).__name__, "msg": str(value)}
    # fallback to repr
    return {"__repr__": repr(value)}

# ----------------------------
# Fuzz harness: call two functions with same Universals and compare
# ----------------------------
def TestOneInput(data: bytes):
    fdp = atheris.FuzzedDataProvider(data)

    # Decide number of positional args and kwargs deterministically from FuzzedDataProvider
    n_pos = fdp.ConsumeIntInRange(0, 4)
    n_kw = fdp.ConsumeIntInRange(0, 3)

    # Build positional Universals
    pos_args = [Universal(fdp) for _ in range(n_pos)]

    # Build kwargs with deterministic names (take fuzzed strings but sanitize)
    kwargs = {}
    for i in range(n_kw):
        rawname = fdp.ConsumeUnicodeNoSurrogates(6)
        # sanitize to valid identifier-ish key; if empty, fallback to k{i}
        name = "".join(ch for ch in rawname if ch.isidentifier()) or f"k{i}"
        # ensure unique
        if name in kwargs:
            name = f"{name}_{i}"
        kwargs[name] = Universal(fdp)

    # Also create a Universal that can be used as callback or other shared object
    shared = Universal(fdp)

    # Optionally insert shared into args/kwargs in some deterministic way
    if n_pos > 0 and fdp.ConsumeBool():
        pos_args[0] = shared
    if n_kw > 0 and fdp.ConsumeBool():
        first_key = next(iter(kwargs))
        kwargs[first_key] = shared

    # Helper to call a function and capture outcome (value or exception)
    def call_and_capture(func):
        try:
            out = func(*pos_args, **kwargs)
            return ("return", observe(out))
        except BaseException as e:
            # capture exception type and message and stack for diagnostics
            tb = traceback.format_exc(limit=5)
            return ("exception", {"type": type(e).__name__, "msg": str(e), "trace": tb})

    # Call both functions
    a_out = call_and_capture(func_a)
    b_out = call_and_capture(func_b)

    # Compare observations
    if a_out != b_out:
        # Provide details to help debugging - raise AssertionError so atheris can record the input
        msg = (
            "Behavior mismatch between func_a and func_b\n"
            f"pos_args count: {n_pos}, kwargs: {list(kwargs.keys())}\n"
            f"func_a -> {a_out}\n"
            f"func_b -> {b_out}\n"
            f"pos_args repr: {[repr(p) for p in pos_args]}\n"
            f"kwargs repr: {{ {', '.join(f'{k}: {repr(v)}' for k, v in kwargs.items())} }}\n"
        )
        raise AssertionError(msg)

# ----------------------------
# Main: set up atheris
# ----------------------------
def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    # If you want to debug locally without atheris, you can call TestOneInput with a fixed seed:
    if "--debug-run" in sys.argv:
        # Quick non-coverage deterministic run for debugging
        data = b"debug-seed-bytes-1234567890"
        TestOneInput(data)
        print("Debug run finished (no mismatch detected).")
        sys.exit(0)
    main()
