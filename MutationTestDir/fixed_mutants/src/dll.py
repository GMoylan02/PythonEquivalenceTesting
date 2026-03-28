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
class DLLNode(object):

    def xǁDLLNodeǁ__init____mutmut_orig(self, data=None, next_node=None, prev=None):
        self.data = data
        self.next = next_node
        self.prev = prev

    def xǁDLLNodeǁ__init____mutmut_1(self, data=None, next_node=None, prev=None):
        self.data = None
        self.next = next_node
        self.prev = prev

    def xǁDLLNodeǁ__init____mutmut_2(self, data=None, next_node=None, prev=None):
        self.data = data
        self.next = None
        self.prev = prev

    def xǁDLLNodeǁ__init____mutmut_3(self, data=None, next_node=None, prev=None):
        self.data = data
        self.next = next_node
        self.prev = None
    
    xǁDLLNodeǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDLLNodeǁ__init____mutmut_1': xǁDLLNodeǁ__init____mutmut_1, 
        'xǁDLLNodeǁ__init____mutmut_2': xǁDLLNodeǁ__init____mutmut_2, 
        'xǁDLLNodeǁ__init____mutmut_3': xǁDLLNodeǁ__init____mutmut_3
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDLLNodeǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁDLLNodeǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁDLLNodeǁ__init____mutmut_orig)
    xǁDLLNodeǁ__init____mutmut_orig.__name__ = 'xǁDLLNodeǁ__init__'

    def xǁDLLNodeǁ__repr____mutmut_orig(self):
        return "Value: {}".format(self.data)

    def xǁDLLNodeǁ__repr____mutmut_1(self):
        return "Value: {}".format(None)

    def xǁDLLNodeǁ__repr____mutmut_2(self):
        return "XXValue: {}XX".format(self.data)

    def xǁDLLNodeǁ__repr____mutmut_3(self):
        return "value: {}".format(self.data)

    def xǁDLLNodeǁ__repr____mutmut_4(self):
        return "VALUE: {}".format(self.data)
    
    xǁDLLNodeǁ__repr____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDLLNodeǁ__repr____mutmut_1': xǁDLLNodeǁ__repr____mutmut_1, 
        'xǁDLLNodeǁ__repr____mutmut_2': xǁDLLNodeǁ__repr____mutmut_2, 
        'xǁDLLNodeǁ__repr____mutmut_3': xǁDLLNodeǁ__repr____mutmut_3, 
        'xǁDLLNodeǁ__repr____mutmut_4': xǁDLLNodeǁ__repr____mutmut_4
    }
    
    def __repr__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDLLNodeǁ__repr____mutmut_orig"), object.__getattribute__(self, "xǁDLLNodeǁ__repr____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __repr__.__signature__ = _mutmut_signature(xǁDLLNodeǁ__repr____mutmut_orig)
    xǁDLLNodeǁ__repr____mutmut_orig.__name__ = 'xǁDLLNodeǁ__repr__'


class DoubleLinkedList(object):

    def xǁDoubleLinkedListǁ__init____mutmut_orig(self, data=None):
        self.head = None
        self.tail = None
        self._length = 0
        try:
            for val in data:
                self.push(val)
        except TypeError:
            if data:
                self.push(data)

    def xǁDoubleLinkedListǁ__init____mutmut_1(self, data=None):
        self.head = ""
        self.tail = None
        self._length = 0
        try:
            for val in data:
                self.push(val)
        except TypeError:
            if data:
                self.push(data)

    def xǁDoubleLinkedListǁ__init____mutmut_2(self, data=None):
        self.head = None
        self.tail = ""
        self._length = 0
        try:
            for val in data:
                self.push(val)
        except TypeError:
            if data:
                self.push(data)

    def xǁDoubleLinkedListǁ__init____mutmut_3(self, data=None):
        self.head = None
        self.tail = None
        self._length = None
        try:
            for val in data:
                self.push(val)
        except TypeError:
            if data:
                self.push(data)

    def xǁDoubleLinkedListǁ__init____mutmut_4(self, data=None):
        self.head = None
        self.tail = None
        self._length = 1
        try:
            for val in data:
                self.push(val)
        except TypeError:
            if data:
                self.push(data)

    def xǁDoubleLinkedListǁ__init____mutmut_5(self, data=None):
        self.head = None
        self.tail = None
        self._length = 0
        try:
            for val in data:
                self.push(None)
        except TypeError:
            if data:
                self.push(data)

    def xǁDoubleLinkedListǁ__init____mutmut_6(self, data=None):
        self.head = None
        self.tail = None
        self._length = 0
        try:
            for val in data:
                self.push(val)
        except TypeError:
            if data:
                self.push(None)
    
    xǁDoubleLinkedListǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDoubleLinkedListǁ__init____mutmut_1': xǁDoubleLinkedListǁ__init____mutmut_1, 
        'xǁDoubleLinkedListǁ__init____mutmut_2': xǁDoubleLinkedListǁ__init____mutmut_2, 
        'xǁDoubleLinkedListǁ__init____mutmut_3': xǁDoubleLinkedListǁ__init____mutmut_3, 
        'xǁDoubleLinkedListǁ__init____mutmut_4': xǁDoubleLinkedListǁ__init____mutmut_4, 
        'xǁDoubleLinkedListǁ__init____mutmut_5': xǁDoubleLinkedListǁ__init____mutmut_5, 
        'xǁDoubleLinkedListǁ__init____mutmut_6': xǁDoubleLinkedListǁ__init____mutmut_6
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDoubleLinkedListǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁDoubleLinkedListǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁDoubleLinkedListǁ__init____mutmut_orig)
    xǁDoubleLinkedListǁ__init____mutmut_orig.__name__ = 'xǁDoubleLinkedListǁ__init__'

    def xǁDoubleLinkedListǁpush__mutmut_orig(self, val):
        old_head = self.head
        self.head = DLLNode(val, next_node=old_head)
        if old_head:
            old_head.prev = self.head
        if not self.tail:
            self.tail = self.head
        self._length += 1

    def xǁDoubleLinkedListǁpush__mutmut_1(self, val):
        old_head = None
        self.head = DLLNode(val, next_node=old_head)
        if old_head:
            old_head.prev = self.head
        if not self.tail:
            self.tail = self.head
        self._length += 1

    def xǁDoubleLinkedListǁpush__mutmut_2(self, val):
        old_head = self.head
        self.head = None
        if old_head:
            old_head.prev = self.head
        if not self.tail:
            self.tail = self.head
        self._length += 1

    def xǁDoubleLinkedListǁpush__mutmut_3(self, val):
        old_head = self.head
        self.head = DLLNode(None, next_node=old_head)
        if old_head:
            old_head.prev = self.head
        if not self.tail:
            self.tail = self.head
        self._length += 1

    def xǁDoubleLinkedListǁpush__mutmut_4(self, val):
        old_head = self.head
        self.head = DLLNode(val, next_node=None)
        if old_head:
            old_head.prev = self.head
        if not self.tail:
            self.tail = self.head
        self._length += 1

    def xǁDoubleLinkedListǁpush__mutmut_5(self, val):
        old_head = self.head
        self.head = DLLNode(next_node=old_head)
        if old_head:
            old_head.prev = self.head
        if not self.tail:
            self.tail = self.head
        self._length += 1

    def xǁDoubleLinkedListǁpush__mutmut_6(self, val):
        old_head = self.head
        self.head = DLLNode(val, )
        if old_head:
            old_head.prev = self.head
        if not self.tail:
            self.tail = self.head
        self._length += 1

    def xǁDoubleLinkedListǁpush__mutmut_7(self, val):
        old_head = self.head
        self.head = DLLNode(val, next_node=old_head)
        if old_head:
            old_head.prev = None
        if not self.tail:
            self.tail = self.head
        self._length += 1

    def xǁDoubleLinkedListǁpush__mutmut_8(self, val):
        old_head = self.head
        self.head = DLLNode(val, next_node=old_head)
        if old_head:
            old_head.prev = self.head
        if self.tail:
            self.tail = self.head
        self._length += 1

    def xǁDoubleLinkedListǁpush__mutmut_9(self, val):
        old_head = self.head
        self.head = DLLNode(val, next_node=old_head)
        if old_head:
            old_head.prev = self.head
        if not self.tail:
            self.tail = None
        self._length += 1

    def xǁDoubleLinkedListǁpush__mutmut_10(self, val):
        old_head = self.head
        self.head = DLLNode(val, next_node=old_head)
        if old_head:
            old_head.prev = self.head
        if not self.tail:
            self.tail = self.head
        self._length = 1

    def xǁDoubleLinkedListǁpush__mutmut_11(self, val):
        old_head = self.head
        self.head = DLLNode(val, next_node=old_head)
        if old_head:
            old_head.prev = self.head
        if not self.tail:
            self.tail = self.head
        self._length -= 1

    def xǁDoubleLinkedListǁpush__mutmut_12(self, val):
        old_head = self.head
        self.head = DLLNode(val, next_node=old_head)
        if old_head:
            old_head.prev = self.head
        if not self.tail:
            self.tail = self.head
        self._length += 2
    
    xǁDoubleLinkedListǁpush__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDoubleLinkedListǁpush__mutmut_1': xǁDoubleLinkedListǁpush__mutmut_1, 
        'xǁDoubleLinkedListǁpush__mutmut_2': xǁDoubleLinkedListǁpush__mutmut_2, 
        'xǁDoubleLinkedListǁpush__mutmut_3': xǁDoubleLinkedListǁpush__mutmut_3, 
        'xǁDoubleLinkedListǁpush__mutmut_4': xǁDoubleLinkedListǁpush__mutmut_4, 
        'xǁDoubleLinkedListǁpush__mutmut_5': xǁDoubleLinkedListǁpush__mutmut_5, 
        'xǁDoubleLinkedListǁpush__mutmut_6': xǁDoubleLinkedListǁpush__mutmut_6, 
        'xǁDoubleLinkedListǁpush__mutmut_7': xǁDoubleLinkedListǁpush__mutmut_7, 
        'xǁDoubleLinkedListǁpush__mutmut_8': xǁDoubleLinkedListǁpush__mutmut_8, 
        'xǁDoubleLinkedListǁpush__mutmut_9': xǁDoubleLinkedListǁpush__mutmut_9, 
        'xǁDoubleLinkedListǁpush__mutmut_10': xǁDoubleLinkedListǁpush__mutmut_10, 
        'xǁDoubleLinkedListǁpush__mutmut_11': xǁDoubleLinkedListǁpush__mutmut_11, 
        'xǁDoubleLinkedListǁpush__mutmut_12': xǁDoubleLinkedListǁpush__mutmut_12
    }
    
    def push(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDoubleLinkedListǁpush__mutmut_orig"), object.__getattribute__(self, "xǁDoubleLinkedListǁpush__mutmut_mutants"), args, kwargs, self)
        return result 
    
    push.__signature__ = _mutmut_signature(xǁDoubleLinkedListǁpush__mutmut_orig)
    xǁDoubleLinkedListǁpush__mutmut_orig.__name__ = 'xǁDoubleLinkedListǁpush'

    def xǁDoubleLinkedListǁpop__mutmut_orig(self):
        if self._length < 1:
            raise IndexError('Cannot pop from an empty list.')
        to_return = self.head
        new_head = self.head.next
        if new_head:
            new_head.prev = None
        self.head = new_head
        self._length -= 1
        if self._length < 1:
            self.tail = None
        return to_return.data

    def xǁDoubleLinkedListǁpop__mutmut_1(self):
        if self._length <= 1:
            raise IndexError('Cannot pop from an empty list.')
        to_return = self.head
        new_head = self.head.next
        if new_head:
            new_head.prev = None
        self.head = new_head
        self._length -= 1
        if self._length < 1:
            self.tail = None
        return to_return.data

    def xǁDoubleLinkedListǁpop__mutmut_2(self):
        if self._length < 2:
            raise IndexError('Cannot pop from an empty list.')
        to_return = self.head
        new_head = self.head.next
        if new_head:
            new_head.prev = None
        self.head = new_head
        self._length -= 1
        if self._length < 1:
            self.tail = None
        return to_return.data

    def xǁDoubleLinkedListǁpop__mutmut_3(self):
        if self._length < 1:
            raise IndexError(None)
        to_return = self.head
        new_head = self.head.next
        if new_head:
            new_head.prev = None
        self.head = new_head
        self._length -= 1
        if self._length < 1:
            self.tail = None
        return to_return.data

    def xǁDoubleLinkedListǁpop__mutmut_4(self):
        if self._length < 1:
            raise IndexError('XXCannot pop from an empty list.XX')
        to_return = self.head
        new_head = self.head.next
        if new_head:
            new_head.prev = None
        self.head = new_head
        self._length -= 1
        if self._length < 1:
            self.tail = None
        return to_return.data

    def xǁDoubleLinkedListǁpop__mutmut_5(self):
        if self._length < 1:
            raise IndexError('cannot pop from an empty list.')
        to_return = self.head
        new_head = self.head.next
        if new_head:
            new_head.prev = None
        self.head = new_head
        self._length -= 1
        if self._length < 1:
            self.tail = None
        return to_return.data

    def xǁDoubleLinkedListǁpop__mutmut_6(self):
        if self._length < 1:
            raise IndexError('CANNOT POP FROM AN EMPTY LIST.')
        to_return = self.head
        new_head = self.head.next
        if new_head:
            new_head.prev = None
        self.head = new_head
        self._length -= 1
        if self._length < 1:
            self.tail = None
        return to_return.data

    def xǁDoubleLinkedListǁpop__mutmut_7(self):
        if self._length < 1:
            raise IndexError('Cannot pop from an empty list.')
        to_return = None
        new_head = self.head.next
        if new_head:
            new_head.prev = None
        self.head = new_head
        self._length -= 1
        if self._length < 1:
            self.tail = None
        return to_return.data

    def xǁDoubleLinkedListǁpop__mutmut_8(self):
        if self._length < 1:
            raise IndexError('Cannot pop from an empty list.')
        to_return = self.head
        new_head = None
        if new_head:
            new_head.prev = None
        self.head = new_head
        self._length -= 1
        if self._length < 1:
            self.tail = None
        return to_return.data

    def xǁDoubleLinkedListǁpop__mutmut_9(self):
        if self._length < 1:
            raise IndexError('Cannot pop from an empty list.')
        to_return = self.head
        new_head = self.head.next
        if new_head:
            new_head.prev = ""
        self.head = new_head
        self._length -= 1
        if self._length < 1:
            self.tail = None
        return to_return.data

    def xǁDoubleLinkedListǁpop__mutmut_10(self):
        if self._length < 1:
            raise IndexError('Cannot pop from an empty list.')
        to_return = self.head
        new_head = self.head.next
        if new_head:
            new_head.prev = None
        self.head = None
        self._length -= 1
        if self._length < 1:
            self.tail = None
        return to_return.data

    def xǁDoubleLinkedListǁpop__mutmut_11(self):
        if self._length < 1:
            raise IndexError('Cannot pop from an empty list.')
        to_return = self.head
        new_head = self.head.next
        if new_head:
            new_head.prev = None
        self.head = new_head
        self._length = 1
        if self._length < 1:
            self.tail = None
        return to_return.data

    def xǁDoubleLinkedListǁpop__mutmut_12(self):
        if self._length < 1:
            raise IndexError('Cannot pop from an empty list.')
        to_return = self.head
        new_head = self.head.next
        if new_head:
            new_head.prev = None
        self.head = new_head
        self._length += 1
        if self._length < 1:
            self.tail = None
        return to_return.data

    def xǁDoubleLinkedListǁpop__mutmut_13(self):
        if self._length < 1:
            raise IndexError('Cannot pop from an empty list.')
        to_return = self.head
        new_head = self.head.next
        if new_head:
            new_head.prev = None
        self.head = new_head
        self._length -= 2
        if self._length < 1:
            self.tail = None
        return to_return.data

    def xǁDoubleLinkedListǁpop__mutmut_14(self):
        if self._length < 1:
            raise IndexError('Cannot pop from an empty list.')
        to_return = self.head
        new_head = self.head.next
        if new_head:
            new_head.prev = None
        self.head = new_head
        self._length -= 1
        if self._length <= 1:
            self.tail = None
        return to_return.data

    def xǁDoubleLinkedListǁpop__mutmut_15(self):
        if self._length < 1:
            raise IndexError('Cannot pop from an empty list.')
        to_return = self.head
        new_head = self.head.next
        if new_head:
            new_head.prev = None
        self.head = new_head
        self._length -= 1
        if self._length < 2:
            self.tail = None
        return to_return.data

    def xǁDoubleLinkedListǁpop__mutmut_16(self):
        if self._length < 1:
            raise IndexError('Cannot pop from an empty list.')
        to_return = self.head
        new_head = self.head.next
        if new_head:
            new_head.prev = None
        self.head = new_head
        self._length -= 1
        if self._length < 1:
            self.tail = ""
        return to_return.data
    
    xǁDoubleLinkedListǁpop__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDoubleLinkedListǁpop__mutmut_1': xǁDoubleLinkedListǁpop__mutmut_1, 
        'xǁDoubleLinkedListǁpop__mutmut_2': xǁDoubleLinkedListǁpop__mutmut_2, 
        'xǁDoubleLinkedListǁpop__mutmut_3': xǁDoubleLinkedListǁpop__mutmut_3, 
        'xǁDoubleLinkedListǁpop__mutmut_4': xǁDoubleLinkedListǁpop__mutmut_4, 
        'xǁDoubleLinkedListǁpop__mutmut_5': xǁDoubleLinkedListǁpop__mutmut_5, 
        'xǁDoubleLinkedListǁpop__mutmut_6': xǁDoubleLinkedListǁpop__mutmut_6, 
        'xǁDoubleLinkedListǁpop__mutmut_7': xǁDoubleLinkedListǁpop__mutmut_7, 
        'xǁDoubleLinkedListǁpop__mutmut_8': xǁDoubleLinkedListǁpop__mutmut_8, 
        'xǁDoubleLinkedListǁpop__mutmut_9': xǁDoubleLinkedListǁpop__mutmut_9, 
        'xǁDoubleLinkedListǁpop__mutmut_10': xǁDoubleLinkedListǁpop__mutmut_10, 
        'xǁDoubleLinkedListǁpop__mutmut_11': xǁDoubleLinkedListǁpop__mutmut_11, 
        'xǁDoubleLinkedListǁpop__mutmut_12': xǁDoubleLinkedListǁpop__mutmut_12, 
        'xǁDoubleLinkedListǁpop__mutmut_13': xǁDoubleLinkedListǁpop__mutmut_13, 
        'xǁDoubleLinkedListǁpop__mutmut_14': xǁDoubleLinkedListǁpop__mutmut_14, 
        'xǁDoubleLinkedListǁpop__mutmut_15': xǁDoubleLinkedListǁpop__mutmut_15, 
        'xǁDoubleLinkedListǁpop__mutmut_16': xǁDoubleLinkedListǁpop__mutmut_16
    }
    
    def pop(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDoubleLinkedListǁpop__mutmut_orig"), object.__getattribute__(self, "xǁDoubleLinkedListǁpop__mutmut_mutants"), args, kwargs, self)
        return result 
    
    pop.__signature__ = _mutmut_signature(xǁDoubleLinkedListǁpop__mutmut_orig)
    xǁDoubleLinkedListǁpop__mutmut_orig.__name__ = 'xǁDoubleLinkedListǁpop'

    def xǁDoubleLinkedListǁappend__mutmut_orig(self, val):
        old_tail = self.tail
        self.tail = DLLNode(val, prev=old_tail)
        if old_tail:
            old_tail.next = self.tail
        if self._length < 1:
            self.head = self.tail
        self._length += 1

    def xǁDoubleLinkedListǁappend__mutmut_1(self, val):
        old_tail = None
        self.tail = DLLNode(val, prev=old_tail)
        if old_tail:
            old_tail.next = self.tail
        if self._length < 1:
            self.head = self.tail
        self._length += 1

    def xǁDoubleLinkedListǁappend__mutmut_2(self, val):
        old_tail = self.tail
        self.tail = None
        if old_tail:
            old_tail.next = self.tail
        if self._length < 1:
            self.head = self.tail
        self._length += 1

    def xǁDoubleLinkedListǁappend__mutmut_3(self, val):
        old_tail = self.tail
        self.tail = DLLNode(None, prev=old_tail)
        if old_tail:
            old_tail.next = self.tail
        if self._length < 1:
            self.head = self.tail
        self._length += 1

    def xǁDoubleLinkedListǁappend__mutmut_4(self, val):
        old_tail = self.tail
        self.tail = DLLNode(val, prev=None)
        if old_tail:
            old_tail.next = self.tail
        if self._length < 1:
            self.head = self.tail
        self._length += 1

    def xǁDoubleLinkedListǁappend__mutmut_5(self, val):
        old_tail = self.tail
        self.tail = DLLNode(prev=old_tail)
        if old_tail:
            old_tail.next = self.tail
        if self._length < 1:
            self.head = self.tail
        self._length += 1

    def xǁDoubleLinkedListǁappend__mutmut_6(self, val):
        old_tail = self.tail
        self.tail = DLLNode(val, )
        if old_tail:
            old_tail.next = self.tail
        if self._length < 1:
            self.head = self.tail
        self._length += 1

    def xǁDoubleLinkedListǁappend__mutmut_7(self, val):
        old_tail = self.tail
        self.tail = DLLNode(val, prev=old_tail)
        if old_tail:
            old_tail.next = None
        if self._length < 1:
            self.head = self.tail
        self._length += 1

    def xǁDoubleLinkedListǁappend__mutmut_8(self, val):
        old_tail = self.tail
        self.tail = DLLNode(val, prev=old_tail)
        if old_tail:
            old_tail.next = self.tail
        if self._length <= 1:
            self.head = self.tail
        self._length += 1

    def xǁDoubleLinkedListǁappend__mutmut_9(self, val):
        old_tail = self.tail
        self.tail = DLLNode(val, prev=old_tail)
        if old_tail:
            old_tail.next = self.tail
        if self._length < 2:
            self.head = self.tail
        self._length += 1

    def xǁDoubleLinkedListǁappend__mutmut_10(self, val):
        old_tail = self.tail
        self.tail = DLLNode(val, prev=old_tail)
        if old_tail:
            old_tail.next = self.tail
        if self._length < 1:
            self.head = None
        self._length += 1

    def xǁDoubleLinkedListǁappend__mutmut_11(self, val):
        old_tail = self.tail
        self.tail = DLLNode(val, prev=old_tail)
        if old_tail:
            old_tail.next = self.tail
        if self._length < 1:
            self.head = self.tail
        self._length = 1

    def xǁDoubleLinkedListǁappend__mutmut_12(self, val):
        old_tail = self.tail
        self.tail = DLLNode(val, prev=old_tail)
        if old_tail:
            old_tail.next = self.tail
        if self._length < 1:
            self.head = self.tail
        self._length -= 1

    def xǁDoubleLinkedListǁappend__mutmut_13(self, val):
        old_tail = self.tail
        self.tail = DLLNode(val, prev=old_tail)
        if old_tail:
            old_tail.next = self.tail
        if self._length < 1:
            self.head = self.tail
        self._length += 2
    
    xǁDoubleLinkedListǁappend__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDoubleLinkedListǁappend__mutmut_1': xǁDoubleLinkedListǁappend__mutmut_1, 
        'xǁDoubleLinkedListǁappend__mutmut_2': xǁDoubleLinkedListǁappend__mutmut_2, 
        'xǁDoubleLinkedListǁappend__mutmut_3': xǁDoubleLinkedListǁappend__mutmut_3, 
        'xǁDoubleLinkedListǁappend__mutmut_4': xǁDoubleLinkedListǁappend__mutmut_4, 
        'xǁDoubleLinkedListǁappend__mutmut_5': xǁDoubleLinkedListǁappend__mutmut_5, 
        'xǁDoubleLinkedListǁappend__mutmut_6': xǁDoubleLinkedListǁappend__mutmut_6, 
        'xǁDoubleLinkedListǁappend__mutmut_7': xǁDoubleLinkedListǁappend__mutmut_7, 
        'xǁDoubleLinkedListǁappend__mutmut_8': xǁDoubleLinkedListǁappend__mutmut_8, 
        'xǁDoubleLinkedListǁappend__mutmut_9': xǁDoubleLinkedListǁappend__mutmut_9, 
        'xǁDoubleLinkedListǁappend__mutmut_10': xǁDoubleLinkedListǁappend__mutmut_10, 
        'xǁDoubleLinkedListǁappend__mutmut_11': xǁDoubleLinkedListǁappend__mutmut_11, 
        'xǁDoubleLinkedListǁappend__mutmut_12': xǁDoubleLinkedListǁappend__mutmut_12, 
        'xǁDoubleLinkedListǁappend__mutmut_13': xǁDoubleLinkedListǁappend__mutmut_13
    }
    
    def append(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDoubleLinkedListǁappend__mutmut_orig"), object.__getattribute__(self, "xǁDoubleLinkedListǁappend__mutmut_mutants"), args, kwargs, self)
        return result 
    
    append.__signature__ = _mutmut_signature(xǁDoubleLinkedListǁappend__mutmut_orig)
    xǁDoubleLinkedListǁappend__mutmut_orig.__name__ = 'xǁDoubleLinkedListǁappend'

    def xǁDoubleLinkedListǁshift__mutmut_orig(self):
        if self._length < 1:
            raise IndexError('Cannot shift from an empty list.')
        to_return = self.tail
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = None
        self.tail = new_tail
        self._length -= 1
        if self._length < 1:
            self.head = None

        return to_return.data

    def xǁDoubleLinkedListǁshift__mutmut_1(self):
        if self._length <= 1:
            raise IndexError('Cannot shift from an empty list.')
        to_return = self.tail
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = None
        self.tail = new_tail
        self._length -= 1
        if self._length < 1:
            self.head = None

        return to_return.data

    def xǁDoubleLinkedListǁshift__mutmut_2(self):
        if self._length < 2:
            raise IndexError('Cannot shift from an empty list.')
        to_return = self.tail
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = None
        self.tail = new_tail
        self._length -= 1
        if self._length < 1:
            self.head = None

        return to_return.data

    def xǁDoubleLinkedListǁshift__mutmut_3(self):
        if self._length < 1:
            raise IndexError(None)
        to_return = self.tail
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = None
        self.tail = new_tail
        self._length -= 1
        if self._length < 1:
            self.head = None

        return to_return.data

    def xǁDoubleLinkedListǁshift__mutmut_4(self):
        if self._length < 1:
            raise IndexError('XXCannot shift from an empty list.XX')
        to_return = self.tail
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = None
        self.tail = new_tail
        self._length -= 1
        if self._length < 1:
            self.head = None

        return to_return.data

    def xǁDoubleLinkedListǁshift__mutmut_5(self):
        if self._length < 1:
            raise IndexError('cannot shift from an empty list.')
        to_return = self.tail
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = None
        self.tail = new_tail
        self._length -= 1
        if self._length < 1:
            self.head = None

        return to_return.data

    def xǁDoubleLinkedListǁshift__mutmut_6(self):
        if self._length < 1:
            raise IndexError('CANNOT SHIFT FROM AN EMPTY LIST.')
        to_return = self.tail
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = None
        self.tail = new_tail
        self._length -= 1
        if self._length < 1:
            self.head = None

        return to_return.data

    def xǁDoubleLinkedListǁshift__mutmut_7(self):
        if self._length < 1:
            raise IndexError('Cannot shift from an empty list.')
        to_return = None
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = None
        self.tail = new_tail
        self._length -= 1
        if self._length < 1:
            self.head = None

        return to_return.data

    def xǁDoubleLinkedListǁshift__mutmut_8(self):
        if self._length < 1:
            raise IndexError('Cannot shift from an empty list.')
        to_return = self.tail
        new_tail = None
        if new_tail:
            new_tail.next = None
        self.tail = new_tail
        self._length -= 1
        if self._length < 1:
            self.head = None

        return to_return.data

    def xǁDoubleLinkedListǁshift__mutmut_9(self):
        if self._length < 1:
            raise IndexError('Cannot shift from an empty list.')
        to_return = self.tail
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = ""
        self.tail = new_tail
        self._length -= 1
        if self._length < 1:
            self.head = None

        return to_return.data

    def xǁDoubleLinkedListǁshift__mutmut_10(self):
        if self._length < 1:
            raise IndexError('Cannot shift from an empty list.')
        to_return = self.tail
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = None
        self.tail = None
        self._length -= 1
        if self._length < 1:
            self.head = None

        return to_return.data

    def xǁDoubleLinkedListǁshift__mutmut_11(self):
        if self._length < 1:
            raise IndexError('Cannot shift from an empty list.')
        to_return = self.tail
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = None
        self.tail = new_tail
        self._length = 1
        if self._length < 1:
            self.head = None

        return to_return.data

    def xǁDoubleLinkedListǁshift__mutmut_12(self):
        if self._length < 1:
            raise IndexError('Cannot shift from an empty list.')
        to_return = self.tail
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = None
        self.tail = new_tail
        self._length += 1
        if self._length < 1:
            self.head = None

        return to_return.data

    def xǁDoubleLinkedListǁshift__mutmut_13(self):
        if self._length < 1:
            raise IndexError('Cannot shift from an empty list.')
        to_return = self.tail
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = None
        self.tail = new_tail
        self._length -= 2
        if self._length < 1:
            self.head = None

        return to_return.data

    def xǁDoubleLinkedListǁshift__mutmut_14(self):
        if self._length < 1:
            raise IndexError('Cannot shift from an empty list.')
        to_return = self.tail
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = None
        self.tail = new_tail
        self._length -= 1
        if self._length <= 1:
            self.head = None

        return to_return.data

    def xǁDoubleLinkedListǁshift__mutmut_15(self):
        if self._length < 1:
            raise IndexError('Cannot shift from an empty list.')
        to_return = self.tail
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = None
        self.tail = new_tail
        self._length -= 1
        if self._length < 2:
            self.head = None

        return to_return.data

    def xǁDoubleLinkedListǁshift__mutmut_16(self):
        if self._length < 1:
            raise IndexError('Cannot shift from an empty list.')
        to_return = self.tail
        new_tail = self.tail.prev
        if new_tail:
            new_tail.next = None
        self.tail = new_tail
        self._length -= 1
        if self._length < 1:
            self.head = ""

        return to_return.data
    
    xǁDoubleLinkedListǁshift__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDoubleLinkedListǁshift__mutmut_1': xǁDoubleLinkedListǁshift__mutmut_1, 
        'xǁDoubleLinkedListǁshift__mutmut_2': xǁDoubleLinkedListǁshift__mutmut_2, 
        'xǁDoubleLinkedListǁshift__mutmut_3': xǁDoubleLinkedListǁshift__mutmut_3, 
        'xǁDoubleLinkedListǁshift__mutmut_4': xǁDoubleLinkedListǁshift__mutmut_4, 
        'xǁDoubleLinkedListǁshift__mutmut_5': xǁDoubleLinkedListǁshift__mutmut_5, 
        'xǁDoubleLinkedListǁshift__mutmut_6': xǁDoubleLinkedListǁshift__mutmut_6, 
        'xǁDoubleLinkedListǁshift__mutmut_7': xǁDoubleLinkedListǁshift__mutmut_7, 
        'xǁDoubleLinkedListǁshift__mutmut_8': xǁDoubleLinkedListǁshift__mutmut_8, 
        'xǁDoubleLinkedListǁshift__mutmut_9': xǁDoubleLinkedListǁshift__mutmut_9, 
        'xǁDoubleLinkedListǁshift__mutmut_10': xǁDoubleLinkedListǁshift__mutmut_10, 
        'xǁDoubleLinkedListǁshift__mutmut_11': xǁDoubleLinkedListǁshift__mutmut_11, 
        'xǁDoubleLinkedListǁshift__mutmut_12': xǁDoubleLinkedListǁshift__mutmut_12, 
        'xǁDoubleLinkedListǁshift__mutmut_13': xǁDoubleLinkedListǁshift__mutmut_13, 
        'xǁDoubleLinkedListǁshift__mutmut_14': xǁDoubleLinkedListǁshift__mutmut_14, 
        'xǁDoubleLinkedListǁshift__mutmut_15': xǁDoubleLinkedListǁshift__mutmut_15, 
        'xǁDoubleLinkedListǁshift__mutmut_16': xǁDoubleLinkedListǁshift__mutmut_16
    }
    
    def shift(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDoubleLinkedListǁshift__mutmut_orig"), object.__getattribute__(self, "xǁDoubleLinkedListǁshift__mutmut_mutants"), args, kwargs, self)
        return result 
    
    shift.__signature__ = _mutmut_signature(xǁDoubleLinkedListǁshift__mutmut_orig)
    xǁDoubleLinkedListǁshift__mutmut_orig.__name__ = 'xǁDoubleLinkedListǁshift'

    def xǁDoubleLinkedListǁremove__mutmut_orig(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_1(self, val):
        curr = None
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_2(self, val):
        curr = self.head
        while curr:
            if curr.data != val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_3(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length != 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_4(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 2:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_5(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_6(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head or curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_7(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_8(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_9(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = None
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_10(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is not self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_11(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_12(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is not self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_13(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_14(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length = 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_15(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length += 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_16(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 2
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_17(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = None
        raise ValueError('{} is not in the list'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_18(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError(None)

    def xǁDoubleLinkedListǁremove__mutmut_19(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} is not in the list'.format(None))

    def xǁDoubleLinkedListǁremove__mutmut_20(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('XX{} is not in the listXX'.format(val))

    def xǁDoubleLinkedListǁremove__mutmut_21(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                if self._length == 1:
                    self.head, self.tail = None, None
                elif curr is not self.head and curr is not self.tail:
                    curr.next.prev, curr.prev.next = curr.prev, curr.next
                elif curr is self.head:
                    self.head, curr.next.prev = curr.next, None
                elif curr is self.tail:
                    self.tail, curr.prev.next = curr.prev, None
                self._length -= 1
                return
            curr = curr.next
        raise ValueError('{} IS NOT IN THE LIST'.format(val))
    
    xǁDoubleLinkedListǁremove__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDoubleLinkedListǁremove__mutmut_1': xǁDoubleLinkedListǁremove__mutmut_1, 
        'xǁDoubleLinkedListǁremove__mutmut_2': xǁDoubleLinkedListǁremove__mutmut_2, 
        'xǁDoubleLinkedListǁremove__mutmut_3': xǁDoubleLinkedListǁremove__mutmut_3, 
        'xǁDoubleLinkedListǁremove__mutmut_4': xǁDoubleLinkedListǁremove__mutmut_4, 
        'xǁDoubleLinkedListǁremove__mutmut_5': xǁDoubleLinkedListǁremove__mutmut_5, 
        'xǁDoubleLinkedListǁremove__mutmut_6': xǁDoubleLinkedListǁremove__mutmut_6, 
        'xǁDoubleLinkedListǁremove__mutmut_7': xǁDoubleLinkedListǁremove__mutmut_7, 
        'xǁDoubleLinkedListǁremove__mutmut_8': xǁDoubleLinkedListǁremove__mutmut_8, 
        'xǁDoubleLinkedListǁremove__mutmut_9': xǁDoubleLinkedListǁremove__mutmut_9, 
        'xǁDoubleLinkedListǁremove__mutmut_10': xǁDoubleLinkedListǁremove__mutmut_10, 
        'xǁDoubleLinkedListǁremove__mutmut_11': xǁDoubleLinkedListǁremove__mutmut_11, 
        'xǁDoubleLinkedListǁremove__mutmut_12': xǁDoubleLinkedListǁremove__mutmut_12, 
        'xǁDoubleLinkedListǁremove__mutmut_13': xǁDoubleLinkedListǁremove__mutmut_13, 
        'xǁDoubleLinkedListǁremove__mutmut_14': xǁDoubleLinkedListǁremove__mutmut_14, 
        'xǁDoubleLinkedListǁremove__mutmut_15': xǁDoubleLinkedListǁremove__mutmut_15, 
        'xǁDoubleLinkedListǁremove__mutmut_16': xǁDoubleLinkedListǁremove__mutmut_16, 
        'xǁDoubleLinkedListǁremove__mutmut_17': xǁDoubleLinkedListǁremove__mutmut_17, 
        'xǁDoubleLinkedListǁremove__mutmut_18': xǁDoubleLinkedListǁremove__mutmut_18, 
        'xǁDoubleLinkedListǁremove__mutmut_19': xǁDoubleLinkedListǁremove__mutmut_19, 
        'xǁDoubleLinkedListǁremove__mutmut_20': xǁDoubleLinkedListǁremove__mutmut_20, 
        'xǁDoubleLinkedListǁremove__mutmut_21': xǁDoubleLinkedListǁremove__mutmut_21
    }
    
    def remove(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDoubleLinkedListǁremove__mutmut_orig"), object.__getattribute__(self, "xǁDoubleLinkedListǁremove__mutmut_mutants"), args, kwargs, self)
        return result 
    
    remove.__signature__ = _mutmut_signature(xǁDoubleLinkedListǁremove__mutmut_orig)
    xǁDoubleLinkedListǁremove__mutmut_orig.__name__ = 'xǁDoubleLinkedListǁremove'

    def xǁDoubleLinkedListǁas_list__mutmut_orig(self):
        result = []
        curr = self.head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

    def xǁDoubleLinkedListǁas_list__mutmut_1(self):
        result = None
        curr = self.head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

    def xǁDoubleLinkedListǁas_list__mutmut_2(self):
        result = []
        curr = None
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

    def xǁDoubleLinkedListǁas_list__mutmut_3(self):
        result = []
        curr = self.head
        while curr:
            result.append(None)
            curr = curr.next
        return result

    def xǁDoubleLinkedListǁas_list__mutmut_4(self):
        result = []
        curr = self.head
        while curr:
            result.append(curr.data)
            curr = None
        return result
    
    xǁDoubleLinkedListǁas_list__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁDoubleLinkedListǁas_list__mutmut_1': xǁDoubleLinkedListǁas_list__mutmut_1, 
        'xǁDoubleLinkedListǁas_list__mutmut_2': xǁDoubleLinkedListǁas_list__mutmut_2, 
        'xǁDoubleLinkedListǁas_list__mutmut_3': xǁDoubleLinkedListǁas_list__mutmut_3, 
        'xǁDoubleLinkedListǁas_list__mutmut_4': xǁDoubleLinkedListǁas_list__mutmut_4
    }
    
    def as_list(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁDoubleLinkedListǁas_list__mutmut_orig"), object.__getattribute__(self, "xǁDoubleLinkedListǁas_list__mutmut_mutants"), args, kwargs, self)
        return result 
    
    as_list.__signature__ = _mutmut_signature(xǁDoubleLinkedListǁas_list__mutmut_orig)
    xǁDoubleLinkedListǁas_list__mutmut_orig.__name__ = 'xǁDoubleLinkedListǁas_list'