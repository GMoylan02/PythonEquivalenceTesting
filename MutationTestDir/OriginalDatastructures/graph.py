class Graph(object):

    def __init__(self, data=None):
        self.graph = {}
        if data:
            for i in data:
                self.add_node(i)

    def nodes(self):
        return list(self.graph.keys())

    def edges(self):
        return [(n, edge) for n, edges in self.graph.items() for edge in edges]

    def add_node(self, n):
        self.graph.setdefault(n, set())

    def add_edge(self, n1, n2):
        self.graph.setdefault(n1, set())
        self.graph.setdefault(n2, set())
        self.graph[n1].add(n2)

    def del_node(self, n):
        if n not in self.graph:
            raise ValueError(f'{n} is not in the graph')
        del self.graph[n]
        for k in self.graph:
            self.graph[k].discard(n)

    def del_edge(self, n1, n2):
        if n1 not in self.graph or n2 not in self.graph[n1]:
            raise ValueError('Edge does not exist')
        self.graph[n1].remove(n2)

    def has_node(self, n):
        return n in self.graph

    def neighbors(self, n):
        if n not in self.graph:
            raise ValueError(f'{n} is not in the graph')
        return self.graph[n]

    def adjacent(self, n1, n2):
        if n1 not in self.graph or n2 not in self.graph:
            raise ValueError('One or both nodes not in graph')
        return n2 in self.graph[n1]
