from .binheap import Binheap
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


class PriorityQ(object):

    def xǁPriorityQǁ__init____mutmut_orig(self):
        self._container = Binheap()

    def xǁPriorityQǁ__init____mutmut_1(self):
        self._container = None
    
    xǁPriorityQǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPriorityQǁ__init____mutmut_1': xǁPriorityQǁ__init____mutmut_1
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPriorityQǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁPriorityQǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁPriorityQǁ__init____mutmut_orig)
    xǁPriorityQǁ__init____mutmut_orig.__name__ = 'xǁPriorityQǁ__init__'

    def xǁPriorityQǁinsert__mutmut_orig(self, val, priority=0):
        self._container.push((priority, val))

    def xǁPriorityQǁinsert__mutmut_1(self, val, priority=1):
        self._container.push((priority, val))

    def xǁPriorityQǁinsert__mutmut_2(self, val, priority=0):
        self._container.push(None)
    
    xǁPriorityQǁinsert__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPriorityQǁinsert__mutmut_1': xǁPriorityQǁinsert__mutmut_1, 
        'xǁPriorityQǁinsert__mutmut_2': xǁPriorityQǁinsert__mutmut_2
    }
    
    def insert(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPriorityQǁinsert__mutmut_orig"), object.__getattribute__(self, "xǁPriorityQǁinsert__mutmut_mutants"), args, kwargs, self)
        return result 
    
    insert.__signature__ = _mutmut_signature(xǁPriorityQǁinsert__mutmut_orig)
    xǁPriorityQǁinsert__mutmut_orig.__name__ = 'xǁPriorityQǁinsert'

    def xǁPriorityQǁpop__mutmut_orig(self):
        if len(self._container.container) < 2:
            raise IndexError("Can't pop from an empty queue.")
        to_return = self._container.container[1][1]
        self._container.pop()
        return to_return

    def xǁPriorityQǁpop__mutmut_1(self):
        if len(self._container.container) <= 2:
            raise IndexError("Can't pop from an empty queue.")
        to_return = self._container.container[1][1]
        self._container.pop()
        return to_return

    def xǁPriorityQǁpop__mutmut_2(self):
        if len(self._container.container) < 3:
            raise IndexError("Can't pop from an empty queue.")
        to_return = self._container.container[1][1]
        self._container.pop()
        return to_return

    def xǁPriorityQǁpop__mutmut_3(self):
        if len(self._container.container) < 2:
            raise IndexError(None)
        to_return = self._container.container[1][1]
        self._container.pop()
        return to_return

    def xǁPriorityQǁpop__mutmut_4(self):
        if len(self._container.container) < 2:
            raise IndexError("XXCan't pop from an empty queue.XX")
        to_return = self._container.container[1][1]
        self._container.pop()
        return to_return

    def xǁPriorityQǁpop__mutmut_5(self):
        if len(self._container.container) < 2:
            raise IndexError("can't pop from an empty queue.")
        to_return = self._container.container[1][1]
        self._container.pop()
        return to_return

    def xǁPriorityQǁpop__mutmut_6(self):
        if len(self._container.container) < 2:
            raise IndexError("CAN'T POP FROM AN EMPTY QUEUE.")
        to_return = self._container.container[1][1]
        self._container.pop()
        return to_return

    def xǁPriorityQǁpop__mutmut_7(self):
        if len(self._container.container) < 2:
            raise IndexError("Can't pop from an empty queue.")
        to_return = None
        self._container.pop()
        return to_return

    def xǁPriorityQǁpop__mutmut_8(self):
        if len(self._container.container) < 2:
            raise IndexError("Can't pop from an empty queue.")
        to_return = self._container.container[2][1]
        self._container.pop()
        return to_return

    def xǁPriorityQǁpop__mutmut_9(self):
        if len(self._container.container) < 2:
            raise IndexError("Can't pop from an empty queue.")
        to_return = self._container.container[1][2]
        self._container.pop()
        return to_return
    
    xǁPriorityQǁpop__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPriorityQǁpop__mutmut_1': xǁPriorityQǁpop__mutmut_1, 
        'xǁPriorityQǁpop__mutmut_2': xǁPriorityQǁpop__mutmut_2, 
        'xǁPriorityQǁpop__mutmut_3': xǁPriorityQǁpop__mutmut_3, 
        'xǁPriorityQǁpop__mutmut_4': xǁPriorityQǁpop__mutmut_4, 
        'xǁPriorityQǁpop__mutmut_5': xǁPriorityQǁpop__mutmut_5, 
        'xǁPriorityQǁpop__mutmut_6': xǁPriorityQǁpop__mutmut_6, 
        'xǁPriorityQǁpop__mutmut_7': xǁPriorityQǁpop__mutmut_7, 
        'xǁPriorityQǁpop__mutmut_8': xǁPriorityQǁpop__mutmut_8, 
        'xǁPriorityQǁpop__mutmut_9': xǁPriorityQǁpop__mutmut_9
    }
    
    def pop(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPriorityQǁpop__mutmut_orig"), object.__getattribute__(self, "xǁPriorityQǁpop__mutmut_mutants"), args, kwargs, self)
        return result 
    
    pop.__signature__ = _mutmut_signature(xǁPriorityQǁpop__mutmut_orig)
    xǁPriorityQǁpop__mutmut_orig.__name__ = 'xǁPriorityQǁpop'

    def xǁPriorityQǁpeek__mutmut_orig(self):
        try:
            return self._container.container[1][1]
        except IndexError:
            return None

    def xǁPriorityQǁpeek__mutmut_1(self):
        try:
            return self._container.container[2][1]
        except IndexError:
            return None

    def xǁPriorityQǁpeek__mutmut_2(self):
        try:
            return self._container.container[1][2]
        except IndexError:
            return None
    
    xǁPriorityQǁpeek__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPriorityQǁpeek__mutmut_1': xǁPriorityQǁpeek__mutmut_1, 
        'xǁPriorityQǁpeek__mutmut_2': xǁPriorityQǁpeek__mutmut_2
    }
    
    def peek(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPriorityQǁpeek__mutmut_orig"), object.__getattribute__(self, "xǁPriorityQǁpeek__mutmut_mutants"), args, kwargs, self)
        return result 
    
    peek.__signature__ = _mutmut_signature(xǁPriorityQǁpeek__mutmut_orig)
    xǁPriorityQǁpeek__mutmut_orig.__name__ = 'xǁPriorityQǁpeek'