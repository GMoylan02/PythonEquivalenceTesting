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
class LLNode(object):
    def xǁLLNodeǁ__init____mutmut_orig(self, data, next_node=None):
        self.data = data
        self.next = next_node
    def xǁLLNodeǁ__init____mutmut_1(self, data, next_node=None):
        self.data = None
        self.next = next_node
    def xǁLLNodeǁ__init____mutmut_2(self, data, next_node=None):
        self.data = data
        self.next = None
    
    xǁLLNodeǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLLNodeǁ__init____mutmut_1': xǁLLNodeǁ__init____mutmut_1,
        'xǁLLNodeǁ__init____mutmut_2': xǁLLNodeǁ__init____mutmut_2
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLLNodeǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁLLNodeǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁLLNodeǁ__init____mutmut_orig)
    xǁLLNodeǁ__init____mutmut_orig.__name__ = 'xǁLLNodeǁ__init__'


class LinkedList(object):

    def xǁLinkedListǁ__init____mutmut_orig(self, data=None):
        self._length = 0
        self.head = None
        try:
            for val in data:
                self.push(val)
        except TypeError:
            if data:
                self.push(data)

    def xǁLinkedListǁ__init____mutmut_1(self, data=None):
        self._length = None
        self.head = None
        try:
            for val in data:
                self.push(val)
        except TypeError:
            if data:
                self.push(data)

    def xǁLinkedListǁ__init____mutmut_2(self, data=None):
        self._length = 1
        self.head = None
        try:
            for val in data:
                self.push(val)
        except TypeError:
            if data:
                self.push(data)

    def xǁLinkedListǁ__init____mutmut_3(self, data=None):
        self._length = 0
        self.head = ""
        try:
            for val in data:
                self.push(val)
        except TypeError:
            if data:
                self.push(data)

    def xǁLinkedListǁ__init____mutmut_4(self, data=None):
        self._length = 0
        self.head = None
        try:
            for val in data:
                self.push(None)
        except TypeError:
            if data:
                self.push(data)

    def xǁLinkedListǁ__init____mutmut_5(self, data=None):
        self._length = 0
        self.head = None
        try:
            for val in data:
                self.push(val)
        except TypeError:
            if data:
                self.push(None)
    
    xǁLinkedListǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLinkedListǁ__init____mutmut_1': xǁLinkedListǁ__init____mutmut_1, 
        'xǁLinkedListǁ__init____mutmut_2': xǁLinkedListǁ__init____mutmut_2, 
        'xǁLinkedListǁ__init____mutmut_3': xǁLinkedListǁ__init____mutmut_3, 
        'xǁLinkedListǁ__init____mutmut_4': xǁLinkedListǁ__init____mutmut_4, 
        'xǁLinkedListǁ__init____mutmut_5': xǁLinkedListǁ__init____mutmut_5
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLinkedListǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁLinkedListǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁLinkedListǁ__init____mutmut_orig)
    xǁLinkedListǁ__init____mutmut_orig.__name__ = 'xǁLinkedListǁ__init__'

    def xǁLinkedListǁpush__mutmut_orig(self, val):
        self.head = LLNode(val, self.head)
        self._length += 1

    def xǁLinkedListǁpush__mutmut_1(self, val):
        self.head = None
        self._length += 1

    def xǁLinkedListǁpush__mutmut_2(self, val):
        self.head = LLNode(None, self.head)
        self._length += 1

    def xǁLinkedListǁpush__mutmut_3(self, val):
        self.head = LLNode(val, None)
        self._length += 1

    def xǁLinkedListǁpush__mutmut_4(self, val):
        self.head = LLNode(self.head)
        self._length += 1

    def xǁLinkedListǁpush__mutmut_5(self, val):
        self.head = LLNode(val, )
        self._length += 1

    def xǁLinkedListǁpush__mutmut_6(self, val):
        self.head = LLNode(val, self.head)
        self._length = 1

    def xǁLinkedListǁpush__mutmut_7(self, val):
        self.head = LLNode(val, self.head)
        self._length -= 1

    def xǁLinkedListǁpush__mutmut_8(self, val):
        self.head = LLNode(val, self.head)
        self._length += 2
    
    xǁLinkedListǁpush__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLinkedListǁpush__mutmut_1': xǁLinkedListǁpush__mutmut_1, 
        'xǁLinkedListǁpush__mutmut_2': xǁLinkedListǁpush__mutmut_2, 
        'xǁLinkedListǁpush__mutmut_3': xǁLinkedListǁpush__mutmut_3, 
        'xǁLinkedListǁpush__mutmut_4': xǁLinkedListǁpush__mutmut_4, 
        'xǁLinkedListǁpush__mutmut_5': xǁLinkedListǁpush__mutmut_5, 
        'xǁLinkedListǁpush__mutmut_6': xǁLinkedListǁpush__mutmut_6, 
        'xǁLinkedListǁpush__mutmut_7': xǁLinkedListǁpush__mutmut_7, 
        'xǁLinkedListǁpush__mutmut_8': xǁLinkedListǁpush__mutmut_8
    }
    
    def push(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLinkedListǁpush__mutmut_orig"), object.__getattribute__(self, "xǁLinkedListǁpush__mutmut_mutants"), args, kwargs, self)
        return result 
    
    push.__signature__ = _mutmut_signature(xǁLinkedListǁpush__mutmut_orig)
    xǁLinkedListǁpush__mutmut_orig.__name__ = 'xǁLinkedListǁpush'

    def xǁLinkedListǁpop__mutmut_orig(self):
        if not self.head:
            raise IndexError('Cannot pop from an empty list')
        to_return = self.head
        self.head = self.head.next
        self._length -= 1
        return to_return.data

    def xǁLinkedListǁpop__mutmut_1(self):
        if self.head:
            raise IndexError('Cannot pop from an empty list')
        to_return = self.head
        self.head = self.head.next
        self._length -= 1
        return to_return.data

    def xǁLinkedListǁpop__mutmut_2(self):
        if not self.head:
            raise IndexError(None)
        to_return = self.head
        self.head = self.head.next
        self._length -= 1
        return to_return.data

    def xǁLinkedListǁpop__mutmut_3(self):
        if not self.head:
            raise IndexError('XXCannot pop from an empty listXX')
        to_return = self.head
        self.head = self.head.next
        self._length -= 1
        return to_return.data

    def xǁLinkedListǁpop__mutmut_4(self):
        if not self.head:
            raise IndexError('cannot pop from an empty list')
        to_return = self.head
        self.head = self.head.next
        self._length -= 1
        return to_return.data

    def xǁLinkedListǁpop__mutmut_5(self):
        if not self.head:
            raise IndexError('CANNOT POP FROM AN EMPTY LIST')
        to_return = self.head
        self.head = self.head.next
        self._length -= 1
        return to_return.data

    def xǁLinkedListǁpop__mutmut_6(self):
        if not self.head:
            raise IndexError('Cannot pop from an empty list')
        to_return = None
        self.head = self.head.next
        self._length -= 1
        return to_return.data

    def xǁLinkedListǁpop__mutmut_7(self):
        if not self.head:
            raise IndexError('Cannot pop from an empty list')
        to_return = self.head
        self.head = None
        self._length -= 1
        return to_return.data

    def xǁLinkedListǁpop__mutmut_8(self):
        if not self.head:
            raise IndexError('Cannot pop from an empty list')
        to_return = self.head
        self.head = self.head.next
        self._length = 1
        return to_return.data

    def xǁLinkedListǁpop__mutmut_9(self):
        if not self.head:
            raise IndexError('Cannot pop from an empty list')
        to_return = self.head
        self.head = self.head.next
        self._length += 1
        return to_return.data

    def xǁLinkedListǁpop__mutmut_10(self):
        if not self.head:
            raise IndexError('Cannot pop from an empty list')
        to_return = self.head
        self.head = self.head.next
        self._length -= 2
        return to_return.data
    
    xǁLinkedListǁpop__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLinkedListǁpop__mutmut_1': xǁLinkedListǁpop__mutmut_1, 
        'xǁLinkedListǁpop__mutmut_2': xǁLinkedListǁpop__mutmut_2, 
        'xǁLinkedListǁpop__mutmut_3': xǁLinkedListǁpop__mutmut_3, 
        'xǁLinkedListǁpop__mutmut_4': xǁLinkedListǁpop__mutmut_4, 
        'xǁLinkedListǁpop__mutmut_5': xǁLinkedListǁpop__mutmut_5, 
        'xǁLinkedListǁpop__mutmut_6': xǁLinkedListǁpop__mutmut_6, 
        'xǁLinkedListǁpop__mutmut_7': xǁLinkedListǁpop__mutmut_7, 
        'xǁLinkedListǁpop__mutmut_8': xǁLinkedListǁpop__mutmut_8, 
        'xǁLinkedListǁpop__mutmut_9': xǁLinkedListǁpop__mutmut_9, 
        'xǁLinkedListǁpop__mutmut_10': xǁLinkedListǁpop__mutmut_10
    }
    
    def pop(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLinkedListǁpop__mutmut_orig"), object.__getattribute__(self, "xǁLinkedListǁpop__mutmut_mutants"), args, kwargs, self)
        return result 
    
    pop.__signature__ = _mutmut_signature(xǁLinkedListǁpop__mutmut_orig)
    xǁLinkedListǁpop__mutmut_orig.__name__ = 'xǁLinkedListǁpop'

    def size(self):
        return self._length

    def xǁLinkedListǁsearch__mutmut_orig(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                return curr
            curr = curr.next

    def xǁLinkedListǁsearch__mutmut_1(self, val):
        curr = None
        while curr:
            if curr.data == val:
                return curr
            curr = curr.next

    def xǁLinkedListǁsearch__mutmut_2(self, val):
        curr = self.head
        while curr:
            if curr.data != val:
                return curr
            curr = curr.next

    def xǁLinkedListǁsearch__mutmut_3(self, val):
        curr = self.head
        while curr:
            if curr.data == val:
                return curr
            curr = None
    
    xǁLinkedListǁsearch__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLinkedListǁsearch__mutmut_1': xǁLinkedListǁsearch__mutmut_1, 
        'xǁLinkedListǁsearch__mutmut_2': xǁLinkedListǁsearch__mutmut_2, 
        'xǁLinkedListǁsearch__mutmut_3': xǁLinkedListǁsearch__mutmut_3
    }
    
    def search(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLinkedListǁsearch__mutmut_orig"), object.__getattribute__(self, "xǁLinkedListǁsearch__mutmut_mutants"), args, kwargs, self)
        return result 
    
    search.__signature__ = _mutmut_signature(xǁLinkedListǁsearch__mutmut_orig)
    xǁLinkedListǁsearch__mutmut_orig.__name__ = 'xǁLinkedListǁsearch'

    def xǁLinkedListǁremove__mutmut_orig(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = self.head.next
            self._length -= 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length -= 1
                return
            curr = curr.next

        raise ValueError('{} is not in the list'.format(val))

    def xǁLinkedListǁremove__mutmut_1(self, val):
        curr = None
        if curr and curr.data == val:
            self.head = self.head.next
            self._length -= 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length -= 1
                return
            curr = curr.next

        raise ValueError('{} is not in the list'.format(val))

    def xǁLinkedListǁremove__mutmut_2(self, val):
        curr = self.head
        if curr or curr.data == val:
            self.head = self.head.next
            self._length -= 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length -= 1
                return
            curr = curr.next

        raise ValueError('{} is not in the list'.format(val))

    def xǁLinkedListǁremove__mutmut_3(self, val):
        curr = self.head
        if curr and curr.data != val:
            self.head = self.head.next
            self._length -= 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length -= 1
                return
            curr = curr.next

        raise ValueError('{} is not in the list'.format(val))

    def xǁLinkedListǁremove__mutmut_4(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = None
            self._length -= 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length -= 1
                return
            curr = curr.next

        raise ValueError('{} is not in the list'.format(val))

    def xǁLinkedListǁremove__mutmut_5(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = self.head.next
            self._length = 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length -= 1
                return
            curr = curr.next

        raise ValueError('{} is not in the list'.format(val))

    def xǁLinkedListǁremove__mutmut_6(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = self.head.next
            self._length += 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length -= 1
                return
            curr = curr.next

        raise ValueError('{} is not in the list'.format(val))

    def xǁLinkedListǁremove__mutmut_7(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = self.head.next
            self._length -= 2
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length -= 1
                return
            curr = curr.next

        raise ValueError('{} is not in the list'.format(val))

    def xǁLinkedListǁremove__mutmut_8(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = self.head.next
            self._length -= 1
            return

        while curr:
            if curr.next or curr.next.data == val:
                curr.next = curr.next.next
                self._length -= 1
                return
            curr = curr.next

        raise ValueError('{} is not in the list'.format(val))

    def xǁLinkedListǁremove__mutmut_9(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = self.head.next
            self._length -= 1
            return

        while curr:
            if curr.next and curr.next.data != val:
                curr.next = curr.next.next
                self._length -= 1
                return
            curr = curr.next

        raise ValueError('{} is not in the list'.format(val))

    def xǁLinkedListǁremove__mutmut_10(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = self.head.next
            self._length -= 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = None
                self._length -= 1
                return
            curr = curr.next

        raise ValueError('{} is not in the list'.format(val))

    def xǁLinkedListǁremove__mutmut_11(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = self.head.next
            self._length -= 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length = 1
                return
            curr = curr.next

        raise ValueError('{} is not in the list'.format(val))

    def xǁLinkedListǁremove__mutmut_12(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = self.head.next
            self._length -= 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length += 1
                return
            curr = curr.next

        raise ValueError('{} is not in the list'.format(val))

    def xǁLinkedListǁremove__mutmut_13(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = self.head.next
            self._length -= 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length -= 2
                return
            curr = curr.next

        raise ValueError('{} is not in the list'.format(val))

    def xǁLinkedListǁremove__mutmut_14(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = self.head.next
            self._length -= 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length -= 1
                return
            curr = None

        raise ValueError('{} is not in the list'.format(val))

    def xǁLinkedListǁremove__mutmut_15(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = self.head.next
            self._length -= 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length -= 1
                return
            curr = curr.next

        raise ValueError(None)

    def xǁLinkedListǁremove__mutmut_16(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = self.head.next
            self._length -= 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length -= 1
                return
            curr = curr.next

        raise ValueError('{} is not in the list'.format(None))

    def xǁLinkedListǁremove__mutmut_17(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = self.head.next
            self._length -= 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length -= 1
                return
            curr = curr.next

        raise ValueError('XX{} is not in the listXX'.format(val))

    def xǁLinkedListǁremove__mutmut_18(self, val):
        curr = self.head
        if curr and curr.data == val:
            self.head = self.head.next
            self._length -= 1
            return

        while curr:
            if curr.next and curr.next.data == val:
                curr.next = curr.next.next
                self._length -= 1
                return
            curr = curr.next

        raise ValueError('{} IS NOT IN THE LIST'.format(val))
    
    xǁLinkedListǁremove__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLinkedListǁremove__mutmut_1': xǁLinkedListǁremove__mutmut_1, 
        'xǁLinkedListǁremove__mutmut_2': xǁLinkedListǁremove__mutmut_2, 
        'xǁLinkedListǁremove__mutmut_3': xǁLinkedListǁremove__mutmut_3, 
        'xǁLinkedListǁremove__mutmut_4': xǁLinkedListǁremove__mutmut_4, 
        'xǁLinkedListǁremove__mutmut_5': xǁLinkedListǁremove__mutmut_5, 
        'xǁLinkedListǁremove__mutmut_6': xǁLinkedListǁremove__mutmut_6, 
        'xǁLinkedListǁremove__mutmut_7': xǁLinkedListǁremove__mutmut_7, 
        'xǁLinkedListǁremove__mutmut_8': xǁLinkedListǁremove__mutmut_8, 
        'xǁLinkedListǁremove__mutmut_9': xǁLinkedListǁremove__mutmut_9, 
        'xǁLinkedListǁremove__mutmut_10': xǁLinkedListǁremove__mutmut_10, 
        'xǁLinkedListǁremove__mutmut_11': xǁLinkedListǁremove__mutmut_11, 
        'xǁLinkedListǁremove__mutmut_12': xǁLinkedListǁremove__mutmut_12, 
        'xǁLinkedListǁremove__mutmut_13': xǁLinkedListǁremove__mutmut_13, 
        'xǁLinkedListǁremove__mutmut_14': xǁLinkedListǁremove__mutmut_14, 
        'xǁLinkedListǁremove__mutmut_15': xǁLinkedListǁremove__mutmut_15, 
        'xǁLinkedListǁremove__mutmut_16': xǁLinkedListǁremove__mutmut_16, 
        'xǁLinkedListǁremove__mutmut_17': xǁLinkedListǁremove__mutmut_17, 
        'xǁLinkedListǁremove__mutmut_18': xǁLinkedListǁremove__mutmut_18
    }
    
    def remove(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLinkedListǁremove__mutmut_orig"), object.__getattribute__(self, "xǁLinkedListǁremove__mutmut_mutants"), args, kwargs, self)
        return result 
    
    remove.__signature__ = _mutmut_signature(xǁLinkedListǁremove__mutmut_orig)
    xǁLinkedListǁremove__mutmut_orig.__name__ = 'xǁLinkedListǁremove'

    def xǁLinkedListǁdisplay__mutmut_orig(self):
        if not self.head:
            return '()'
        curr = self.head
        display = '('
        while curr:
            display += str(curr.data) + ', '
            curr = curr.next
        return display[:-2] + ')'

    def xǁLinkedListǁdisplay__mutmut_1(self):
        if self.head:
            return '()'
        curr = self.head
        display = '('
        while curr:
            display += str(curr.data) + ', '
            curr = curr.next
        return display[:-2] + ')'

    def xǁLinkedListǁdisplay__mutmut_2(self):
        if not self.head:
            return 'XX()XX'
        curr = self.head
        display = '('
        while curr:
            display += str(curr.data) + ', '
            curr = curr.next
        return display[:-2] + ')'

    def xǁLinkedListǁdisplay__mutmut_3(self):
        if not self.head:
            return '()'
        curr = None
        display = '('
        while curr:
            display += str(curr.data) + ', '
            curr = curr.next
        return display[:-2] + ')'

    def xǁLinkedListǁdisplay__mutmut_4(self):
        if not self.head:
            return '()'
        curr = self.head
        display = None
        while curr:
            display += str(curr.data) + ', '
            curr = curr.next
        return display[:-2] + ')'

    def xǁLinkedListǁdisplay__mutmut_5(self):
        if not self.head:
            return '()'
        curr = self.head
        display = 'XX(XX'
        while curr:
            display += str(curr.data) + ', '
            curr = curr.next
        return display[:-2] + ')'

    def xǁLinkedListǁdisplay__mutmut_6(self):
        if not self.head:
            return '()'
        curr = self.head
        display = '('
        while curr:
            display = str(curr.data) + ', '
            curr = curr.next
        return display[:-2] + ')'

    def xǁLinkedListǁdisplay__mutmut_7(self):
        if not self.head:
            return '()'
        curr = self.head
        display = '('
        while curr:
            display -= str(curr.data) + ', '
            curr = curr.next
        return display[:-2] + ')'

    def xǁLinkedListǁdisplay__mutmut_8(self):
        if not self.head:
            return '()'
        curr = self.head
        display = '('
        while curr:
            display += str(curr.data) - ', '
            curr = curr.next
        return display[:-2] + ')'

    def xǁLinkedListǁdisplay__mutmut_9(self):
        if not self.head:
            return '()'
        curr = self.head
        display = '('
        while curr:
            display += str(None) + ', '
            curr = curr.next
        return display[:-2] + ')'

    def xǁLinkedListǁdisplay__mutmut_10(self):
        if not self.head:
            return '()'
        curr = self.head
        display = '('
        while curr:
            display += str(curr.data) + 'XX, XX'
            curr = curr.next
        return display[:-2] + ')'

    def xǁLinkedListǁdisplay__mutmut_11(self):
        if not self.head:
            return '()'
        curr = self.head
        display = '('
        while curr:
            display += str(curr.data) + ', '
            curr = None
        return display[:-2] + ')'

    def xǁLinkedListǁdisplay__mutmut_12(self):
        if not self.head:
            return '()'
        curr = self.head
        display = '('
        while curr:
            display += str(curr.data) + ', '
            curr = curr.next
        return display[:-2] - ')'

    def xǁLinkedListǁdisplay__mutmut_13(self):
        if not self.head:
            return '()'
        curr = self.head
        display = '('
        while curr:
            display += str(curr.data) + ', '
            curr = curr.next
        return display[:+2] + ')'

    def xǁLinkedListǁdisplay__mutmut_14(self):
        if not self.head:
            return '()'
        curr = self.head
        display = '('
        while curr:
            display += str(curr.data) + ', '
            curr = curr.next
        return display[:-3] + ')'

    def xǁLinkedListǁdisplay__mutmut_15(self):
        if not self.head:
            return '()'
        curr = self.head
        display = '('
        while curr:
            display += str(curr.data) + ', '
            curr = curr.next
        return display[:-2] + 'XX)XX'
    
    xǁLinkedListǁdisplay__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLinkedListǁdisplay__mutmut_1': xǁLinkedListǁdisplay__mutmut_1, 
        'xǁLinkedListǁdisplay__mutmut_2': xǁLinkedListǁdisplay__mutmut_2, 
        'xǁLinkedListǁdisplay__mutmut_3': xǁLinkedListǁdisplay__mutmut_3, 
        'xǁLinkedListǁdisplay__mutmut_4': xǁLinkedListǁdisplay__mutmut_4, 
        'xǁLinkedListǁdisplay__mutmut_5': xǁLinkedListǁdisplay__mutmut_5, 
        'xǁLinkedListǁdisplay__mutmut_6': xǁLinkedListǁdisplay__mutmut_6, 
        'xǁLinkedListǁdisplay__mutmut_7': xǁLinkedListǁdisplay__mutmut_7, 
        'xǁLinkedListǁdisplay__mutmut_8': xǁLinkedListǁdisplay__mutmut_8, 
        'xǁLinkedListǁdisplay__mutmut_9': xǁLinkedListǁdisplay__mutmut_9, 
        'xǁLinkedListǁdisplay__mutmut_10': xǁLinkedListǁdisplay__mutmut_10, 
        'xǁLinkedListǁdisplay__mutmut_11': xǁLinkedListǁdisplay__mutmut_11, 
        'xǁLinkedListǁdisplay__mutmut_12': xǁLinkedListǁdisplay__mutmut_12, 
        'xǁLinkedListǁdisplay__mutmut_13': xǁLinkedListǁdisplay__mutmut_13, 
        'xǁLinkedListǁdisplay__mutmut_14': xǁLinkedListǁdisplay__mutmut_14, 
        'xǁLinkedListǁdisplay__mutmut_15': xǁLinkedListǁdisplay__mutmut_15
    }
    
    def display(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLinkedListǁdisplay__mutmut_orig"), object.__getattribute__(self, "xǁLinkedListǁdisplay__mutmut_mutants"), args, kwargs, self)
        return result 
    
    display.__signature__ = _mutmut_signature(xǁLinkedListǁdisplay__mutmut_orig)
    xǁLinkedListǁdisplay__mutmut_orig.__name__ = 'xǁLinkedListǁdisplay'
