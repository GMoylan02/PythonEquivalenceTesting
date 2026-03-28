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
class Queue(object):


    def xǁQueueǁ__init____mutmut_orig(self, data=None):
        self.queue = []
        if data:
            for val in data:
                self.enqueue(val)


    def xǁQueueǁ__init____mutmut_1(self, data=None):
        self.queue = None
        if data:
            for val in data:
                self.enqueue(val)


    def xǁQueueǁ__init____mutmut_2(self, data=None):
        self.queue = []
        if data:
            for val in data:
                self.enqueue(None)
    
    xǁQueueǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁQueueǁ__init____mutmut_1': xǁQueueǁ__init____mutmut_1, 
        'xǁQueueǁ__init____mutmut_2': xǁQueueǁ__init____mutmut_2
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁQueueǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁQueueǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁQueueǁ__init____mutmut_orig)
    xǁQueueǁ__init____mutmut_orig.__name__ = 'xǁQueueǁ__init__'

    def xǁQueueǁenqueue__mutmut_orig(self, element):
        self.queue.append(element)

    def xǁQueueǁenqueue__mutmut_1(self, element):
        self.queue.append(None)
    
    xǁQueueǁenqueue__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁQueueǁenqueue__mutmut_1': xǁQueueǁenqueue__mutmut_1
    }
    
    def enqueue(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁQueueǁenqueue__mutmut_orig"), object.__getattribute__(self, "xǁQueueǁenqueue__mutmut_mutants"), args, kwargs, self)
        return result 
    
    enqueue.__signature__ = _mutmut_signature(xǁQueueǁenqueue__mutmut_orig)
    xǁQueueǁenqueue__mutmut_orig.__name__ = 'xǁQueueǁenqueue'

    def xǁQueueǁdequeue__mutmut_orig(self):
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self.queue.pop(0)

    def xǁQueueǁdequeue__mutmut_1(self):
        if self.isEmpty():
            raise IndexError(None)
        return self.queue.pop(0)

    def xǁQueueǁdequeue__mutmut_2(self):
        if self.isEmpty():
            raise IndexError("XXQueue is emptyXX")
        return self.queue.pop(0)

    def xǁQueueǁdequeue__mutmut_3(self):
        if self.isEmpty():
            raise IndexError("queue is empty")
        return self.queue.pop(0)

    def xǁQueueǁdequeue__mutmut_4(self):
        if self.isEmpty():
            raise IndexError("QUEUE IS EMPTY")
        return self.queue.pop(0)

    def xǁQueueǁdequeue__mutmut_5(self):
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self.queue.pop(None)

    def xǁQueueǁdequeue__mutmut_6(self):
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self.queue.pop(1)
    
    xǁQueueǁdequeue__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁQueueǁdequeue__mutmut_1': xǁQueueǁdequeue__mutmut_1, 
        'xǁQueueǁdequeue__mutmut_2': xǁQueueǁdequeue__mutmut_2, 
        'xǁQueueǁdequeue__mutmut_3': xǁQueueǁdequeue__mutmut_3, 
        'xǁQueueǁdequeue__mutmut_4': xǁQueueǁdequeue__mutmut_4, 
        'xǁQueueǁdequeue__mutmut_5': xǁQueueǁdequeue__mutmut_5, 
        'xǁQueueǁdequeue__mutmut_6': xǁQueueǁdequeue__mutmut_6
    }
    
    def dequeue(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁQueueǁdequeue__mutmut_orig"), object.__getattribute__(self, "xǁQueueǁdequeue__mutmut_mutants"), args, kwargs, self)
        return result 
    
    dequeue.__signature__ = _mutmut_signature(xǁQueueǁdequeue__mutmut_orig)
    xǁQueueǁdequeue__mutmut_orig.__name__ = 'xǁQueueǁdequeue'

    def xǁQueueǁpeek__mutmut_orig(self):
        if self.isEmpty():
            return None
        return self.queue[0]

    def xǁQueueǁpeek__mutmut_1(self):
        if self.isEmpty():
            return None
        return self.queue[1]
    
    xǁQueueǁpeek__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁQueueǁpeek__mutmut_1': xǁQueueǁpeek__mutmut_1
    }
    
    def peek(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁQueueǁpeek__mutmut_orig"), object.__getattribute__(self, "xǁQueueǁpeek__mutmut_mutants"), args, kwargs, self)
        return result 
    
    peek.__signature__ = _mutmut_signature(xǁQueueǁpeek__mutmut_orig)
    xǁQueueǁpeek__mutmut_orig.__name__ = 'xǁQueueǁpeek'

    def xǁQueueǁisEmpty__mutmut_orig(self):
        return len(self.queue) == 0

    def xǁQueueǁisEmpty__mutmut_1(self):
        return len(self.queue) != 0

    def xǁQueueǁisEmpty__mutmut_2(self):
        return len(self.queue) == 1
    
    xǁQueueǁisEmpty__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁQueueǁisEmpty__mutmut_1': xǁQueueǁisEmpty__mutmut_1, 
        'xǁQueueǁisEmpty__mutmut_2': xǁQueueǁisEmpty__mutmut_2
    }
    
    def isEmpty(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁQueueǁisEmpty__mutmut_orig"), object.__getattribute__(self, "xǁQueueǁisEmpty__mutmut_mutants"), args, kwargs, self)
        return result 
    
    isEmpty.__signature__ = _mutmut_signature(xǁQueueǁisEmpty__mutmut_orig)
    xǁQueueǁisEmpty__mutmut_orig.__name__ = 'xǁQueueǁisEmpty'

