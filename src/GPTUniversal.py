# universal.py
import random
import string
import operator
import hashlib
from functools import lru_cache

"""
GPT generated Universal object made to use Hypofuzz. 
Doesn't seem to work.
"""

# helper: deterministic RNG from (seed, key)
def _rng_for(seed: int, key: str) -> random.Random:
    # produce a deterministic 64-bit seed from (seed, key)
    h = hashlib.sha256(f"{seed}|{key}".encode("utf-8")).digest()
    # take 8 bytes -> int
    rnd_seed = int.from_bytes(h[:8], "big")
    return random.Random(rnd_seed)

class Universal:
    """
    A 'universal' placeholder. Construct with a seed (int) and an optional path tuple.
    Concrete values for coercions are derived deterministically using (seed, path, typename).
    """
    def __init__(self, seed: int, path: tuple = ()):
        self._seed = int(seed)
        self._path = tuple(path)
        self._cache = {}  # maps (typename, extra) -> concrete value

    def _key(self, typename: str, extra: str = "") -> str:
        # create a single stable string key
        return "/".join(map(str, (self._seed,)+self._path+(typename,extra)))

    def _derive(self, typename: str, extra: str = ""):
        k = (typename, extra)
        if k in self._cache:
            return self._cache[k]
        rng = _rng_for(self._seed, self._key(typename, extra))

        if typename == "int":
            # default: 32-bit signed-ish range
            val = rng.randint(-2**31, 2**31-1)
        elif typename == "float":
            # float in a reasonable range
            val = rng.uniform(-1e6, 1e6)
        elif typename == "str":
            length = rng.randint(0, 50)
            # printable subset
            val = "".join(rng.choice(string.ascii_letters + string.digits + " _-") for _ in range(length))
        elif typename == "bytes":
            length = rng.randint(0, 50)
            val = bytes(rng.getrandbits(8) for _ in range(length))
        elif typename == "bool":
            val = rng.choice([False, True])
        elif typename == "list":
            n = rng.randint(0, 6)
            # list of small primitive values (could also be Universals)
            vals = []
            for i in range(n):
                # choose a primitive type to populate the list
                t = rng.choice(["int", "float", "str", "bool"])
                vals.append(self._derive(t, f"listidx{i}"))
            val = vals
        elif typename == "dict":
            n = rng.randint(0, 6)
            d = {}
            for i in range(n):
                kstr = self._derive("str", f"dictkey{i}") or ""
                v = self._derive(rng.choice(["int","float","str","bool"]), f"dictval{i}")
                d[kstr] = v
            val = d
        elif typename == "iter":
            # produce a list and return iterator later
            val = self._derive("list", extra)
        else:
            # fallback: return None
            val = None

        self._cache[k] = val
        return val

    # Primitive coercions
    def __int__(self):
        return int(self._derive("int"))
    def __index__(self):
        return self.__int__()
    def __float__(self):
        return float(self._derive("float"))
    def __complex__(self):
        return complex(self._derive("float"))
    def __str__(self):
        s = self._derive("str")
        return s if s is not None else object.__str__(self)
    def __bytes__(self):
        b = self._derive("bytes")
        return b if b is not None else b""
    def __bool__(self):
        return bool(self._derive("bool"))

    # Sequence / mapping protocols
    def __len__(self):
        seq = self._derive("list")
        try:
            return len(seq)
        except Exception:
            return 0
    def __iter__(self):
        seq = self._derive("iter")
        if seq is None:
            return iter(())
        return iter(seq)
    def __getitem__(self, key):
        # if key is integer -> map to list index; else -> dict lookup
        if isinstance(key, int):
            lst = self._derive("list")
            try:
                return lst[key]
            except Exception:
                # out-of-range: return a new Universal derived for this index
                return Universal(self._seed, self._path + (f"idx:{key}",))
        else:
            d = self._derive("dict")
            return d.get(str(key), Universal(self._seed, self._path + (f"item:{key}",)))

    # attribute access: create a new Universal for that attribute path
    def __getattr__(self, name):
        # avoid interfering with internals
        if name.startswith("_"):
            raise AttributeError(name)
        return Universal(self._seed, self._path + (f"attr:{name}",))

    # calling a Universal returns another Universal or a derived primitive (configurable)
    def __call__(self, *args, **kwargs):
        # create a new Universal whose path encodes the call + args/kwargs fingerprints
        arg_key = f"call({len(args)},{len(kwargs)})"
        return Universal(self._seed, self._path + (arg_key,))

    # binary numeric operations: prefer integer if both can be ints, else float
    def _coerce_for_numeric(self, other):
        # coerce self to int/float
        try:
            a = int(self)
            # if other is also Universal, attempt int, else use other's numeric
            if isinstance(other, Universal):
                try:
                    b = int(other)
                    return ("int", a, b)
                except Exception:
                    b = float(other)
                    return ("float", float(a), float(b))
            else:
                # not Universal: use other as-is
                if isinstance(other, float):
                    return ("float", float(a), other)
                return ("int", a, other)
        except Exception:
            # fallback to float
            return ("float", float(self), float(other))

    def _binary_op(self, other, op):
        if isinstance(other, Universal):
            kind, a, b = self._coerce_for_numeric(other)
        else:
            # other is concrete
            try:
                a = int(self)
                b = other
                return op(a, b)
            except Exception:
                a = float(self)
                return op(a, other)
        return op(a, b)

    # implement common numeric dunders
    def __add__(self, other): return self._binary_op(other, operator.add)
    def __radd__(self, other): return self._binary_op(other, operator.add)
    def __sub__(self, other): return self._binary_op(other, operator.sub)
    def __rsub__(self, other): return self._binary_op(other, lambda x,y: operator.sub(y,x))
    def __mul__(self, other): return self._binary_op(other, operator.mul)
    def __rmul__(self, other): return self._binary_op(other, operator.mul)
    def __truediv__(self, other): return self._binary_op(other, operator.truediv)
    def __rtruediv__(self, other): return self._binary_op(other, lambda x,y: operator.truediv(y,x))

    # comparisons: coerce to str if both appear stringable, else try numeric
    def __eq__(self, other):
        if isinstance(other, Universal):
            # compare derived canonical repr for deterministic compare
            return self._derive("str") == other._derive("str")
        else:
            # try compare with str first, then numeric
            try:
                return self._derive("str") == str(other)
            except Exception:
                try:
                    return float(self) == float(other)
                except Exception:
                    return False
    def __lt__(self, other):
        if isinstance(other, Universal):
            return self._derive("str") < other._derive("str")
        try:
            return float(self) < float(other)
        except Exception:
            return str(self) < str(other)

    # repr is useful for debugging
    def __repr__(self):
        return f"<Universal seed={self._seed} path={self._path!r}>"
