from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg is not None:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result
class Binheap(object):

    def xǁBinheapǁ__init____mutmut_orig(self, data=None):
        self.container = [None]
        if data:
            for val in data:
                self.push(val)

    def xǁBinheapǁ__init____mutmut_1(self, data=None):
        self.container = None
        if data:
            for val in data:
                self.push(val)

    def xǁBinheapǁ__init____mutmut_2(self, data=None):
        self.container = [None]
        if data:
            for val in data:
                self.push(None)
    
    xǁBinheapǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBinheapǁ__init____mutmut_1': xǁBinheapǁ__init____mutmut_1, 
        'xǁBinheapǁ__init____mutmut_2': xǁBinheapǁ__init____mutmut_2
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBinheapǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁBinheapǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁBinheapǁ__init____mutmut_orig)
    xǁBinheapǁ__init____mutmut_orig.__name__ = 'xǁBinheapǁ__init__'

    def xǁBinheapǁ_balance__mutmut_orig(self):
        size = len(self.container) - 1
        while size // 2 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_1(self):
        size = None
        while size // 2 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_2(self):
        size = len(self.container) + 1
        while size // 2 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_3(self):
        size = len(self.container) - 2
        while size // 2 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_4(self):
        size = len(self.container) - 1
        while size / 2 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_5(self):
        size = len(self.container) - 1
        while size // 3 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_6(self):
        size = len(self.container) - 1
        while size // 2 >= 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_7(self):
        size = len(self.container) - 1
        while size // 2 > 1:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_8(self):
        size = len(self.container) - 1
        while size // 2 > 0:
            if self.container[size] >= self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_9(self):
        size = len(self.container) - 1
        while size // 2 > 0:
            if self.container[size] > self.container[size / 2]:
                tmp = self.container[size // 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_10(self):
        size = len(self.container) - 1
        while size // 2 > 0:
            if self.container[size] > self.container[size // 3]:
                tmp = self.container[size // 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_11(self):
        size = len(self.container) - 1
        while size // 2 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = None
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_12(self):
        size = len(self.container) - 1
        while size // 2 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size / 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_13(self):
        size = len(self.container) - 1
        while size // 2 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 3]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_14(self):
        size = len(self.container) - 1
        while size // 2 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size // 2] = None
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_15(self):
        size = len(self.container) - 1
        while size // 2 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size / 2] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_16(self):
        size = len(self.container) - 1
        while size // 2 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size // 3] = self.container[size]
                self.container[size] = tmp
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_17(self):
        size = len(self.container) - 1
        while size // 2 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = None
            size = size // 2

    def xǁBinheapǁ_balance__mutmut_18(self):
        size = len(self.container) - 1
        while size // 2 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = None

    def xǁBinheapǁ_balance__mutmut_19(self):
        size = len(self.container) - 1
        while size // 2 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size / 2

    def xǁBinheapǁ_balance__mutmut_20(self):
        size = len(self.container) - 1
        while size // 2 > 0:
            if self.container[size] > self.container[size // 2]:
                tmp = self.container[size // 2]
                self.container[size // 2] = self.container[size]
                self.container[size] = tmp
            size = size // 3
    
    xǁBinheapǁ_balance__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBinheapǁ_balance__mutmut_1': xǁBinheapǁ_balance__mutmut_1, 
        'xǁBinheapǁ_balance__mutmut_2': xǁBinheapǁ_balance__mutmut_2, 
        'xǁBinheapǁ_balance__mutmut_3': xǁBinheapǁ_balance__mutmut_3, 
        'xǁBinheapǁ_balance__mutmut_4': xǁBinheapǁ_balance__mutmut_4, 
        'xǁBinheapǁ_balance__mutmut_5': xǁBinheapǁ_balance__mutmut_5, 
        'xǁBinheapǁ_balance__mutmut_6': xǁBinheapǁ_balance__mutmut_6, 
        'xǁBinheapǁ_balance__mutmut_7': xǁBinheapǁ_balance__mutmut_7, 
        'xǁBinheapǁ_balance__mutmut_8': xǁBinheapǁ_balance__mutmut_8, 
        'xǁBinheapǁ_balance__mutmut_9': xǁBinheapǁ_balance__mutmut_9, 
        'xǁBinheapǁ_balance__mutmut_10': xǁBinheapǁ_balance__mutmut_10, 
        'xǁBinheapǁ_balance__mutmut_11': xǁBinheapǁ_balance__mutmut_11, 
        'xǁBinheapǁ_balance__mutmut_12': xǁBinheapǁ_balance__mutmut_12, 
        'xǁBinheapǁ_balance__mutmut_13': xǁBinheapǁ_balance__mutmut_13, 
        'xǁBinheapǁ_balance__mutmut_14': xǁBinheapǁ_balance__mutmut_14, 
        'xǁBinheapǁ_balance__mutmut_15': xǁBinheapǁ_balance__mutmut_15, 
        'xǁBinheapǁ_balance__mutmut_16': xǁBinheapǁ_balance__mutmut_16, 
        'xǁBinheapǁ_balance__mutmut_17': xǁBinheapǁ_balance__mutmut_17, 
        'xǁBinheapǁ_balance__mutmut_18': xǁBinheapǁ_balance__mutmut_18, 
        'xǁBinheapǁ_balance__mutmut_19': xǁBinheapǁ_balance__mutmut_19, 
        'xǁBinheapǁ_balance__mutmut_20': xǁBinheapǁ_balance__mutmut_20
    }
    
    def _balance(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBinheapǁ_balance__mutmut_orig"), object.__getattribute__(self, "xǁBinheapǁ_balance__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _balance.__signature__ = _mutmut_signature(xǁBinheapǁ_balance__mutmut_orig)
    xǁBinheapǁ_balance__mutmut_orig.__name__ = 'xǁBinheapǁ_balance'

    def xǁBinheapǁpush__mutmut_orig(self, val):
        self.container.append(val)
        self._balance()

    def xǁBinheapǁpush__mutmut_1(self, val):
        self.container.append(None)
        self._balance()
    
    xǁBinheapǁpush__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBinheapǁpush__mutmut_1': xǁBinheapǁpush__mutmut_1
    }
    
    def push(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBinheapǁpush__mutmut_orig"), object.__getattribute__(self, "xǁBinheapǁpush__mutmut_mutants"), args, kwargs, self)
        return result 
    
    push.__signature__ = _mutmut_signature(xǁBinheapǁpush__mutmut_orig)
    xǁBinheapǁpush__mutmut_orig.__name__ = 'xǁBinheapǁpush'

    def xǁBinheapǁ_sift_down__mutmut_orig(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_1(self, idx: int):
        size = None
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_2(self, idx: int):
        size = len(self.container) + 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_3(self, idx: int):
        size = len(self.container) - 2
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_4(self, idx: int):
        size = len(self.container) - 1
        while idx / 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_5(self, idx: int):
        size = len(self.container) - 1
        while idx * 3 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_6(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 < size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_7(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = None
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_8(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx / 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_9(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 3
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_10(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size or self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_11(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 - 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_12(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx / 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_13(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 3 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_14(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 2 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_15(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 < size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_16(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 - 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_17(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx / 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_18(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 3 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_19(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 2] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_20(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] >= self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_21(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx / 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_22(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 3]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_23(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = None

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_24(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 - 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_25(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx / 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_26(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 3 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_27(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 2

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_28(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] >= self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_29(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = None
                idx = larger_child
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_30(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = None
            else:
                break

    def xǁBinheapǁ_sift_down__mutmut_31(self, idx: int):
        size = len(self.container) - 1
        while idx * 2 <= size:
            larger_child = idx * 2
            if idx * 2 + 1 <= size and self.container[idx * 2 + 1] > self.container[idx * 2]:
                larger_child = idx * 2 + 1

            if self.container[larger_child] > self.container[idx]:
                self.container[idx], self.container[larger_child] = self.container[larger_child], self.container[idx]
                idx = larger_child
            else:
                return
    
    xǁBinheapǁ_sift_down__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBinheapǁ_sift_down__mutmut_1': xǁBinheapǁ_sift_down__mutmut_1, 
        'xǁBinheapǁ_sift_down__mutmut_2': xǁBinheapǁ_sift_down__mutmut_2, 
        'xǁBinheapǁ_sift_down__mutmut_3': xǁBinheapǁ_sift_down__mutmut_3, 
        'xǁBinheapǁ_sift_down__mutmut_4': xǁBinheapǁ_sift_down__mutmut_4, 
        'xǁBinheapǁ_sift_down__mutmut_5': xǁBinheapǁ_sift_down__mutmut_5, 
        'xǁBinheapǁ_sift_down__mutmut_6': xǁBinheapǁ_sift_down__mutmut_6, 
        'xǁBinheapǁ_sift_down__mutmut_7': xǁBinheapǁ_sift_down__mutmut_7, 
        'xǁBinheapǁ_sift_down__mutmut_8': xǁBinheapǁ_sift_down__mutmut_8, 
        'xǁBinheapǁ_sift_down__mutmut_9': xǁBinheapǁ_sift_down__mutmut_9, 
        'xǁBinheapǁ_sift_down__mutmut_10': xǁBinheapǁ_sift_down__mutmut_10, 
        'xǁBinheapǁ_sift_down__mutmut_11': xǁBinheapǁ_sift_down__mutmut_11, 
        'xǁBinheapǁ_sift_down__mutmut_12': xǁBinheapǁ_sift_down__mutmut_12, 
        'xǁBinheapǁ_sift_down__mutmut_13': xǁBinheapǁ_sift_down__mutmut_13, 
        'xǁBinheapǁ_sift_down__mutmut_14': xǁBinheapǁ_sift_down__mutmut_14, 
        'xǁBinheapǁ_sift_down__mutmut_15': xǁBinheapǁ_sift_down__mutmut_15, 
        'xǁBinheapǁ_sift_down__mutmut_16': xǁBinheapǁ_sift_down__mutmut_16, 
        'xǁBinheapǁ_sift_down__mutmut_17': xǁBinheapǁ_sift_down__mutmut_17, 
        'xǁBinheapǁ_sift_down__mutmut_18': xǁBinheapǁ_sift_down__mutmut_18, 
        'xǁBinheapǁ_sift_down__mutmut_19': xǁBinheapǁ_sift_down__mutmut_19, 
        'xǁBinheapǁ_sift_down__mutmut_20': xǁBinheapǁ_sift_down__mutmut_20, 
        'xǁBinheapǁ_sift_down__mutmut_21': xǁBinheapǁ_sift_down__mutmut_21, 
        'xǁBinheapǁ_sift_down__mutmut_22': xǁBinheapǁ_sift_down__mutmut_22, 
        'xǁBinheapǁ_sift_down__mutmut_23': xǁBinheapǁ_sift_down__mutmut_23, 
        'xǁBinheapǁ_sift_down__mutmut_24': xǁBinheapǁ_sift_down__mutmut_24, 
        'xǁBinheapǁ_sift_down__mutmut_25': xǁBinheapǁ_sift_down__mutmut_25, 
        'xǁBinheapǁ_sift_down__mutmut_26': xǁBinheapǁ_sift_down__mutmut_26, 
        'xǁBinheapǁ_sift_down__mutmut_27': xǁBinheapǁ_sift_down__mutmut_27, 
        'xǁBinheapǁ_sift_down__mutmut_28': xǁBinheapǁ_sift_down__mutmut_28, 
        'xǁBinheapǁ_sift_down__mutmut_29': xǁBinheapǁ_sift_down__mutmut_29, 
        'xǁBinheapǁ_sift_down__mutmut_30': xǁBinheapǁ_sift_down__mutmut_30, 
        'xǁBinheapǁ_sift_down__mutmut_31': xǁBinheapǁ_sift_down__mutmut_31
    }
    
    def _sift_down(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBinheapǁ_sift_down__mutmut_orig"), object.__getattribute__(self, "xǁBinheapǁ_sift_down__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _sift_down.__signature__ = _mutmut_signature(xǁBinheapǁ_sift_down__mutmut_orig)
    xǁBinheapǁ_sift_down__mutmut_orig.__name__ = 'xǁBinheapǁ_sift_down'

    def xǁBinheapǁpop__mutmut_orig(self):
        if len(self.container) < 2:
            raise IndexError("Can't pop from an empty heap")

        max_val = self.container[1]

        self.container[1] = self.container[-1]
        self.container.pop()

        if len(self.container) > 1:
            self._sift_down(1)

        return max_val

    def xǁBinheapǁpop__mutmut_1(self):
        if len(self.container) <= 2:
            raise IndexError("Can't pop from an empty heap")

        max_val = self.container[1]

        self.container[1] = self.container[-1]
        self.container.pop()

        if len(self.container) > 1:
            self._sift_down(1)

        return max_val

    def xǁBinheapǁpop__mutmut_2(self):
        if len(self.container) < 3:
            raise IndexError("Can't pop from an empty heap")

        max_val = self.container[1]

        self.container[1] = self.container[-1]
        self.container.pop()

        if len(self.container) > 1:
            self._sift_down(1)

        return max_val

    def xǁBinheapǁpop__mutmut_3(self):
        if len(self.container) < 2:
            raise IndexError(None)

        max_val = self.container[1]

        self.container[1] = self.container[-1]
        self.container.pop()

        if len(self.container) > 1:
            self._sift_down(1)

        return max_val

    def xǁBinheapǁpop__mutmut_4(self):
        if len(self.container) < 2:
            raise IndexError("XXCan't pop from an empty heapXX")

        max_val = self.container[1]

        self.container[1] = self.container[-1]
        self.container.pop()

        if len(self.container) > 1:
            self._sift_down(1)

        return max_val

    def xǁBinheapǁpop__mutmut_5(self):
        if len(self.container) < 2:
            raise IndexError("can't pop from an empty heap")

        max_val = self.container[1]

        self.container[1] = self.container[-1]
        self.container.pop()

        if len(self.container) > 1:
            self._sift_down(1)

        return max_val

    def xǁBinheapǁpop__mutmut_6(self):
        if len(self.container) < 2:
            raise IndexError("CAN'T POP FROM AN EMPTY HEAP")

        max_val = self.container[1]

        self.container[1] = self.container[-1]
        self.container.pop()

        if len(self.container) > 1:
            self._sift_down(1)

        return max_val

    def xǁBinheapǁpop__mutmut_7(self):
        if len(self.container) < 2:
            raise IndexError("Can't pop from an empty heap")

        max_val = None

        self.container[1] = self.container[-1]
        self.container.pop()

        if len(self.container) > 1:
            self._sift_down(1)

        return max_val

    def xǁBinheapǁpop__mutmut_8(self):
        if len(self.container) < 2:
            raise IndexError("Can't pop from an empty heap")

        max_val = self.container[2]

        self.container[1] = self.container[-1]
        self.container.pop()

        if len(self.container) > 1:
            self._sift_down(1)

        return max_val

    def xǁBinheapǁpop__mutmut_9(self):
        if len(self.container) < 2:
            raise IndexError("Can't pop from an empty heap")

        max_val = self.container[1]

        self.container[1] = None
        self.container.pop()

        if len(self.container) > 1:
            self._sift_down(1)

        return max_val

    def xǁBinheapǁpop__mutmut_10(self):
        if len(self.container) < 2:
            raise IndexError("Can't pop from an empty heap")

        max_val = self.container[1]

        self.container[2] = self.container[-1]
        self.container.pop()

        if len(self.container) > 1:
            self._sift_down(1)

        return max_val

    def xǁBinheapǁpop__mutmut_11(self):
        if len(self.container) < 2:
            raise IndexError("Can't pop from an empty heap")

        max_val = self.container[1]

        self.container[1] = self.container[+1]
        self.container.pop()

        if len(self.container) > 1:
            self._sift_down(1)

        return max_val

    def xǁBinheapǁpop__mutmut_12(self):
        if len(self.container) < 2:
            raise IndexError("Can't pop from an empty heap")

        max_val = self.container[1]

        self.container[1] = self.container[-2]
        self.container.pop()

        if len(self.container) > 1:
            self._sift_down(1)

        return max_val

    def xǁBinheapǁpop__mutmut_13(self):
        if len(self.container) < 2:
            raise IndexError("Can't pop from an empty heap")

        max_val = self.container[1]

        self.container[1] = self.container[-1]
        self.container.pop()

        if len(self.container) >= 1:
            self._sift_down(1)

        return max_val

    def xǁBinheapǁpop__mutmut_14(self):
        if len(self.container) < 2:
            raise IndexError("Can't pop from an empty heap")

        max_val = self.container[1]

        self.container[1] = self.container[-1]
        self.container.pop()

        if len(self.container) > 2:
            self._sift_down(1)

        return max_val

    def xǁBinheapǁpop__mutmut_15(self):
        if len(self.container) < 2:
            raise IndexError("Can't pop from an empty heap")

        max_val = self.container[1]

        self.container[1] = self.container[-1]
        self.container.pop()

        if len(self.container) > 1:
            self._sift_down(None)

        return max_val

    def xǁBinheapǁpop__mutmut_16(self):
        if len(self.container) < 2:
            raise IndexError("Can't pop from an empty heap")

        max_val = self.container[1]

        self.container[1] = self.container[-1]
        self.container.pop()

        if len(self.container) > 1:
            self._sift_down(2)

        return max_val
    
    xǁBinheapǁpop__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBinheapǁpop__mutmut_1': xǁBinheapǁpop__mutmut_1, 
        'xǁBinheapǁpop__mutmut_2': xǁBinheapǁpop__mutmut_2, 
        'xǁBinheapǁpop__mutmut_3': xǁBinheapǁpop__mutmut_3, 
        'xǁBinheapǁpop__mutmut_4': xǁBinheapǁpop__mutmut_4, 
        'xǁBinheapǁpop__mutmut_5': xǁBinheapǁpop__mutmut_5, 
        'xǁBinheapǁpop__mutmut_6': xǁBinheapǁpop__mutmut_6, 
        'xǁBinheapǁpop__mutmut_7': xǁBinheapǁpop__mutmut_7, 
        'xǁBinheapǁpop__mutmut_8': xǁBinheapǁpop__mutmut_8, 
        'xǁBinheapǁpop__mutmut_9': xǁBinheapǁpop__mutmut_9, 
        'xǁBinheapǁpop__mutmut_10': xǁBinheapǁpop__mutmut_10, 
        'xǁBinheapǁpop__mutmut_11': xǁBinheapǁpop__mutmut_11, 
        'xǁBinheapǁpop__mutmut_12': xǁBinheapǁpop__mutmut_12, 
        'xǁBinheapǁpop__mutmut_13': xǁBinheapǁpop__mutmut_13, 
        'xǁBinheapǁpop__mutmut_14': xǁBinheapǁpop__mutmut_14, 
        'xǁBinheapǁpop__mutmut_15': xǁBinheapǁpop__mutmut_15, 
        'xǁBinheapǁpop__mutmut_16': xǁBinheapǁpop__mutmut_16
    }
    
    def pop(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBinheapǁpop__mutmut_orig"), object.__getattribute__(self, "xǁBinheapǁpop__mutmut_mutants"), args, kwargs, self)
        return result 
    
    pop.__signature__ = _mutmut_signature(xǁBinheapǁpop__mutmut_orig)
    xǁBinheapǁpop__mutmut_orig.__name__ = 'xǁBinheapǁpop'

    def xǁBinheapǁdisplay__mutmut_orig(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_1(self):
        cols = None
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_2(self):
        cols = []
        col = None
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_3(self):
        cols = []
        col = 2
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_4(self):
        cols = []
        col = 1
        to_show = None
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_5(self):
        cols = []
        col = 1
        to_show = 'XXXX'
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_6(self):
        cols = []
        col = 1
        to_show = ''
        l = None

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_7(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[2:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_8(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) >= col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_9(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(None)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_10(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col = 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_11(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col /= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_12(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 3

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_13(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(None):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_14(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = None
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_15(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] / 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_16(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 + i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_17(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[+1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_18(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-2 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_19(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 3
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_20(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show = buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_21(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show -= buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_22(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff / ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_23(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * 'XX XX'
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_24(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(None):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_25(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show = str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_26(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show -= str(l.pop(0)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_27(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) - ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_28(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(None) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_29(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(None)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_30(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(1)) + ' '
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_31(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + 'XX XX'
            to_show += '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_32(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show = '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_33(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show -= '\n'

        return to_show

    def xǁBinheapǁdisplay__mutmut_34(self):
        cols = []
        col = 1
        to_show = ''
        l = self.container[1:]

        while len(self.container) > col:
            cols.append(col)
            col *= 2

        for i, v in enumerate(cols):
            buff = cols[-1 - i] // 2
            to_show += buff * ' '
            for idx in range(v):
                if l:
                    to_show += str(l.pop(0)) + ' '
            to_show += 'XX\nXX'

        return to_show
    
    xǁBinheapǁdisplay__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBinheapǁdisplay__mutmut_1': xǁBinheapǁdisplay__mutmut_1, 
        'xǁBinheapǁdisplay__mutmut_2': xǁBinheapǁdisplay__mutmut_2, 
        'xǁBinheapǁdisplay__mutmut_3': xǁBinheapǁdisplay__mutmut_3, 
        'xǁBinheapǁdisplay__mutmut_4': xǁBinheapǁdisplay__mutmut_4, 
        'xǁBinheapǁdisplay__mutmut_5': xǁBinheapǁdisplay__mutmut_5, 
        'xǁBinheapǁdisplay__mutmut_6': xǁBinheapǁdisplay__mutmut_6, 
        'xǁBinheapǁdisplay__mutmut_7': xǁBinheapǁdisplay__mutmut_7, 
        'xǁBinheapǁdisplay__mutmut_8': xǁBinheapǁdisplay__mutmut_8, 
        'xǁBinheapǁdisplay__mutmut_9': xǁBinheapǁdisplay__mutmut_9, 
        'xǁBinheapǁdisplay__mutmut_10': xǁBinheapǁdisplay__mutmut_10, 
        'xǁBinheapǁdisplay__mutmut_11': xǁBinheapǁdisplay__mutmut_11, 
        'xǁBinheapǁdisplay__mutmut_12': xǁBinheapǁdisplay__mutmut_12, 
        'xǁBinheapǁdisplay__mutmut_13': xǁBinheapǁdisplay__mutmut_13, 
        'xǁBinheapǁdisplay__mutmut_14': xǁBinheapǁdisplay__mutmut_14, 
        'xǁBinheapǁdisplay__mutmut_15': xǁBinheapǁdisplay__mutmut_15, 
        'xǁBinheapǁdisplay__mutmut_16': xǁBinheapǁdisplay__mutmut_16, 
        'xǁBinheapǁdisplay__mutmut_17': xǁBinheapǁdisplay__mutmut_17, 
        'xǁBinheapǁdisplay__mutmut_18': xǁBinheapǁdisplay__mutmut_18, 
        'xǁBinheapǁdisplay__mutmut_19': xǁBinheapǁdisplay__mutmut_19, 
        'xǁBinheapǁdisplay__mutmut_20': xǁBinheapǁdisplay__mutmut_20, 
        'xǁBinheapǁdisplay__mutmut_21': xǁBinheapǁdisplay__mutmut_21, 
        'xǁBinheapǁdisplay__mutmut_22': xǁBinheapǁdisplay__mutmut_22, 
        'xǁBinheapǁdisplay__mutmut_23': xǁBinheapǁdisplay__mutmut_23, 
        'xǁBinheapǁdisplay__mutmut_24': xǁBinheapǁdisplay__mutmut_24, 
        'xǁBinheapǁdisplay__mutmut_25': xǁBinheapǁdisplay__mutmut_25, 
        'xǁBinheapǁdisplay__mutmut_26': xǁBinheapǁdisplay__mutmut_26, 
        'xǁBinheapǁdisplay__mutmut_27': xǁBinheapǁdisplay__mutmut_27, 
        'xǁBinheapǁdisplay__mutmut_28': xǁBinheapǁdisplay__mutmut_28, 
        'xǁBinheapǁdisplay__mutmut_29': xǁBinheapǁdisplay__mutmut_29, 
        'xǁBinheapǁdisplay__mutmut_30': xǁBinheapǁdisplay__mutmut_30, 
        'xǁBinheapǁdisplay__mutmut_31': xǁBinheapǁdisplay__mutmut_31, 
        'xǁBinheapǁdisplay__mutmut_32': xǁBinheapǁdisplay__mutmut_32, 
        'xǁBinheapǁdisplay__mutmut_33': xǁBinheapǁdisplay__mutmut_33, 
        'xǁBinheapǁdisplay__mutmut_34': xǁBinheapǁdisplay__mutmut_34
    }
    
    def display(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBinheapǁdisplay__mutmut_orig"), object.__getattribute__(self, "xǁBinheapǁdisplay__mutmut_mutants"), args, kwargs, self)
        return result 
    
    display.__signature__ = _mutmut_signature(xǁBinheapǁdisplay__mutmut_orig)
    xǁBinheapǁdisplay__mutmut_orig.__name__ = 'xǁBinheapǁdisplay'
