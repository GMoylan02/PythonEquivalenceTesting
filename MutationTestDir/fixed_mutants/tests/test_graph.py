import pytest


@pytest.fixture
def empty_graph():
    from graph import Graph
    return Graph()


@pytest.fixture
def one_graph():
    from graph import Graph
    return Graph(['A'])


@pytest.fixture
def multi_graph():
    from graph import Graph
    return Graph(['A', 'B', 'C', 'D', 'E'])


def test_nodes_empty(empty_graph):
    assert empty_graph.nodes() == []


def test_nodes_one(one_graph):
    assert one_graph.nodes() == ['A']


def test_nodes_graph(multi_graph):
    assert sorted(multi_graph.nodes()) == ['A', 'B', 'C', 'D', 'E']


def test_add_node(empty_graph):
    empty_graph.add_node('A')
    assert empty_graph.nodes() == ['A']


def test_add_node_no_duplicate(one_graph):
    one_graph.add_node('A')
    assert one_graph.nodes() == ['A']


def test_add_edge_known_nodes(multi_graph):
    multi_graph.add_edge('A', 'B')
    assert multi_graph.graph['A'] == {'B'}


def test_add_edge_new_nodes(empty_graph):
    empty_graph.add_edge('A', 'B')
    assert empty_graph.graph == {'A': {'B'}, 'B': set()}


def test_edges_empty(empty_graph):
    assert empty_graph.edges() == []


def test_edges_returns_tuples(multi_graph):
    multi_graph.add_edge('A', 'B')
    multi_graph.add_edge('A', 'C')
    assert sorted(multi_graph.edges()) == [('A', 'B'), ('A', 'C')]


def test_edges_multiple_nodes(multi_graph):
    multi_graph.add_edge('A', 'B')
    multi_graph.add_edge('B', 'C')
    assert sorted(multi_graph.edges()) == [('A', 'B'), ('B', 'C')]


def test_del_edge(multi_graph):
    multi_graph.add_edge('A', 'B')
    multi_graph.del_edge('A', 'B')
    assert multi_graph.edges() == []


def test_del_edge_missing_raises(empty_graph):
    with pytest.raises(ValueError):
        empty_graph.del_edge('A', 'B')


def test_has_node_true(multi_graph):
    assert multi_graph.has_node('A')


def test_has_node_false(empty_graph):
    assert not empty_graph.has_node('A')


def test_neighbors_returns_connected(multi_graph):
    multi_graph.add_edge('A', 'B')
    assert multi_graph.neighbors('A') == {'B'}


def test_neighbors_empty(multi_graph):
    assert multi_graph.neighbors('A') == set()


def test_neighbors_missing_node_raises(empty_graph):
    with pytest.raises(ValueError):
        empty_graph.neighbors('A')


def test_adjacent_true(multi_graph):
    multi_graph.add_edge('A', 'B')
    assert multi_graph.adjacent('A', 'B')


def test_adjacent_false(multi_graph):
    assert not multi_graph.adjacent('A', 'B')


def test_adjacent_missing_node_raises(empty_graph):
    with pytest.raises(ValueError):
        empty_graph.adjacent('A', 'B')


def test_del_node(one_graph):
    one_graph.del_node('A')
    assert one_graph.graph == {}


def test_del_node_missing_raises(empty_graph):
    with pytest.raises(ValueError):
        empty_graph.del_node('A')


def test_del_node_removes_edges(multi_graph):
    multi_graph.add_edge('A', 'C')
    multi_graph.add_edge('B', 'C')
    multi_graph.add_edge('A', 'D')
    multi_graph.del_node('C')
    assert sorted(multi_graph.nodes()) == ['A', 'B', 'D', 'E']
    assert sorted(multi_graph.edges()) == [('A', 'D')]