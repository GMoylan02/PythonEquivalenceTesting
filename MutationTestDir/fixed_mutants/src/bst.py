from .a_queue import Queue
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


class BSTNode(object):

    def xǁBSTNodeǁ__init____mutmut_orig(self, val=None, parent =None):
        self.val = val
        self.right = ""
        self.left = None
        self.parent = parent
        self.height = 1

    def xǁBSTNodeǁ__init____mutmut_1(self, val=None, parent =None):
        self.val = None
        self.right = ""
        self.left = None
        self.parent = parent
        self.height = 1

    def xǁBSTNodeǁ__init____mutmut_2(self, val=None, parent =None):
        self.val = val
        self.right = None
        self.left = None
        self.parent = parent
        self.height = 1

    def xǁBSTNodeǁ__init____mutmut_3(self, val=None, parent =None):
        self.val = val
        self.right = "XXXX"
        self.left = None
        self.parent = parent
        self.height = 1

    def xǁBSTNodeǁ__init____mutmut_4(self, val=None, parent =None):
        self.val = val
        self.right = ""
        self.left = ""
        self.parent = parent
        self.height = 1

    def xǁBSTNodeǁ__init____mutmut_5(self, val=None, parent =None):
        self.val = val
        self.right = ""
        self.left = None
        self.parent = None
        self.height = 1

    def xǁBSTNodeǁ__init____mutmut_6(self, val=None, parent =None):
        self.val = val
        self.right = ""
        self.left = None
        self.parent = parent
        self.height = None

    def xǁBSTNodeǁ__init____mutmut_7(self, val=None, parent =None):
        self.val = val
        self.right = ""
        self.left = None
        self.parent = parent
        self.height = 2
    
    xǁBSTNodeǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBSTNodeǁ__init____mutmut_1': xǁBSTNodeǁ__init____mutmut_1, 
        'xǁBSTNodeǁ__init____mutmut_2': xǁBSTNodeǁ__init____mutmut_2, 
        'xǁBSTNodeǁ__init____mutmut_3': xǁBSTNodeǁ__init____mutmut_3, 
        'xǁBSTNodeǁ__init____mutmut_4': xǁBSTNodeǁ__init____mutmut_4, 
        'xǁBSTNodeǁ__init____mutmut_5': xǁBSTNodeǁ__init____mutmut_5, 
        'xǁBSTNodeǁ__init____mutmut_6': xǁBSTNodeǁ__init____mutmut_6, 
        'xǁBSTNodeǁ__init____mutmut_7': xǁBSTNodeǁ__init____mutmut_7
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBSTNodeǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁBSTNodeǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁBSTNodeǁ__init____mutmut_orig)
    xǁBSTNodeǁ__init____mutmut_orig.__name__ = 'xǁBSTNodeǁ__init__'

    def xǁBSTNodeǁ_is_leaf__mutmut_orig(self):
        return not (self.right or self.left)

    def xǁBSTNodeǁ_is_leaf__mutmut_1(self):
        return (self.right or self.left)

    def xǁBSTNodeǁ_is_leaf__mutmut_2(self):
        return not (self.right and self.left)
    
    xǁBSTNodeǁ_is_leaf__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBSTNodeǁ_is_leaf__mutmut_1': xǁBSTNodeǁ_is_leaf__mutmut_1, 
        'xǁBSTNodeǁ_is_leaf__mutmut_2': xǁBSTNodeǁ_is_leaf__mutmut_2
    }
    
    def _is_leaf(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBSTNodeǁ_is_leaf__mutmut_orig"), object.__getattribute__(self, "xǁBSTNodeǁ_is_leaf__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _is_leaf.__signature__ = _mutmut_signature(xǁBSTNodeǁ_is_leaf__mutmut_orig)
    xǁBSTNodeǁ_is_leaf__mutmut_orig.__name__ = 'xǁBSTNodeǁ_is_leaf'

    def xǁBSTNodeǁ_is_interior__mutmut_orig(self):
        return (self.right and self.left)

    def xǁBSTNodeǁ_is_interior__mutmut_1(self):
        return (self.right or self.left)
    
    xǁBSTNodeǁ_is_interior__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBSTNodeǁ_is_interior__mutmut_1': xǁBSTNodeǁ_is_interior__mutmut_1
    }
    
    def _is_interior(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBSTNodeǁ_is_interior__mutmut_orig"), object.__getattribute__(self, "xǁBSTNodeǁ_is_interior__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _is_interior.__signature__ = _mutmut_signature(xǁBSTNodeǁ_is_interior__mutmut_orig)
    xǁBSTNodeǁ_is_interior__mutmut_orig.__name__ = 'xǁBSTNodeǁ_is_interior'

    def xǁBSTNodeǁ_onlychild__mutmut_orig(self):
        if self.left and not self.right:
            return 'left'
        if self.right and not self.left:
            return 'right'

    def xǁBSTNodeǁ_onlychild__mutmut_1(self):
        if self.left or not self.right:
            return 'left'
        if self.right and not self.left:
            return 'right'

    def xǁBSTNodeǁ_onlychild__mutmut_2(self):
        if self.left and self.right:
            return 'left'
        if self.right and not self.left:
            return 'right'

    def xǁBSTNodeǁ_onlychild__mutmut_3(self):
        if self.left and not self.right:
            return 'XXleftXX'
        if self.right and not self.left:
            return 'right'

    def xǁBSTNodeǁ_onlychild__mutmut_4(self):
        if self.left and not self.right:
            return 'LEFT'
        if self.right and not self.left:
            return 'right'

    def xǁBSTNodeǁ_onlychild__mutmut_5(self):
        if self.left and not self.right:
            return 'left'
        if self.right or not self.left:
            return 'right'

    def xǁBSTNodeǁ_onlychild__mutmut_6(self):
        if self.left and not self.right:
            return 'left'
        if self.right and self.left:
            return 'right'

    def xǁBSTNodeǁ_onlychild__mutmut_7(self):
        if self.left and not self.right:
            return 'left'
        if self.right and not self.left:
            return 'XXrightXX'

    def xǁBSTNodeǁ_onlychild__mutmut_8(self):
        if self.left and not self.right:
            return 'left'
        if self.right and not self.left:
            return 'RIGHT'
    
    xǁBSTNodeǁ_onlychild__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBSTNodeǁ_onlychild__mutmut_1': xǁBSTNodeǁ_onlychild__mutmut_1, 
        'xǁBSTNodeǁ_onlychild__mutmut_2': xǁBSTNodeǁ_onlychild__mutmut_2, 
        'xǁBSTNodeǁ_onlychild__mutmut_3': xǁBSTNodeǁ_onlychild__mutmut_3, 
        'xǁBSTNodeǁ_onlychild__mutmut_4': xǁBSTNodeǁ_onlychild__mutmut_4, 
        'xǁBSTNodeǁ_onlychild__mutmut_5': xǁBSTNodeǁ_onlychild__mutmut_5, 
        'xǁBSTNodeǁ_onlychild__mutmut_6': xǁBSTNodeǁ_onlychild__mutmut_6, 
        'xǁBSTNodeǁ_onlychild__mutmut_7': xǁBSTNodeǁ_onlychild__mutmut_7, 
        'xǁBSTNodeǁ_onlychild__mutmut_8': xǁBSTNodeǁ_onlychild__mutmut_8
    }
    
    def _onlychild(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBSTNodeǁ_onlychild__mutmut_orig"), object.__getattribute__(self, "xǁBSTNodeǁ_onlychild__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _onlychild.__signature__ = _mutmut_signature(xǁBSTNodeǁ_onlychild__mutmut_orig)
    xǁBSTNodeǁ_onlychild__mutmut_orig.__name__ = 'xǁBSTNodeǁ_onlychild'

    def xǁBSTNodeǁ_side__mutmut_orig(self):
        if self.parent:
            return 'left' if self.parent.left == self else 'right'

    def xǁBSTNodeǁ_side__mutmut_1(self):
        if self.parent:
            return 'XXleftXX' if self.parent.left == self else 'right'

    def xǁBSTNodeǁ_side__mutmut_2(self):
        if self.parent:
            return 'LEFT' if self.parent.left == self else 'right'

    def xǁBSTNodeǁ_side__mutmut_3(self):
        if self.parent:
            return 'left' if self.parent.left != self else 'right'

    def xǁBSTNodeǁ_side__mutmut_4(self):
        if self.parent:
            return 'left' if self.parent.left == self else 'XXrightXX'

    def xǁBSTNodeǁ_side__mutmut_5(self):
        if self.parent:
            return 'left' if self.parent.left == self else 'RIGHT'
    
    xǁBSTNodeǁ_side__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBSTNodeǁ_side__mutmut_1': xǁBSTNodeǁ_side__mutmut_1, 
        'xǁBSTNodeǁ_side__mutmut_2': xǁBSTNodeǁ_side__mutmut_2, 
        'xǁBSTNodeǁ_side__mutmut_3': xǁBSTNodeǁ_side__mutmut_3, 
        'xǁBSTNodeǁ_side__mutmut_4': xǁBSTNodeǁ_side__mutmut_4, 
        'xǁBSTNodeǁ_side__mutmut_5': xǁBSTNodeǁ_side__mutmut_5
    }
    
    def _side(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBSTNodeǁ_side__mutmut_orig"), object.__getattribute__(self, "xǁBSTNodeǁ_side__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _side.__signature__ = _mutmut_signature(xǁBSTNodeǁ_side__mutmut_orig)
    xǁBSTNodeǁ_side__mutmut_orig.__name__ = 'xǁBSTNodeǁ_side'


class Bst(object):

    def xǁBstǁ__init____mutmut_orig(self, data=None):
        self._size = 0
        self.root = None
        if data:
            for i in data:
                self.insert(i)

    def xǁBstǁ__init____mutmut_1(self, data=None):
        self._size = None
        self.root = None
        if data:
            for i in data:
                self.insert(i)

    def xǁBstǁ__init____mutmut_2(self, data=None):
        self._size = 1
        self.root = None
        if data:
            for i in data:
                self.insert(i)

    def xǁBstǁ__init____mutmut_3(self, data=None):
        self._size = 0
        self.root = ""
        if data:
            for i in data:
                self.insert(i)

    def xǁBstǁ__init____mutmut_4(self, data=None):
        self._size = 0
        self.root = None
        if data:
            for i in data:
                self.insert(None)
    
    xǁBstǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁ__init____mutmut_1': xǁBstǁ__init____mutmut_1, 
        'xǁBstǁ__init____mutmut_2': xǁBstǁ__init____mutmut_2, 
        'xǁBstǁ__init____mutmut_3': xǁBstǁ__init____mutmut_3, 
        'xǁBstǁ__init____mutmut_4': xǁBstǁ__init____mutmut_4
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁBstǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁBstǁ__init____mutmut_orig)
    xǁBstǁ__init____mutmut_orig.__name__ = 'xǁBstǁ__init__'

    def xǁBstǁinsert__mutmut_orig(self, val):
        if not self.root:
            self.root = BSTNode(val)
            self._size += 1
        else:
            self._step(val, self.root)

    def xǁBstǁinsert__mutmut_1(self, val):
        if self.root:
            self.root = BSTNode(val)
            self._size += 1
        else:
            self._step(val, self.root)

    def xǁBstǁinsert__mutmut_2(self, val):
        if not self.root:
            self.root = None
            self._size += 1
        else:
            self._step(val, self.root)

    def xǁBstǁinsert__mutmut_3(self, val):
        if not self.root:
            self.root = BSTNode(None)
            self._size += 1
        else:
            self._step(val, self.root)

    def xǁBstǁinsert__mutmut_4(self, val):
        if not self.root:
            self.root = BSTNode(val)
            self._size = 1
        else:
            self._step(val, self.root)

    def xǁBstǁinsert__mutmut_5(self, val):
        if not self.root:
            self.root = BSTNode(val)
            self._size -= 1
        else:
            self._step(val, self.root)

    def xǁBstǁinsert__mutmut_6(self, val):
        if not self.root:
            self.root = BSTNode(val)
            self._size += 2
        else:
            self._step(val, self.root)

    def xǁBstǁinsert__mutmut_7(self, val):
        if not self.root:
            self.root = BSTNode(val)
            self._size += 1
        else:
            self._step(None, self.root)

    def xǁBstǁinsert__mutmut_8(self, val):
        if not self.root:
            self.root = BSTNode(val)
            self._size += 1
        else:
            self._step(val, None)

    def xǁBstǁinsert__mutmut_9(self, val):
        if not self.root:
            self.root = BSTNode(val)
            self._size += 1
        else:
            self._step(self.root)

    def xǁBstǁinsert__mutmut_10(self, val):
        if not self.root:
            self.root = BSTNode(val)
            self._size += 1
        else:
            self._step(val, )
    
    xǁBstǁinsert__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁinsert__mutmut_1': xǁBstǁinsert__mutmut_1, 
        'xǁBstǁinsert__mutmut_2': xǁBstǁinsert__mutmut_2, 
        'xǁBstǁinsert__mutmut_3': xǁBstǁinsert__mutmut_3, 
        'xǁBstǁinsert__mutmut_4': xǁBstǁinsert__mutmut_4, 
        'xǁBstǁinsert__mutmut_5': xǁBstǁinsert__mutmut_5, 
        'xǁBstǁinsert__mutmut_6': xǁBstǁinsert__mutmut_6, 
        'xǁBstǁinsert__mutmut_7': xǁBstǁinsert__mutmut_7, 
        'xǁBstǁinsert__mutmut_8': xǁBstǁinsert__mutmut_8, 
        'xǁBstǁinsert__mutmut_9': xǁBstǁinsert__mutmut_9, 
        'xǁBstǁinsert__mutmut_10': xǁBstǁinsert__mutmut_10
    }
    
    def insert(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁinsert__mutmut_orig"), object.__getattribute__(self, "xǁBstǁinsert__mutmut_mutants"), args, kwargs, self)
        return result 
    
    insert.__signature__ = _mutmut_signature(xǁBstǁinsert__mutmut_orig)
    xǁBstǁinsert__mutmut_orig.__name__ = 'xǁBstǁinsert'

    def xǁBstǁ_step__mutmut_orig(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, 'left', val)
        elif val > curr.val:
            curr = self._set_child(curr, 'right', val)
        return curr.height

    def xǁBstǁ_step__mutmut_1(self, val, curr: BSTNode):
        if val <= curr.val:
            curr = self._set_child(curr, 'left', val)
        elif val > curr.val:
            curr = self._set_child(curr, 'right', val)
        return curr.height

    def xǁBstǁ_step__mutmut_2(self, val, curr: BSTNode):
        if val < curr.val:
            curr = None
        elif val > curr.val:
            curr = self._set_child(curr, 'right', val)
        return curr.height

    def xǁBstǁ_step__mutmut_3(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(None, 'left', val)
        elif val > curr.val:
            curr = self._set_child(curr, 'right', val)
        return curr.height

    def xǁBstǁ_step__mutmut_4(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, None, val)
        elif val > curr.val:
            curr = self._set_child(curr, 'right', val)
        return curr.height

    def xǁBstǁ_step__mutmut_5(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, 'left', None)
        elif val > curr.val:
            curr = self._set_child(curr, 'right', val)
        return curr.height

    def xǁBstǁ_step__mutmut_6(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child('left', val)
        elif val > curr.val:
            curr = self._set_child(curr, 'right', val)
        return curr.height

    def xǁBstǁ_step__mutmut_7(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, val)
        elif val > curr.val:
            curr = self._set_child(curr, 'right', val)
        return curr.height

    def xǁBstǁ_step__mutmut_8(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, 'left', )
        elif val > curr.val:
            curr = self._set_child(curr, 'right', val)
        return curr.height

    def xǁBstǁ_step__mutmut_9(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, 'XXleftXX', val)
        elif val > curr.val:
            curr = self._set_child(curr, 'right', val)
        return curr.height

    def xǁBstǁ_step__mutmut_10(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, 'LEFT', val)
        elif val > curr.val:
            curr = self._set_child(curr, 'right', val)
        return curr.height

    def xǁBstǁ_step__mutmut_11(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, 'left', val)
        elif val >= curr.val:
            curr = self._set_child(curr, 'right', val)
        return curr.height

    def xǁBstǁ_step__mutmut_12(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, 'left', val)
        elif val > curr.val:
            curr = None
        return curr.height

    def xǁBstǁ_step__mutmut_13(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, 'left', val)
        elif val > curr.val:
            curr = self._set_child(None, 'right', val)
        return curr.height

    def xǁBstǁ_step__mutmut_14(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, 'left', val)
        elif val > curr.val:
            curr = self._set_child(curr, None, val)
        return curr.height

    def xǁBstǁ_step__mutmut_15(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, 'left', val)
        elif val > curr.val:
            curr = self._set_child(curr, 'right', None)
        return curr.height

    def xǁBstǁ_step__mutmut_16(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, 'left', val)
        elif val > curr.val:
            curr = self._set_child('right', val)
        return curr.height

    def xǁBstǁ_step__mutmut_17(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, 'left', val)
        elif val > curr.val:
            curr = self._set_child(curr, val)
        return curr.height

    def xǁBstǁ_step__mutmut_18(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, 'left', val)
        elif val > curr.val:
            curr = self._set_child(curr, 'right', )
        return curr.height

    def xǁBstǁ_step__mutmut_19(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, 'left', val)
        elif val > curr.val:
            curr = self._set_child(curr, 'XXrightXX', val)
        return curr.height

    def xǁBstǁ_step__mutmut_20(self, val, curr: BSTNode):
        if val < curr.val:
            curr = self._set_child(curr, 'left', val)
        elif val > curr.val:
            curr = self._set_child(curr, 'RIGHT', val)
        return curr.height
    
    xǁBstǁ_step__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁ_step__mutmut_1': xǁBstǁ_step__mutmut_1, 
        'xǁBstǁ_step__mutmut_2': xǁBstǁ_step__mutmut_2, 
        'xǁBstǁ_step__mutmut_3': xǁBstǁ_step__mutmut_3, 
        'xǁBstǁ_step__mutmut_4': xǁBstǁ_step__mutmut_4, 
        'xǁBstǁ_step__mutmut_5': xǁBstǁ_step__mutmut_5, 
        'xǁBstǁ_step__mutmut_6': xǁBstǁ_step__mutmut_6, 
        'xǁBstǁ_step__mutmut_7': xǁBstǁ_step__mutmut_7, 
        'xǁBstǁ_step__mutmut_8': xǁBstǁ_step__mutmut_8, 
        'xǁBstǁ_step__mutmut_9': xǁBstǁ_step__mutmut_9, 
        'xǁBstǁ_step__mutmut_10': xǁBstǁ_step__mutmut_10, 
        'xǁBstǁ_step__mutmut_11': xǁBstǁ_step__mutmut_11, 
        'xǁBstǁ_step__mutmut_12': xǁBstǁ_step__mutmut_12, 
        'xǁBstǁ_step__mutmut_13': xǁBstǁ_step__mutmut_13, 
        'xǁBstǁ_step__mutmut_14': xǁBstǁ_step__mutmut_14, 
        'xǁBstǁ_step__mutmut_15': xǁBstǁ_step__mutmut_15, 
        'xǁBstǁ_step__mutmut_16': xǁBstǁ_step__mutmut_16, 
        'xǁBstǁ_step__mutmut_17': xǁBstǁ_step__mutmut_17, 
        'xǁBstǁ_step__mutmut_18': xǁBstǁ_step__mutmut_18, 
        'xǁBstǁ_step__mutmut_19': xǁBstǁ_step__mutmut_19, 
        'xǁBstǁ_step__mutmut_20': xǁBstǁ_step__mutmut_20
    }
    
    def _step(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁ_step__mutmut_orig"), object.__getattribute__(self, "xǁBstǁ_step__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _step.__signature__ = _mutmut_signature(xǁBstǁ_step__mutmut_orig)
    xǁBstǁ_step__mutmut_orig.__name__ = 'xǁBstǁ_step'

    def xǁBstǁ_set_child__mutmut_orig(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_1(self, curr: BSTNode, side, val):
        child = None
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_2(self, curr: BSTNode, side, val):
        child = getattr(None, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_3(self, curr: BSTNode, side, val):
        child = getattr(curr, None)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_4(self, curr: BSTNode, side, val):
        child = getattr(side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_5(self, curr: BSTNode, side, val):
        child = getattr(curr, )
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_6(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = None
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_7(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(None, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_8(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, None)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_9(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_10(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, )
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_11(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height < count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_12(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height = 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_13(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height -= 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_14(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 2
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_15(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(None, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_16(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, None, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_17(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, None)
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_18(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_19(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_20(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, )
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_21(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(None, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_22(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, None))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_23(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_24(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, ))
            self._size += 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_25(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size = 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_26(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size -= 1
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_27(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 2
            if curr.height == 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_28(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height != 1:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_29(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 2:           
                curr.height += 1
        return curr

    def xǁBstǁ_set_child__mutmut_30(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height = 1
        return curr

    def xǁBstǁ_set_child__mutmut_31(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height -= 1
        return curr

    def xǁBstǁ_set_child__mutmut_32(self, curr: BSTNode, side, val):
        child = getattr(curr, side)
        if child:
            count = self._step(val, child)
            if curr.height <= count:
                curr.height += 1
        else:
            setattr(curr, side, BSTNode(val, curr))
            self._size += 1
            if curr.height == 1:           
                curr.height += 2
        return curr
    
    xǁBstǁ_set_child__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁ_set_child__mutmut_1': xǁBstǁ_set_child__mutmut_1, 
        'xǁBstǁ_set_child__mutmut_2': xǁBstǁ_set_child__mutmut_2, 
        'xǁBstǁ_set_child__mutmut_3': xǁBstǁ_set_child__mutmut_3, 
        'xǁBstǁ_set_child__mutmut_4': xǁBstǁ_set_child__mutmut_4, 
        'xǁBstǁ_set_child__mutmut_5': xǁBstǁ_set_child__mutmut_5, 
        'xǁBstǁ_set_child__mutmut_6': xǁBstǁ_set_child__mutmut_6, 
        'xǁBstǁ_set_child__mutmut_7': xǁBstǁ_set_child__mutmut_7, 
        'xǁBstǁ_set_child__mutmut_8': xǁBstǁ_set_child__mutmut_8, 
        'xǁBstǁ_set_child__mutmut_9': xǁBstǁ_set_child__mutmut_9, 
        'xǁBstǁ_set_child__mutmut_10': xǁBstǁ_set_child__mutmut_10, 
        'xǁBstǁ_set_child__mutmut_11': xǁBstǁ_set_child__mutmut_11, 
        'xǁBstǁ_set_child__mutmut_12': xǁBstǁ_set_child__mutmut_12, 
        'xǁBstǁ_set_child__mutmut_13': xǁBstǁ_set_child__mutmut_13, 
        'xǁBstǁ_set_child__mutmut_14': xǁBstǁ_set_child__mutmut_14, 
        'xǁBstǁ_set_child__mutmut_15': xǁBstǁ_set_child__mutmut_15, 
        'xǁBstǁ_set_child__mutmut_16': xǁBstǁ_set_child__mutmut_16, 
        'xǁBstǁ_set_child__mutmut_17': xǁBstǁ_set_child__mutmut_17, 
        'xǁBstǁ_set_child__mutmut_18': xǁBstǁ_set_child__mutmut_18, 
        'xǁBstǁ_set_child__mutmut_19': xǁBstǁ_set_child__mutmut_19, 
        'xǁBstǁ_set_child__mutmut_20': xǁBstǁ_set_child__mutmut_20, 
        'xǁBstǁ_set_child__mutmut_21': xǁBstǁ_set_child__mutmut_21, 
        'xǁBstǁ_set_child__mutmut_22': xǁBstǁ_set_child__mutmut_22, 
        'xǁBstǁ_set_child__mutmut_23': xǁBstǁ_set_child__mutmut_23, 
        'xǁBstǁ_set_child__mutmut_24': xǁBstǁ_set_child__mutmut_24, 
        'xǁBstǁ_set_child__mutmut_25': xǁBstǁ_set_child__mutmut_25, 
        'xǁBstǁ_set_child__mutmut_26': xǁBstǁ_set_child__mutmut_26, 
        'xǁBstǁ_set_child__mutmut_27': xǁBstǁ_set_child__mutmut_27, 
        'xǁBstǁ_set_child__mutmut_28': xǁBstǁ_set_child__mutmut_28, 
        'xǁBstǁ_set_child__mutmut_29': xǁBstǁ_set_child__mutmut_29, 
        'xǁBstǁ_set_child__mutmut_30': xǁBstǁ_set_child__mutmut_30, 
        'xǁBstǁ_set_child__mutmut_31': xǁBstǁ_set_child__mutmut_31, 
        'xǁBstǁ_set_child__mutmut_32': xǁBstǁ_set_child__mutmut_32
    }
    
    def _set_child(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁ_set_child__mutmut_orig"), object.__getattribute__(self, "xǁBstǁ_set_child__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _set_child.__signature__ = _mutmut_signature(xǁBstǁ_set_child__mutmut_orig)
    xǁBstǁ_set_child__mutmut_orig.__name__ = 'xǁBstǁ_set_child'

    def xǁBstǁsearch__mutmut_orig(self, val):
        curr = self.root
        while curr:
            if curr.val == val:
                return curr
            elif val < curr.val:
                curr = curr.left
            else:
                curr = curr.right

    def xǁBstǁsearch__mutmut_1(self, val):
        curr = None
        while curr:
            if curr.val == val:
                return curr
            elif val < curr.val:
                curr = curr.left
            else:
                curr = curr.right

    def xǁBstǁsearch__mutmut_2(self, val):
        curr = self.root
        while curr:
            if curr.val != val:
                return curr
            elif val < curr.val:
                curr = curr.left
            else:
                curr = curr.right

    def xǁBstǁsearch__mutmut_3(self, val):
        curr = self.root
        while curr:
            if curr.val == val:
                return curr
            elif val <= curr.val:
                curr = curr.left
            else:
                curr = curr.right

    def xǁBstǁsearch__mutmut_4(self, val):
        curr = self.root
        while curr:
            if curr.val == val:
                return curr
            elif val < curr.val:
                curr = None
            else:
                curr = curr.right

    def xǁBstǁsearch__mutmut_5(self, val):
        curr = self.root
        while curr:
            if curr.val == val:
                return curr
            elif val < curr.val:
                curr = curr.left
            else:
                curr = None
    
    xǁBstǁsearch__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁsearch__mutmut_1': xǁBstǁsearch__mutmut_1, 
        'xǁBstǁsearch__mutmut_2': xǁBstǁsearch__mutmut_2, 
        'xǁBstǁsearch__mutmut_3': xǁBstǁsearch__mutmut_3, 
        'xǁBstǁsearch__mutmut_4': xǁBstǁsearch__mutmut_4, 
        'xǁBstǁsearch__mutmut_5': xǁBstǁsearch__mutmut_5
    }
    
    def search(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁsearch__mutmut_orig"), object.__getattribute__(self, "xǁBstǁsearch__mutmut_mutants"), args, kwargs, self)
        return result 
    
    search.__signature__ = _mutmut_signature(xǁBstǁsearch__mutmut_orig)
    xǁBstǁsearch__mutmut_orig.__name__ = 'xǁBstǁsearch'

    def xǁBstǁdepth__mutmut_orig(self):
        return 0 if not self.root else self.root.height

    def xǁBstǁdepth__mutmut_1(self):
        return 1 if not self.root else self.root.height

    def xǁBstǁdepth__mutmut_2(self):
        return 0 if self.root else self.root.height
    
    xǁBstǁdepth__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁdepth__mutmut_1': xǁBstǁdepth__mutmut_1, 
        'xǁBstǁdepth__mutmut_2': xǁBstǁdepth__mutmut_2
    }
    
    def depth(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁdepth__mutmut_orig"), object.__getattribute__(self, "xǁBstǁdepth__mutmut_mutants"), args, kwargs, self)
        return result 
    
    depth.__signature__ = _mutmut_signature(xǁBstǁdepth__mutmut_orig)
    xǁBstǁdepth__mutmut_orig.__name__ = 'xǁBstǁdepth'

    def xǁBstǁcontains__mutmut_orig(self, val):
        return self.search(val) is not None

    def xǁBstǁcontains__mutmut_1(self, val):
        return self.search(None) is not None

    def xǁBstǁcontains__mutmut_2(self, val):
        return self.search(val) is None
    
    xǁBstǁcontains__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁcontains__mutmut_1': xǁBstǁcontains__mutmut_1, 
        'xǁBstǁcontains__mutmut_2': xǁBstǁcontains__mutmut_2
    }
    
    def contains(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁcontains__mutmut_orig"), object.__getattribute__(self, "xǁBstǁcontains__mutmut_mutants"), args, kwargs, self)
        return result 
    
    contains.__signature__ = _mutmut_signature(xǁBstǁcontains__mutmut_orig)
    xǁBstǁcontains__mutmut_orig.__name__ = 'xǁBstǁcontains'

    def xǁBstǁbalance__mutmut_orig(self, tree: BSTNode=None):
        if not tree:
            tree = self.root
            if not tree:
                return 0
        leftbranch = 0 if not tree.left else tree.left.height
        rightbranch = 0 if not tree.right else tree.right.height
        return leftbranch - rightbranch

    def xǁBstǁbalance__mutmut_1(self, tree: BSTNode=None):
        if tree:
            tree = self.root
            if not tree:
                return 0
        leftbranch = 0 if not tree.left else tree.left.height
        rightbranch = 0 if not tree.right else tree.right.height
        return leftbranch - rightbranch

    def xǁBstǁbalance__mutmut_2(self, tree: BSTNode=None):
        if not tree:
            tree = None
            if not tree:
                return 0
        leftbranch = 0 if not tree.left else tree.left.height
        rightbranch = 0 if not tree.right else tree.right.height
        return leftbranch - rightbranch

    def xǁBstǁbalance__mutmut_3(self, tree: BSTNode=None):
        if not tree:
            tree = self.root
            if tree:
                return 0
        leftbranch = 0 if not tree.left else tree.left.height
        rightbranch = 0 if not tree.right else tree.right.height
        return leftbranch - rightbranch

    def xǁBstǁbalance__mutmut_4(self, tree: BSTNode=None):
        if not tree:
            tree = self.root
            if not tree:
                return 1
        leftbranch = 0 if not tree.left else tree.left.height
        rightbranch = 0 if not tree.right else tree.right.height
        return leftbranch - rightbranch

    def xǁBstǁbalance__mutmut_5(self, tree: BSTNode=None):
        if not tree:
            tree = self.root
            if not tree:
                return 0
        leftbranch = None
        rightbranch = 0 if not tree.right else tree.right.height
        return leftbranch - rightbranch

    def xǁBstǁbalance__mutmut_6(self, tree: BSTNode=None):
        if not tree:
            tree = self.root
            if not tree:
                return 0
        leftbranch = 1 if not tree.left else tree.left.height
        rightbranch = 0 if not tree.right else tree.right.height
        return leftbranch - rightbranch

    def xǁBstǁbalance__mutmut_7(self, tree: BSTNode=None):
        if not tree:
            tree = self.root
            if not tree:
                return 0
        leftbranch = 0 if tree.left else tree.left.height
        rightbranch = 0 if not tree.right else tree.right.height
        return leftbranch - rightbranch

    def xǁBstǁbalance__mutmut_8(self, tree: BSTNode=None):
        if not tree:
            tree = self.root
            if not tree:
                return 0
        leftbranch = 0 if not tree.left else tree.left.height
        rightbranch = None
        return leftbranch - rightbranch

    def xǁBstǁbalance__mutmut_9(self, tree: BSTNode=None):
        if not tree:
            tree = self.root
            if not tree:
                return 0
        leftbranch = 0 if not tree.left else tree.left.height
        rightbranch = 1 if not tree.right else tree.right.height
        return leftbranch - rightbranch

    def xǁBstǁbalance__mutmut_10(self, tree: BSTNode=None):
        if not tree:
            tree = self.root
            if not tree:
                return 0
        leftbranch = 0 if not tree.left else tree.left.height
        rightbranch = 0 if tree.right else tree.right.height
        return leftbranch - rightbranch

    def xǁBstǁbalance__mutmut_11(self, tree: BSTNode=None):
        if not tree:
            tree = self.root
            if not tree:
                return 0
        leftbranch = 0 if not tree.left else tree.left.height
        rightbranch = 0 if not tree.right else tree.right.height
        return leftbranch + rightbranch
    
    xǁBstǁbalance__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁbalance__mutmut_1': xǁBstǁbalance__mutmut_1, 
        'xǁBstǁbalance__mutmut_2': xǁBstǁbalance__mutmut_2, 
        'xǁBstǁbalance__mutmut_3': xǁBstǁbalance__mutmut_3, 
        'xǁBstǁbalance__mutmut_4': xǁBstǁbalance__mutmut_4, 
        'xǁBstǁbalance__mutmut_5': xǁBstǁbalance__mutmut_5, 
        'xǁBstǁbalance__mutmut_6': xǁBstǁbalance__mutmut_6, 
        'xǁBstǁbalance__mutmut_7': xǁBstǁbalance__mutmut_7, 
        'xǁBstǁbalance__mutmut_8': xǁBstǁbalance__mutmut_8, 
        'xǁBstǁbalance__mutmut_9': xǁBstǁbalance__mutmut_9, 
        'xǁBstǁbalance__mutmut_10': xǁBstǁbalance__mutmut_10, 
        'xǁBstǁbalance__mutmut_11': xǁBstǁbalance__mutmut_11
    }
    
    def balance(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁbalance__mutmut_orig"), object.__getattribute__(self, "xǁBstǁbalance__mutmut_mutants"), args, kwargs, self)
        return result 
    
    balance.__signature__ = _mutmut_signature(xǁBstǁbalance__mutmut_orig)
    xǁBstǁbalance__mutmut_orig.__name__ = 'xǁBstǁbalance'

    def xǁBstǁpre_order__mutmut_orig(self):
        return self._pre_order(self.root)

    def xǁBstǁpre_order__mutmut_1(self):
        return self._pre_order(None)
    
    xǁBstǁpre_order__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁpre_order__mutmut_1': xǁBstǁpre_order__mutmut_1
    }
    
    def pre_order(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁpre_order__mutmut_orig"), object.__getattribute__(self, "xǁBstǁpre_order__mutmut_mutants"), args, kwargs, self)
        return result 
    
    pre_order.__signature__ = _mutmut_signature(xǁBstǁpre_order__mutmut_orig)
    xǁBstǁpre_order__mutmut_orig.__name__ = 'xǁBstǁpre_order'

    def xǁBstǁ_pre_order__mutmut_orig(self, node: BSTNode):
        if not node:
            return
        yield node.val
        yield from self._pre_order(node.left)
        yield from self._pre_order(node.right)

    def xǁBstǁ_pre_order__mutmut_1(self, node: BSTNode):
        if node:
            return
        yield node.val
        yield from self._pre_order(node.left)
        yield from self._pre_order(node.right)

    def xǁBstǁ_pre_order__mutmut_2(self, node: BSTNode):
        if not node:
            return
        yield node.val
        yield from self._pre_order(None)
        yield from self._pre_order(node.right)

    def xǁBstǁ_pre_order__mutmut_3(self, node: BSTNode):
        if not node:
            return
        yield node.val
        yield from self._pre_order(node.left)
        yield from self._pre_order(None)
    
    xǁBstǁ_pre_order__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁ_pre_order__mutmut_1': xǁBstǁ_pre_order__mutmut_1, 
        'xǁBstǁ_pre_order__mutmut_2': xǁBstǁ_pre_order__mutmut_2, 
        'xǁBstǁ_pre_order__mutmut_3': xǁBstǁ_pre_order__mutmut_3
    }
    
    def _pre_order(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁ_pre_order__mutmut_orig"), object.__getattribute__(self, "xǁBstǁ_pre_order__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _pre_order.__signature__ = _mutmut_signature(xǁBstǁ_pre_order__mutmut_orig)
    xǁBstǁ_pre_order__mutmut_orig.__name__ = 'xǁBstǁ_pre_order'

    def xǁBstǁin_order__mutmut_orig(self):
        return self._in_order(self.root)

    def xǁBstǁin_order__mutmut_1(self):
        return self._in_order(None)
    
    xǁBstǁin_order__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁin_order__mutmut_1': xǁBstǁin_order__mutmut_1
    }
    
    def in_order(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁin_order__mutmut_orig"), object.__getattribute__(self, "xǁBstǁin_order__mutmut_mutants"), args, kwargs, self)
        return result 
    
    in_order.__signature__ = _mutmut_signature(xǁBstǁin_order__mutmut_orig)
    xǁBstǁin_order__mutmut_orig.__name__ = 'xǁBstǁin_order'

    def xǁBstǁ_in_order__mutmut_orig(self, node: BSTNode):
        if not node:
            return
        yield from self._in_order(node.left)
        yield node.val
        yield from self._in_order(node.right)

    def xǁBstǁ_in_order__mutmut_1(self, node: BSTNode):
        if node:
            return
        yield from self._in_order(node.left)
        yield node.val
        yield from self._in_order(node.right)

    def xǁBstǁ_in_order__mutmut_2(self, node: BSTNode):
        if not node:
            return
        yield from self._in_order(None)
        yield node.val
        yield from self._in_order(node.right)

    def xǁBstǁ_in_order__mutmut_3(self, node: BSTNode):
        if not node:
            return
        yield from self._in_order(node.left)
        yield node.val
        yield from self._in_order(None)
    
    xǁBstǁ_in_order__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁ_in_order__mutmut_1': xǁBstǁ_in_order__mutmut_1, 
        'xǁBstǁ_in_order__mutmut_2': xǁBstǁ_in_order__mutmut_2, 
        'xǁBstǁ_in_order__mutmut_3': xǁBstǁ_in_order__mutmut_3
    }
    
    def _in_order(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁ_in_order__mutmut_orig"), object.__getattribute__(self, "xǁBstǁ_in_order__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _in_order.__signature__ = _mutmut_signature(xǁBstǁ_in_order__mutmut_orig)
    xǁBstǁ_in_order__mutmut_orig.__name__ = 'xǁBstǁ_in_order'

    def xǁBstǁpost_order__mutmut_orig(self):
        return self._post_order(self.root)

    def xǁBstǁpost_order__mutmut_1(self):
        return self._post_order(None)
    
    xǁBstǁpost_order__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁpost_order__mutmut_1': xǁBstǁpost_order__mutmut_1
    }
    
    def post_order(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁpost_order__mutmut_orig"), object.__getattribute__(self, "xǁBstǁpost_order__mutmut_mutants"), args, kwargs, self)
        return result 
    
    post_order.__signature__ = _mutmut_signature(xǁBstǁpost_order__mutmut_orig)
    xǁBstǁpost_order__mutmut_orig.__name__ = 'xǁBstǁpost_order'

    def xǁBstǁ_post_order__mutmut_orig(self, node: BSTNode):
        if not node:
            return
        yield from self._post_order(node.left)
        yield from self._post_order(node.right)
        yield node.val

    def xǁBstǁ_post_order__mutmut_1(self, node: BSTNode):
        if node:
            return
        yield from self._post_order(node.left)
        yield from self._post_order(node.right)
        yield node.val

    def xǁBstǁ_post_order__mutmut_2(self, node: BSTNode):
        if not node:
            return
        yield from self._post_order(None)
        yield from self._post_order(node.right)
        yield node.val

    def xǁBstǁ_post_order__mutmut_3(self, node: BSTNode):
        if not node:
            return
        yield from self._post_order(node.left)
        yield from self._post_order(None)
        yield node.val
    
    xǁBstǁ_post_order__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁ_post_order__mutmut_1': xǁBstǁ_post_order__mutmut_1, 
        'xǁBstǁ_post_order__mutmut_2': xǁBstǁ_post_order__mutmut_2, 
        'xǁBstǁ_post_order__mutmut_3': xǁBstǁ_post_order__mutmut_3
    }
    
    def _post_order(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁ_post_order__mutmut_orig"), object.__getattribute__(self, "xǁBstǁ_post_order__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _post_order.__signature__ = _mutmut_signature(xǁBstǁ_post_order__mutmut_orig)
    xǁBstǁ_post_order__mutmut_orig.__name__ = 'xǁBstǁ_post_order'

    def xǁBstǁbreadth_first__mutmut_orig(self):
        q = Queue()
        q.enqueue(self.root)
        while q.peek():
            node = q.dequeue()
            yield node.val
            if node.left:
                q.enqueue(node.left)
            if node.right:
                q.enqueue(node.right)

    def xǁBstǁbreadth_first__mutmut_1(self):
        q = None
        q.enqueue(self.root)
        while q.peek():
            node = q.dequeue()
            yield node.val
            if node.left:
                q.enqueue(node.left)
            if node.right:
                q.enqueue(node.right)

    def xǁBstǁbreadth_first__mutmut_2(self):
        q = Queue()
        q.enqueue(None)
        while q.peek():
            node = q.dequeue()
            yield node.val
            if node.left:
                q.enqueue(node.left)
            if node.right:
                q.enqueue(node.right)

    def xǁBstǁbreadth_first__mutmut_3(self):
        q = Queue()
        q.enqueue(self.root)
        while q.peek():
            node = None
            yield node.val
            if node.left:
                q.enqueue(node.left)
            if node.right:
                q.enqueue(node.right)

    def xǁBstǁbreadth_first__mutmut_4(self):
        q = Queue()
        q.enqueue(self.root)
        while q.peek():
            node = q.dequeue()
            yield node.val
            if node.left:
                q.enqueue(None)
            if node.right:
                q.enqueue(node.right)

    def xǁBstǁbreadth_first__mutmut_5(self):
        q = Queue()
        q.enqueue(self.root)
        while q.peek():
            node = q.dequeue()
            yield node.val
            if node.left:
                q.enqueue(node.left)
            if node.right:
                q.enqueue(None)
    
    xǁBstǁbreadth_first__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁbreadth_first__mutmut_1': xǁBstǁbreadth_first__mutmut_1, 
        'xǁBstǁbreadth_first__mutmut_2': xǁBstǁbreadth_first__mutmut_2, 
        'xǁBstǁbreadth_first__mutmut_3': xǁBstǁbreadth_first__mutmut_3, 
        'xǁBstǁbreadth_first__mutmut_4': xǁBstǁbreadth_first__mutmut_4, 
        'xǁBstǁbreadth_first__mutmut_5': xǁBstǁbreadth_first__mutmut_5
    }
    
    def breadth_first(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁbreadth_first__mutmut_orig"), object.__getattribute__(self, "xǁBstǁbreadth_first__mutmut_mutants"), args, kwargs, self)
        return result 
    
    breadth_first.__signature__ = _mutmut_signature(xǁBstǁbreadth_first__mutmut_orig)
    xǁBstǁbreadth_first__mutmut_orig.__name__ = 'xǁBstǁbreadth_first'

    def xǁBstǁdelete__mutmut_orig(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_1(self, val):
        if self._size < 1 and not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_2(self, val):
        if self._size <= 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_3(self, val):
        if self._size < 2 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_4(self, val):
        if self._size < 1 or self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_5(self, val):
        if self._size < 1 or not self.contains(None):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_6(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = None

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_7(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(None)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_8(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(None, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_9(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, None, None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_10(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_11(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_12(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), )
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_13(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = ""

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_14(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = None
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_15(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(None)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_16(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size = 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_17(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size -= 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_18(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 2
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_19(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(None)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_20(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = None

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_21(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = None
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_22(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(None, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_23(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, None)
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_24(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_25(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, )
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_26(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = None
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_27(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(None, node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_28(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, None, child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_29(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), None)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_30(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node._side(), child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_31(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, child)
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_32(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), )
            else:
                self.root = child

        self._size -= 1

    def xǁBstǁdelete__mutmut_33(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = None

        self._size -= 1

    def xǁBstǁdelete__mutmut_34(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size = 1

    def xǁBstǁdelete__mutmut_35(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size += 1

    def xǁBstǁdelete__mutmut_36(self, val):
        if self._size < 1 or not self.contains(val):
            return

        node = self.search(val)

        if node._is_leaf():
            if node.parent:
                setattr(node.parent, node._side(), None)
            else:
                self.root = None

        elif node._is_interior():
            next_node = self._find_replacement(node)
            self._size += 1
            self.delete(next_node.val)
            node.val = next_node.val

        else:
            child = getattr(node, node._onlychild())
            if node.parent:
                child.parent = node.parent
                setattr(node.parent, node._side(), child)
            else:
                self.root = child

        self._size -= 2
    
    xǁBstǁdelete__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁdelete__mutmut_1': xǁBstǁdelete__mutmut_1, 
        'xǁBstǁdelete__mutmut_2': xǁBstǁdelete__mutmut_2, 
        'xǁBstǁdelete__mutmut_3': xǁBstǁdelete__mutmut_3, 
        'xǁBstǁdelete__mutmut_4': xǁBstǁdelete__mutmut_4, 
        'xǁBstǁdelete__mutmut_5': xǁBstǁdelete__mutmut_5, 
        'xǁBstǁdelete__mutmut_6': xǁBstǁdelete__mutmut_6, 
        'xǁBstǁdelete__mutmut_7': xǁBstǁdelete__mutmut_7, 
        'xǁBstǁdelete__mutmut_8': xǁBstǁdelete__mutmut_8, 
        'xǁBstǁdelete__mutmut_9': xǁBstǁdelete__mutmut_9, 
        'xǁBstǁdelete__mutmut_10': xǁBstǁdelete__mutmut_10, 
        'xǁBstǁdelete__mutmut_11': xǁBstǁdelete__mutmut_11, 
        'xǁBstǁdelete__mutmut_12': xǁBstǁdelete__mutmut_12, 
        'xǁBstǁdelete__mutmut_13': xǁBstǁdelete__mutmut_13, 
        'xǁBstǁdelete__mutmut_14': xǁBstǁdelete__mutmut_14, 
        'xǁBstǁdelete__mutmut_15': xǁBstǁdelete__mutmut_15, 
        'xǁBstǁdelete__mutmut_16': xǁBstǁdelete__mutmut_16, 
        'xǁBstǁdelete__mutmut_17': xǁBstǁdelete__mutmut_17, 
        'xǁBstǁdelete__mutmut_18': xǁBstǁdelete__mutmut_18, 
        'xǁBstǁdelete__mutmut_19': xǁBstǁdelete__mutmut_19, 
        'xǁBstǁdelete__mutmut_20': xǁBstǁdelete__mutmut_20, 
        'xǁBstǁdelete__mutmut_21': xǁBstǁdelete__mutmut_21, 
        'xǁBstǁdelete__mutmut_22': xǁBstǁdelete__mutmut_22, 
        'xǁBstǁdelete__mutmut_23': xǁBstǁdelete__mutmut_23, 
        'xǁBstǁdelete__mutmut_24': xǁBstǁdelete__mutmut_24, 
        'xǁBstǁdelete__mutmut_25': xǁBstǁdelete__mutmut_25, 
        'xǁBstǁdelete__mutmut_26': xǁBstǁdelete__mutmut_26, 
        'xǁBstǁdelete__mutmut_27': xǁBstǁdelete__mutmut_27, 
        'xǁBstǁdelete__mutmut_28': xǁBstǁdelete__mutmut_28, 
        'xǁBstǁdelete__mutmut_29': xǁBstǁdelete__mutmut_29, 
        'xǁBstǁdelete__mutmut_30': xǁBstǁdelete__mutmut_30, 
        'xǁBstǁdelete__mutmut_31': xǁBstǁdelete__mutmut_31, 
        'xǁBstǁdelete__mutmut_32': xǁBstǁdelete__mutmut_32, 
        'xǁBstǁdelete__mutmut_33': xǁBstǁdelete__mutmut_33, 
        'xǁBstǁdelete__mutmut_34': xǁBstǁdelete__mutmut_34, 
        'xǁBstǁdelete__mutmut_35': xǁBstǁdelete__mutmut_35, 
        'xǁBstǁdelete__mutmut_36': xǁBstǁdelete__mutmut_36
    }
    
    def delete(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁdelete__mutmut_orig"), object.__getattribute__(self, "xǁBstǁdelete__mutmut_mutants"), args, kwargs, self)
        return result 
    
    delete.__signature__ = _mutmut_signature(xǁBstǁdelete__mutmut_orig)
    xǁBstǁdelete__mutmut_orig.__name__ = 'xǁBstǁdelete'

    def xǁBstǁ_find_replacement__mutmut_orig(self, node: BSTNode):
        return self._findmin(node.right)

    def xǁBstǁ_find_replacement__mutmut_1(self, node: BSTNode):
        return self._findmin(None)
    
    xǁBstǁ_find_replacement__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁ_find_replacement__mutmut_1': xǁBstǁ_find_replacement__mutmut_1
    }
    
    def _find_replacement(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁ_find_replacement__mutmut_orig"), object.__getattribute__(self, "xǁBstǁ_find_replacement__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _find_replacement.__signature__ = _mutmut_signature(xǁBstǁ_find_replacement__mutmut_orig)
    xǁBstǁ_find_replacement__mutmut_orig.__name__ = 'xǁBstǁ_find_replacement'


    def xǁBstǁ_findmin__mutmut_orig(self, node: BSTNode):
        while node.left:
            node = node.left
        return node


    def xǁBstǁ_findmin__mutmut_1(self, node: BSTNode):
        while node.left:
            node = None
        return node
    
    xǁBstǁ_findmin__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBstǁ_findmin__mutmut_1': xǁBstǁ_findmin__mutmut_1
    }
    
    def _findmin(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBstǁ_findmin__mutmut_orig"), object.__getattribute__(self, "xǁBstǁ_findmin__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _findmin.__signature__ = _mutmut_signature(xǁBstǁ_findmin__mutmut_orig)
    xǁBstǁ_findmin__mutmut_orig.__name__ = 'xǁBstǁ_findmin'