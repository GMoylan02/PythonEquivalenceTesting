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
class Graph(object):

    def xǁGraphǁ__init____mutmut_orig(self, data=None):
        self.graph = {}
        if data:
            for i in data:
                self.add_node(i)

    def xǁGraphǁ__init____mutmut_1(self, data=None):
        self.graph = None
        if data:
            for i in data:
                self.add_node(i)

    def xǁGraphǁ__init____mutmut_2(self, data=None):
        self.graph = {}
        if data:
            for i in data:
                self.add_node(None)
    
    xǁGraphǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGraphǁ__init____mutmut_1': xǁGraphǁ__init____mutmut_1, 
        'xǁGraphǁ__init____mutmut_2': xǁGraphǁ__init____mutmut_2
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGraphǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁGraphǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁGraphǁ__init____mutmut_orig)
    xǁGraphǁ__init____mutmut_orig.__name__ = 'xǁGraphǁ__init__'

    def xǁGraphǁnodes__mutmut_orig(self):
        return list(self.graph.keys())

    def xǁGraphǁnodes__mutmut_1(self):
        return list(None)
    
    xǁGraphǁnodes__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGraphǁnodes__mutmut_1': xǁGraphǁnodes__mutmut_1
    }
    
    def nodes(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGraphǁnodes__mutmut_orig"), object.__getattribute__(self, "xǁGraphǁnodes__mutmut_mutants"), args, kwargs, self)
        return result 
    
    nodes.__signature__ = _mutmut_signature(xǁGraphǁnodes__mutmut_orig)
    xǁGraphǁnodes__mutmut_orig.__name__ = 'xǁGraphǁnodes'

    def edges(self):
        return [(n, edge) for n, edges in self.graph.items() for edge in edges]

    def xǁGraphǁadd_node__mutmut_orig(self, n):
        self.graph.setdefault(n, set())

    def xǁGraphǁadd_node__mutmut_1(self, n):
        self.graph.setdefault(None, set())

    def xǁGraphǁadd_node__mutmut_2(self, n):
        self.graph.setdefault(n, None)

    def xǁGraphǁadd_node__mutmut_3(self, n):
        self.graph.setdefault(set())

    def xǁGraphǁadd_node__mutmut_4(self, n):
        self.graph.setdefault(n, )
    
    xǁGraphǁadd_node__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGraphǁadd_node__mutmut_1': xǁGraphǁadd_node__mutmut_1, 
        'xǁGraphǁadd_node__mutmut_2': xǁGraphǁadd_node__mutmut_2, 
        'xǁGraphǁadd_node__mutmut_3': xǁGraphǁadd_node__mutmut_3, 
        'xǁGraphǁadd_node__mutmut_4': xǁGraphǁadd_node__mutmut_4
    }
    
    def add_node(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGraphǁadd_node__mutmut_orig"), object.__getattribute__(self, "xǁGraphǁadd_node__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_node.__signature__ = _mutmut_signature(xǁGraphǁadd_node__mutmut_orig)
    xǁGraphǁadd_node__mutmut_orig.__name__ = 'xǁGraphǁadd_node'

    def xǁGraphǁadd_edge__mutmut_orig(self, n1, n2):
        self.graph.setdefault(n1, set())
        self.graph.setdefault(n2, set())
        self.graph[n1].add(n2)

    def xǁGraphǁadd_edge__mutmut_1(self, n1, n2):
        self.graph.setdefault(None, set())
        self.graph.setdefault(n2, set())
        self.graph[n1].add(n2)

    def xǁGraphǁadd_edge__mutmut_2(self, n1, n2):
        self.graph.setdefault(n1, None)
        self.graph.setdefault(n2, set())
        self.graph[n1].add(n2)

    def xǁGraphǁadd_edge__mutmut_3(self, n1, n2):
        self.graph.setdefault(set())
        self.graph.setdefault(n2, set())
        self.graph[n1].add(n2)

    def xǁGraphǁadd_edge__mutmut_4(self, n1, n2):
        self.graph.setdefault(n1, )
        self.graph.setdefault(n2, set())
        self.graph[n1].add(n2)

    def xǁGraphǁadd_edge__mutmut_5(self, n1, n2):
        self.graph.setdefault(n1, set())
        self.graph.setdefault(None, set())
        self.graph[n1].add(n2)

    def xǁGraphǁadd_edge__mutmut_6(self, n1, n2):
        self.graph.setdefault(n1, set())
        self.graph.setdefault(n2, None)
        self.graph[n1].add(n2)

    def xǁGraphǁadd_edge__mutmut_7(self, n1, n2):
        self.graph.setdefault(n1, set())
        self.graph.setdefault(set())
        self.graph[n1].add(n2)

    def xǁGraphǁadd_edge__mutmut_8(self, n1, n2):
        self.graph.setdefault(n1, set())
        self.graph.setdefault(n2, )
        self.graph[n1].add(n2)

    def xǁGraphǁadd_edge__mutmut_9(self, n1, n2):
        self.graph.setdefault(n1, set())
        self.graph.setdefault(n2, set())
        self.graph[n1].add(None)
    
    xǁGraphǁadd_edge__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGraphǁadd_edge__mutmut_1': xǁGraphǁadd_edge__mutmut_1, 
        'xǁGraphǁadd_edge__mutmut_2': xǁGraphǁadd_edge__mutmut_2, 
        'xǁGraphǁadd_edge__mutmut_3': xǁGraphǁadd_edge__mutmut_3, 
        'xǁGraphǁadd_edge__mutmut_4': xǁGraphǁadd_edge__mutmut_4, 
        'xǁGraphǁadd_edge__mutmut_5': xǁGraphǁadd_edge__mutmut_5, 
        'xǁGraphǁadd_edge__mutmut_6': xǁGraphǁadd_edge__mutmut_6, 
        'xǁGraphǁadd_edge__mutmut_7': xǁGraphǁadd_edge__mutmut_7, 
        'xǁGraphǁadd_edge__mutmut_8': xǁGraphǁadd_edge__mutmut_8, 
        'xǁGraphǁadd_edge__mutmut_9': xǁGraphǁadd_edge__mutmut_9
    }
    
    def add_edge(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGraphǁadd_edge__mutmut_orig"), object.__getattribute__(self, "xǁGraphǁadd_edge__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_edge.__signature__ = _mutmut_signature(xǁGraphǁadd_edge__mutmut_orig)
    xǁGraphǁadd_edge__mutmut_orig.__name__ = 'xǁGraphǁadd_edge'

    def xǁGraphǁdel_node__mutmut_orig(self, n):
        if n not in self.graph:
            raise ValueError(f'{n} is not in the graph')
        del self.graph[n]
        for k in self.graph:
            self.graph[k].discard(n)

    def xǁGraphǁdel_node__mutmut_1(self, n):
        if n in self.graph:
            raise ValueError(f'{n} is not in the graph')
        del self.graph[n]
        for k in self.graph:
            self.graph[k].discard(n)

    def xǁGraphǁdel_node__mutmut_2(self, n):
        if n not in self.graph:
            raise ValueError(None)
        del self.graph[n]
        for k in self.graph:
            self.graph[k].discard(n)

    def xǁGraphǁdel_node__mutmut_3(self, n):
        if n not in self.graph:
            raise ValueError(f'{n} is not in the graph')
        del self.graph[n]
        for k in self.graph:
            self.graph[k].discard(None)
    
    xǁGraphǁdel_node__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGraphǁdel_node__mutmut_1': xǁGraphǁdel_node__mutmut_1, 
        'xǁGraphǁdel_node__mutmut_2': xǁGraphǁdel_node__mutmut_2, 
        'xǁGraphǁdel_node__mutmut_3': xǁGraphǁdel_node__mutmut_3
    }
    
    def del_node(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGraphǁdel_node__mutmut_orig"), object.__getattribute__(self, "xǁGraphǁdel_node__mutmut_mutants"), args, kwargs, self)
        return result 
    
    del_node.__signature__ = _mutmut_signature(xǁGraphǁdel_node__mutmut_orig)
    xǁGraphǁdel_node__mutmut_orig.__name__ = 'xǁGraphǁdel_node'

    def xǁGraphǁdel_edge__mutmut_orig(self, n1, n2):
        if n1 not in self.graph or n2 not in self.graph[n1]:
            raise ValueError('Edge does not exist')
        self.graph[n1].remove(n2)

    def xǁGraphǁdel_edge__mutmut_1(self, n1, n2):
        if n1 not in self.graph and n2 not in self.graph[n1]:
            raise ValueError('Edge does not exist')
        self.graph[n1].remove(n2)

    def xǁGraphǁdel_edge__mutmut_2(self, n1, n2):
        if n1 in self.graph or n2 not in self.graph[n1]:
            raise ValueError('Edge does not exist')
        self.graph[n1].remove(n2)

    def xǁGraphǁdel_edge__mutmut_3(self, n1, n2):
        if n1 not in self.graph or n2 in self.graph[n1]:
            raise ValueError('Edge does not exist')
        self.graph[n1].remove(n2)

    def xǁGraphǁdel_edge__mutmut_4(self, n1, n2):
        if n1 not in self.graph or n2 not in self.graph[n1]:
            raise ValueError(None)
        self.graph[n1].remove(n2)

    def xǁGraphǁdel_edge__mutmut_5(self, n1, n2):
        if n1 not in self.graph or n2 not in self.graph[n1]:
            raise ValueError('XXEdge does not existXX')
        self.graph[n1].remove(n2)

    def xǁGraphǁdel_edge__mutmut_6(self, n1, n2):
        if n1 not in self.graph or n2 not in self.graph[n1]:
            raise ValueError('edge does not exist')
        self.graph[n1].remove(n2)

    def xǁGraphǁdel_edge__mutmut_7(self, n1, n2):
        if n1 not in self.graph or n2 not in self.graph[n1]:
            raise ValueError('EDGE DOES NOT EXIST')
        self.graph[n1].remove(n2)

    def xǁGraphǁdel_edge__mutmut_8(self, n1, n2):
        if n1 not in self.graph or n2 not in self.graph[n1]:
            raise ValueError('Edge does not exist')
        self.graph[n1].remove(None)
    
    xǁGraphǁdel_edge__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGraphǁdel_edge__mutmut_1': xǁGraphǁdel_edge__mutmut_1, 
        'xǁGraphǁdel_edge__mutmut_2': xǁGraphǁdel_edge__mutmut_2, 
        'xǁGraphǁdel_edge__mutmut_3': xǁGraphǁdel_edge__mutmut_3, 
        'xǁGraphǁdel_edge__mutmut_4': xǁGraphǁdel_edge__mutmut_4, 
        'xǁGraphǁdel_edge__mutmut_5': xǁGraphǁdel_edge__mutmut_5, 
        'xǁGraphǁdel_edge__mutmut_6': xǁGraphǁdel_edge__mutmut_6, 
        'xǁGraphǁdel_edge__mutmut_7': xǁGraphǁdel_edge__mutmut_7, 
        'xǁGraphǁdel_edge__mutmut_8': xǁGraphǁdel_edge__mutmut_8
    }
    
    def del_edge(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGraphǁdel_edge__mutmut_orig"), object.__getattribute__(self, "xǁGraphǁdel_edge__mutmut_mutants"), args, kwargs, self)
        return result 
    
    del_edge.__signature__ = _mutmut_signature(xǁGraphǁdel_edge__mutmut_orig)
    xǁGraphǁdel_edge__mutmut_orig.__name__ = 'xǁGraphǁdel_edge'

    def xǁGraphǁhas_node__mutmut_orig(self, n):
        return n in self.graph

    def xǁGraphǁhas_node__mutmut_1(self, n):
        return n not in self.graph
    
    xǁGraphǁhas_node__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGraphǁhas_node__mutmut_1': xǁGraphǁhas_node__mutmut_1
    }
    
    def has_node(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGraphǁhas_node__mutmut_orig"), object.__getattribute__(self, "xǁGraphǁhas_node__mutmut_mutants"), args, kwargs, self)
        return result 
    
    has_node.__signature__ = _mutmut_signature(xǁGraphǁhas_node__mutmut_orig)
    xǁGraphǁhas_node__mutmut_orig.__name__ = 'xǁGraphǁhas_node'

    def xǁGraphǁneighbors__mutmut_orig(self, n):
        if n not in self.graph:
            raise ValueError(f'{n} is not in the graph')
        return self.graph[n]

    def xǁGraphǁneighbors__mutmut_1(self, n):
        if n in self.graph:
            raise ValueError(f'{n} is not in the graph')
        return self.graph[n]

    def xǁGraphǁneighbors__mutmut_2(self, n):
        if n not in self.graph:
            raise ValueError(None)
        return self.graph[n]
    
    xǁGraphǁneighbors__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGraphǁneighbors__mutmut_1': xǁGraphǁneighbors__mutmut_1, 
        'xǁGraphǁneighbors__mutmut_2': xǁGraphǁneighbors__mutmut_2
    }
    
    def neighbors(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGraphǁneighbors__mutmut_orig"), object.__getattribute__(self, "xǁGraphǁneighbors__mutmut_mutants"), args, kwargs, self)
        return result 
    
    neighbors.__signature__ = _mutmut_signature(xǁGraphǁneighbors__mutmut_orig)
    xǁGraphǁneighbors__mutmut_orig.__name__ = 'xǁGraphǁneighbors'

    def xǁGraphǁadjacent__mutmut_orig(self, n1, n2):
        if n1 not in self.graph or n2 not in self.graph:
            raise ValueError('One or both nodes not in graph')
        return n2 in self.graph[n1]

    def xǁGraphǁadjacent__mutmut_1(self, n1, n2):
        if n1 not in self.graph and n2 not in self.graph:
            raise ValueError('One or both nodes not in graph')
        return n2 in self.graph[n1]

    def xǁGraphǁadjacent__mutmut_2(self, n1, n2):
        if n1 in self.graph or n2 not in self.graph:
            raise ValueError('One or both nodes not in graph')
        return n2 in self.graph[n1]

    def xǁGraphǁadjacent__mutmut_3(self, n1, n2):
        if n1 not in self.graph or n2 in self.graph:
            raise ValueError('One or both nodes not in graph')
        return n2 in self.graph[n1]

    def xǁGraphǁadjacent__mutmut_4(self, n1, n2):
        if n1 not in self.graph or n2 not in self.graph:
            raise ValueError(None)
        return n2 in self.graph[n1]

    def xǁGraphǁadjacent__mutmut_5(self, n1, n2):
        if n1 not in self.graph or n2 not in self.graph:
            raise ValueError('XXOne or both nodes not in graphXX')
        return n2 in self.graph[n1]

    def xǁGraphǁadjacent__mutmut_6(self, n1, n2):
        if n1 not in self.graph or n2 not in self.graph:
            raise ValueError('one or both nodes not in graph')
        return n2 in self.graph[n1]

    def xǁGraphǁadjacent__mutmut_7(self, n1, n2):
        if n1 not in self.graph or n2 not in self.graph:
            raise ValueError('ONE OR BOTH NODES NOT IN GRAPH')
        return n2 in self.graph[n1]

    def xǁGraphǁadjacent__mutmut_8(self, n1, n2):
        if n1 not in self.graph or n2 not in self.graph:
            raise ValueError('One or both nodes not in graph')
        return n2 not in self.graph[n1]
    
    xǁGraphǁadjacent__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁGraphǁadjacent__mutmut_1': xǁGraphǁadjacent__mutmut_1, 
        'xǁGraphǁadjacent__mutmut_2': xǁGraphǁadjacent__mutmut_2, 
        'xǁGraphǁadjacent__mutmut_3': xǁGraphǁadjacent__mutmut_3, 
        'xǁGraphǁadjacent__mutmut_4': xǁGraphǁadjacent__mutmut_4, 
        'xǁGraphǁadjacent__mutmut_5': xǁGraphǁadjacent__mutmut_5, 
        'xǁGraphǁadjacent__mutmut_6': xǁGraphǁadjacent__mutmut_6, 
        'xǁGraphǁadjacent__mutmut_7': xǁGraphǁadjacent__mutmut_7, 
        'xǁGraphǁadjacent__mutmut_8': xǁGraphǁadjacent__mutmut_8
    }
    
    def adjacent(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁGraphǁadjacent__mutmut_orig"), object.__getattribute__(self, "xǁGraphǁadjacent__mutmut_mutants"), args, kwargs, self)
        return result 
    
    adjacent.__signature__ = _mutmut_signature(xǁGraphǁadjacent__mutmut_orig)
    xǁGraphǁadjacent__mutmut_orig.__name__ = 'xǁGraphǁadjacent'
