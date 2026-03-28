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
class Stack:
    def xǁStackǁ__init____mutmut_orig(self):
        self._stack = []
    def xǁStackǁ__init____mutmut_1(self):
        self._stack = None
    
    xǁStackǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStackǁ__init____mutmut_1': xǁStackǁ__init____mutmut_1
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStackǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁStackǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁStackǁ__init____mutmut_orig)
    xǁStackǁ__init____mutmut_orig.__name__ = 'xǁStackǁ__init__'

    def xǁStackǁpush__mutmut_orig(self, value):
        self._stack.append(value)

    def xǁStackǁpush__mutmut_1(self, value):
        self._stack.append(None)
    
    xǁStackǁpush__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStackǁpush__mutmut_1': xǁStackǁpush__mutmut_1
    }
    
    def push(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStackǁpush__mutmut_orig"), object.__getattribute__(self, "xǁStackǁpush__mutmut_mutants"), args, kwargs, self)
        return result 
    
    push.__signature__ = _mutmut_signature(xǁStackǁpush__mutmut_orig)
    xǁStackǁpush__mutmut_orig.__name__ = 'xǁStackǁpush'

    def xǁStackǁpop__mutmut_orig(self):
        if not self._stack:
            raise IndexError("pop from empty stack")
        return self._stack.pop()

    def xǁStackǁpop__mutmut_1(self):
        if self._stack:
            raise IndexError("pop from empty stack")
        return self._stack.pop()

    def xǁStackǁpop__mutmut_2(self):
        if not self._stack:
            raise IndexError(None)
        return self._stack.pop()

    def xǁStackǁpop__mutmut_3(self):
        if not self._stack:
            raise IndexError("XXpop from empty stackXX")
        return self._stack.pop()

    def xǁStackǁpop__mutmut_4(self):
        if not self._stack:
            raise IndexError("POP FROM EMPTY STACK")
        return self._stack.pop()
    
    xǁStackǁpop__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStackǁpop__mutmut_1': xǁStackǁpop__mutmut_1, 
        'xǁStackǁpop__mutmut_2': xǁStackǁpop__mutmut_2, 
        'xǁStackǁpop__mutmut_3': xǁStackǁpop__mutmut_3, 
        'xǁStackǁpop__mutmut_4': xǁStackǁpop__mutmut_4
    }
    
    def pop(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStackǁpop__mutmut_orig"), object.__getattribute__(self, "xǁStackǁpop__mutmut_mutants"), args, kwargs, self)
        return result 
    
    pop.__signature__ = _mutmut_signature(xǁStackǁpop__mutmut_orig)
    xǁStackǁpop__mutmut_orig.__name__ = 'xǁStackǁpop'

    def xǁStackǁpeek__mutmut_orig(self):
        if not self._stack:
            raise IndexError("peek from empty stack")
        return self._stack[-1]

    def xǁStackǁpeek__mutmut_1(self):
        if self._stack:
            raise IndexError("peek from empty stack")
        return self._stack[-1]

    def xǁStackǁpeek__mutmut_2(self):
        if not self._stack:
            raise IndexError(None)
        return self._stack[-1]

    def xǁStackǁpeek__mutmut_3(self):
        if not self._stack:
            raise IndexError("XXpeek from empty stackXX")
        return self._stack[-1]

    def xǁStackǁpeek__mutmut_4(self):
        if not self._stack:
            raise IndexError("PEEK FROM EMPTY STACK")
        return self._stack[-1]

    def xǁStackǁpeek__mutmut_5(self):
        if not self._stack:
            raise IndexError("peek from empty stack")
        return self._stack[+1]

    def xǁStackǁpeek__mutmut_6(self):
        if not self._stack:
            raise IndexError("peek from empty stack")
        return self._stack[-2]
    
    xǁStackǁpeek__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStackǁpeek__mutmut_1': xǁStackǁpeek__mutmut_1, 
        'xǁStackǁpeek__mutmut_2': xǁStackǁpeek__mutmut_2, 
        'xǁStackǁpeek__mutmut_3': xǁStackǁpeek__mutmut_3, 
        'xǁStackǁpeek__mutmut_4': xǁStackǁpeek__mutmut_4, 
        'xǁStackǁpeek__mutmut_5': xǁStackǁpeek__mutmut_5, 
        'xǁStackǁpeek__mutmut_6': xǁStackǁpeek__mutmut_6
    }
    
    def peek(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStackǁpeek__mutmut_orig"), object.__getattribute__(self, "xǁStackǁpeek__mutmut_mutants"), args, kwargs, self)
        return result 
    
    peek.__signature__ = _mutmut_signature(xǁStackǁpeek__mutmut_orig)
    xǁStackǁpeek__mutmut_orig.__name__ = 'xǁStackǁpeek'

    def xǁStackǁisEmpty__mutmut_orig(self):
        return len(self._stack) == 0

    def xǁStackǁisEmpty__mutmut_1(self):
        return len(self._stack) != 0

    def xǁStackǁisEmpty__mutmut_2(self):
        return len(self._stack) == 1
    
    xǁStackǁisEmpty__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStackǁisEmpty__mutmut_1': xǁStackǁisEmpty__mutmut_1, 
        'xǁStackǁisEmpty__mutmut_2': xǁStackǁisEmpty__mutmut_2
    }
    
    def isEmpty(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStackǁisEmpty__mutmut_orig"), object.__getattribute__(self, "xǁStackǁisEmpty__mutmut_mutants"), args, kwargs, self)
        return result 
    
    isEmpty.__signature__ = _mutmut_signature(xǁStackǁisEmpty__mutmut_orig)
    xǁStackǁisEmpty__mutmut_orig.__name__ = 'xǁStackǁisEmpty'

    def size(self):
        return len(self._stack)