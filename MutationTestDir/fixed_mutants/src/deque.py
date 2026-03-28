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
class Deque(object):

    def xǁDequeǁ__init____mutmut_orig(self, data=None):
        self.queue = []
        if data:
            for val in data:
                self.append(val)

    def xǁDequeǁ__init____mutmut_1(self, data=None):
        self.queue = None
        if data:
            for val in data:
                self.append(val)

    def xǁDequeǁ__init____mutmut_2(self, data=None):
        self.queue = []
        if data:
            for val in data:
                self.append(None)
    
    xǁDequeǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDequeǁ__init____mutmut_1': xǁDequeǁ__init____mutmut_1, 
        'xǁDequeǁ__init____mutmut_2': xǁDequeǁ__init____mutmut_2
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDequeǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁDequeǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁDequeǁ__init____mutmut_orig)
    xǁDequeǁ__init____mutmut_orig.__name__ = 'xǁDequeǁ__init__'

    def xǁDequeǁappend__mutmut_orig(self, val):
        self.queue.append(val)

    def xǁDequeǁappend__mutmut_1(self, val):
        self.queue.append(None)
    
    xǁDequeǁappend__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDequeǁappend__mutmut_1': xǁDequeǁappend__mutmut_1
    }
    
    def append(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDequeǁappend__mutmut_orig"), object.__getattribute__(self, "xǁDequeǁappend__mutmut_mutants"), args, kwargs, self)
        return result 
    
    append.__signature__ = _mutmut_signature(xǁDequeǁappend__mutmut_orig)
    xǁDequeǁappend__mutmut_orig.__name__ = 'xǁDequeǁappend'

    def xǁDequeǁappendleft__mutmut_orig(self, val):
        self.queue.insert(0, val)

    def xǁDequeǁappendleft__mutmut_1(self, val):
        self.queue.insert(None, val)

    def xǁDequeǁappendleft__mutmut_2(self, val):
        self.queue.insert(0, None)

    def xǁDequeǁappendleft__mutmut_3(self, val):
        self.queue.insert(val)

    def xǁDequeǁappendleft__mutmut_4(self, val):
        self.queue.insert(0, )

    def xǁDequeǁappendleft__mutmut_5(self, val):
        self.queue.insert(1, val)
    
    xǁDequeǁappendleft__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDequeǁappendleft__mutmut_1': xǁDequeǁappendleft__mutmut_1, 
        'xǁDequeǁappendleft__mutmut_2': xǁDequeǁappendleft__mutmut_2, 
        'xǁDequeǁappendleft__mutmut_3': xǁDequeǁappendleft__mutmut_3, 
        'xǁDequeǁappendleft__mutmut_4': xǁDequeǁappendleft__mutmut_4, 
        'xǁDequeǁappendleft__mutmut_5': xǁDequeǁappendleft__mutmut_5
    }
    
    def appendleft(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDequeǁappendleft__mutmut_orig"), object.__getattribute__(self, "xǁDequeǁappendleft__mutmut_mutants"), args, kwargs, self)
        return result 
    
    appendleft.__signature__ = _mutmut_signature(xǁDequeǁappendleft__mutmut_orig)
    xǁDequeǁappendleft__mutmut_orig.__name__ = 'xǁDequeǁappendleft'

    def xǁDequeǁpop__mutmut_orig(self):
        if self.isEmpty():
            raise IndexError(None)
        return self.queue.pop(-1)

    def xǁDequeǁpop__mutmut_1(self):
        if self.isEmpty():
            raise IndexError(None)
        return self.queue.pop(None)

    def xǁDequeǁpop__mutmut_2(self):
        if self.isEmpty():
            raise IndexError(None)
        return self.queue.pop(+1)

    def xǁDequeǁpop__mutmut_3(self):
        if self.isEmpty():
            raise IndexError(None)
        return self.queue.pop(-2)
    
    xǁDequeǁpop__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDequeǁpop__mutmut_1': xǁDequeǁpop__mutmut_1, 
        'xǁDequeǁpop__mutmut_2': xǁDequeǁpop__mutmut_2, 
        'xǁDequeǁpop__mutmut_3': xǁDequeǁpop__mutmut_3
    }
    
    def pop(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDequeǁpop__mutmut_orig"), object.__getattribute__(self, "xǁDequeǁpop__mutmut_mutants"), args, kwargs, self)
        return result 
    
    pop.__signature__ = _mutmut_signature(xǁDequeǁpop__mutmut_orig)
    xǁDequeǁpop__mutmut_orig.__name__ = 'xǁDequeǁpop'

    def xǁDequeǁpopleft__mutmut_orig(self):
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self.queue.pop(0)

    def xǁDequeǁpopleft__mutmut_1(self):
        if self.isEmpty():
            raise IndexError(None)
        return self.queue.pop(0)

    def xǁDequeǁpopleft__mutmut_2(self):
        if self.isEmpty():
            raise IndexError("XXQueue is emptyXX")
        return self.queue.pop(0)

    def xǁDequeǁpopleft__mutmut_3(self):
        if self.isEmpty():
            raise IndexError("queue is empty")
        return self.queue.pop(0)

    def xǁDequeǁpopleft__mutmut_4(self):
        if self.isEmpty():
            raise IndexError("QUEUE IS EMPTY")
        return self.queue.pop(0)

    def xǁDequeǁpopleft__mutmut_5(self):
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self.queue.pop(None)

    def xǁDequeǁpopleft__mutmut_6(self):
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self.queue.pop(1)
    
    xǁDequeǁpopleft__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDequeǁpopleft__mutmut_1': xǁDequeǁpopleft__mutmut_1, 
        'xǁDequeǁpopleft__mutmut_2': xǁDequeǁpopleft__mutmut_2, 
        'xǁDequeǁpopleft__mutmut_3': xǁDequeǁpopleft__mutmut_3, 
        'xǁDequeǁpopleft__mutmut_4': xǁDequeǁpopleft__mutmut_4, 
        'xǁDequeǁpopleft__mutmut_5': xǁDequeǁpopleft__mutmut_5, 
        'xǁDequeǁpopleft__mutmut_6': xǁDequeǁpopleft__mutmut_6
    }
    
    def popleft(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDequeǁpopleft__mutmut_orig"), object.__getattribute__(self, "xǁDequeǁpopleft__mutmut_mutants"), args, kwargs, self)
        return result 
    
    popleft.__signature__ = _mutmut_signature(xǁDequeǁpopleft__mutmut_orig)
    xǁDequeǁpopleft__mutmut_orig.__name__ = 'xǁDequeǁpopleft'

    def xǁDequeǁpeek__mutmut_orig(self):
        if self.isEmpty():
            return None
        return self.queue[-1]

    def xǁDequeǁpeek__mutmut_1(self):
        if self.isEmpty():
            return None
        return self.queue[+1]

    def xǁDequeǁpeek__mutmut_2(self):
        if self.isEmpty():
            return None
        return self.queue[-2]
    
    xǁDequeǁpeek__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDequeǁpeek__mutmut_1': xǁDequeǁpeek__mutmut_1, 
        'xǁDequeǁpeek__mutmut_2': xǁDequeǁpeek__mutmut_2
    }
    
    def peek(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDequeǁpeek__mutmut_orig"), object.__getattribute__(self, "xǁDequeǁpeek__mutmut_mutants"), args, kwargs, self)
        return result 
    
    peek.__signature__ = _mutmut_signature(xǁDequeǁpeek__mutmut_orig)
    xǁDequeǁpeek__mutmut_orig.__name__ = 'xǁDequeǁpeek'

    def xǁDequeǁpeekleft__mutmut_orig(self):
        if self.isEmpty():
            return None
        return self.queue[0]

    def xǁDequeǁpeekleft__mutmut_1(self):
        if self.isEmpty():
            return None
        return self.queue[1]
    
    xǁDequeǁpeekleft__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDequeǁpeekleft__mutmut_1': xǁDequeǁpeekleft__mutmut_1
    }
    
    def peekleft(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDequeǁpeekleft__mutmut_orig"), object.__getattribute__(self, "xǁDequeǁpeekleft__mutmut_mutants"), args, kwargs, self)
        return result 
    
    peekleft.__signature__ = _mutmut_signature(xǁDequeǁpeekleft__mutmut_orig)
    xǁDequeǁpeekleft__mutmut_orig.__name__ = 'xǁDequeǁpeekleft'

    def xǁDequeǁisEmpty__mutmut_orig(self):
        return len(self.queue) == 0

    def xǁDequeǁisEmpty__mutmut_1(self):
        return len(self.queue) != 0

    def xǁDequeǁisEmpty__mutmut_2(self):
        return len(self.queue) == 1
    
    xǁDequeǁisEmpty__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDequeǁisEmpty__mutmut_1': xǁDequeǁisEmpty__mutmut_1, 
        'xǁDequeǁisEmpty__mutmut_2': xǁDequeǁisEmpty__mutmut_2
    }
    
    def isEmpty(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDequeǁisEmpty__mutmut_orig"), object.__getattribute__(self, "xǁDequeǁisEmpty__mutmut_mutants"), args, kwargs, self)
        return result 
    
    isEmpty.__signature__ = _mutmut_signature(xǁDequeǁisEmpty__mutmut_orig)
    xǁDequeǁisEmpty__mutmut_orig.__name__ = 'xǁDequeǁisEmpty'
