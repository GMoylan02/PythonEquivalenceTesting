# universal.py
import random
import string
import operator
import hashlib
from functools import lru_cache
from hypothesis import given, strategies as st

"""
Unfinished attempt at an implementation of the Universal object
"""

# helper: deterministic RNG from (seed, key)
def _rng_for(seed: int, key: str) -> random.Random:
    # produce a deterministic 64-bit seed from (seed, key)
    h = hashlib.sha256(f"{seed}|{key}".encode("utf-8")).digest()
    # take 8 bytes -> int
    rnd_seed = int.from_bytes(h[:8], "big")
    return random.Random(rnd_seed)

class Universal:
    def __init__(self, seed: int, path: tuple = ()):
        self._seed = seed
        self._path = path
        self._value = None
        self._role = None

    def _key(self, typename: str, extra: str = "") -> str:
        # create a single stable string key
        return "/".join(map(str, (self._seed,)+self._path+(typename,extra)))

    def __int__(self):
        rng = _rng_for(self._seed, self._key("int"))
        if self._role is None:
            self._role = "int"
            self._value = int(rng.randint(-2**31, 2**31-1))
            return self._value
        if self._role in ("int", "float", "str"):
            return int(self._value)
        if self._role == "iterable":
            raise TypeError("'int' role cannot be iterable")
        raise TypeError(f"Universal locked as {self._role} cannot be cast to int")

    def __float__(self):
        rng = _rng_for(self._seed, self._key("float"))
        if self._role is None:
            self._role = "float"
            self._value = float(rng.uniform(-1e6, 1e6))
            return self._value
        if self._role in ("int", "float", "str"):
            return float(self._value)
        if self._role == "iterable":
            raise TypeError("'float' role cannot be iterable")
        raise TypeError(f"Universal locked as {self._role} cannot be cast to float")

    def __bool__(self):
        rng = _rng_for(self._seed, self._key("bool"))
        if self._role is None:
            self._role = "bool"
            self._value = rng.choice([False, True])
            return self._value
        return bool(self._value)

    def __str__(self):
        rng = _rng_for(self._seed, self._key("str"))
        if self._role is None:
            self._role = "str"
            length = rng.randint(0, 50)
            self._value = "".join(rng.choice(string.ascii_letters + string.digits + " _-") for _ in range(length))
            return self._value
        if self._role in ("int", "float", "str"):
            return str(self._value)
        if self._role == "iterable":
            raise NotImplementedError("Not yet implemented") # TODO
        if self._role == "callable":
            return "<Universal function>"
        raise TypeError(f"Universal locked as {self._role} cannot be cast to str")

    def __iter__(self):
        rng = _rng_for(self._seed, self._key("iter"))
        if self._role is None:
            self._role = "iter"
            length = rng.randint(0, 50)
            self._value = []
            for i in range(length):
                #t = rng.choice(["int", "float", "str", "bool"])
                self._value.append(Universal(self._seed))
                # TODO this may need to be rethought and refactored
            #self._value = [Universal(self._seed) for _ in length]
            return iter(self._value)
        if self._role in ("iter", "str"):
            return iter(self._value)
        raise TypeError(f"Universal locked as {self._role} cannot be cast to iter")
