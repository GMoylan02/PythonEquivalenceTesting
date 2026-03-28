import pytest


@pytest.fixture
def empty_bst():
    from bst import Bst
    empty = Bst()
    return empty

@pytest.fixture
def one_bst():
    from bst import Bst
    one = Bst([5])
    return one

@pytest.fixture
def three_bst():
    from bst import Bst
    three = Bst([5, 3, 7])
    return three

@pytest.fixture
def balance_bst():
    from bst import Bst
    balance = Bst([5, 3, 2, 4, 9, 7, 10])
    return balance

@pytest.fixture
def leftheavy_bst():
    from bst import Bst
    leftheavy = Bst([5, 3, 2, 1])
    return leftheavy

@pytest.fixture
def rightheavy_bst():
    from bst import Bst
    rightheavy = Bst([5, 6, 7, 8, 9, 10])
    return rightheavy

@pytest.fixture
def test_traversals():
    from bst import Bst
    fixture = {
        'tree': Bst(['F', 'B', 'A', 'D', 'C', 'E', 'G', 'I', 'H']),
        'empty': Bst(),
        'pre_order': ['F', 'B', 'A', 'D', 'C', 'E', 'G', 'I', 'H'],
        'in_order': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
        'post_order': ['A', 'C', 'E', 'D', 'B', 'H', 'I', 'G', 'F'],
        'breadth': ['F', 'B', 'G', 'A', 'D', 'I', 'C', 'E', 'H']
    }
    return fixture


def test_node_is_leaf(one_bst):
    assert one_bst.root._is_leaf()


def test_insert_sets_root(empty_bst):
    empty_bst.insert(5)
    assert empty_bst.root.val == 5


def test_insert_updates_pointers(one_bst):
    one_bst.insert(3)
    assert one_bst.root.left.val == 3
    assert one_bst.root.left.parent == one_bst.root


def test_insert_smallest_left(one_bst):
    one_bst.insert(3)
    assert one_bst.root.left.val < one_bst.root.val


def test_insert_largest_right(one_bst):
    one_bst.insert(7)
    assert one_bst.root.right.val > one_bst.root.val


def test_insert_increases_size(empty_bst):
    empty_bst.insert(4)
    assert empty_bst._size == 1


def test_contains_method(three_bst):
    assert three_bst.contains(5)
    assert three_bst.contains(3)
    assert three_bst.contains(7)


def test_contains_method_no_val(leftheavy_bst):
    assert not leftheavy_bst.contains(10)


def test_depth_method(empty_bst, one_bst, three_bst, balance_bst, leftheavy_bst, rightheavy_bst):
    depths = [0, 1, 2, 3, 4, 6]
    test_bsts = [empty_bst, one_bst, three_bst, balance_bst, leftheavy_bst, rightheavy_bst]
    assert all(tree.depth() == depths[idx]
               for idx, tree in enumerate(test_bsts))


def test_balance_method(empty_bst, one_bst, three_bst, balance_bst, leftheavy_bst, rightheavy_bst):
    balance = [0, 0, 0, 0, 3, -5]
    test_bsts = [empty_bst, one_bst, three_bst, balance_bst, leftheavy_bst, rightheavy_bst]
    assert all(tree.balance() == balance[idx]
               for idx, tree in enumerate(test_bsts))


def test_search_method_node_exists(one_bst, three_bst, balance_bst, leftheavy_bst, rightheavy_bst):
    test_bsts = [one_bst, three_bst, balance_bst, leftheavy_bst, rightheavy_bst]
    assert all(tree.search(5) for tree in test_bsts)


def test_pre_order(test_traversals):
    path = [i for i in test_traversals['tree'].pre_order()]
    assert path == test_traversals['pre_order']


def test_in_order(test_traversals):
    path = [i for i in test_traversals['tree'].in_order()]
    assert path == test_traversals['in_order']


def test_post_order(test_traversals):
    path = [i for i in test_traversals['tree'].post_order()]
    assert path == test_traversals['post_order']


def test_breadth_first(test_traversals):
    path = [i for i in test_traversals['tree'].breadth_first()]
    assert path == test_traversals['breadth']


def test_traversals_none(test_traversals):
    path = [i for i in test_traversals['empty'].in_order()]
    assert path == []


def test_del_false(three_bst):
    size = three_bst._size
    three_bst.delete(1)
    assert three_bst._size == size


def test_del_empty_tree(empty_bst):
    empty_bst.delete(1)
    assert empty_bst._size == 0


def test_remove_leaf_left(three_bst):
    three_bst.delete(3)
    assert not three_bst.contains(3)
    assert three_bst._size == 2


def test_remove_leaf_right(three_bst):
    three_bst.delete(7)
    assert not three_bst.contains(7)
    assert three_bst._size == 2


def test_remove_leaf_root(one_bst):
    one_bst.delete(5)
    assert not one_bst.contains(5)
    assert one_bst._size == 0


def test_remove_one_child_left(leftheavy_bst):
    leftheavy_bst.delete(3)
    assert not leftheavy_bst.contains(3)
    assert leftheavy_bst._size == 3


def test_remove_one_child_right(rightheavy_bst):
    rightheavy_bst.delete(6)
    assert not rightheavy_bst.contains(6)
    assert rightheavy_bst._size == 5


def test_remove_one_child_right_on_left(one_bst):
    one_bst.insert(2)
    one_bst.insert(4)
    one_bst.delete(2)
    assert not one_bst.contains(2)
    assert one_bst._size == 2


def test_remove_one_child_left_on_right(one_bst):
    one_bst.insert(7)
    one_bst.insert(6)
    one_bst.delete(7)
    assert not one_bst.contains(7)
    assert one_bst._size == 2


def test_remove_one_child_root(one_bst):
    one_bst.insert(7)
    one_bst.delete(5)
    assert not one_bst.contains(5)
    assert one_bst._size == 1
    assert one_bst.root.val == 7


def test_delete_two_children(balance_bst):
    balance_bst.delete(3)
    assert not balance_bst.contains(3)
    assert balance_bst._size == 6


def test_delete_two_children_root(balance_bst):
    balance_bst.delete(5)
    assert not balance_bst.contains(5)
    assert balance_bst._size == 6
    assert balance_bst.root.val == 7

def test_delete_updates_root_with_two_children(balance_bst):
    balance_bst.delete(5)
    assert balance_bst.root.val == 7
    assert balance_bst.root.parent is None


def test_delete_two_children_keeps_bst_property(balance_bst):
    balance_bst.delete(3)
    result = list(balance_bst.in_order())
    assert result == sorted(result)


def test_delete_all_nodes(three_bst):
    for val in [5, 3, 7]:
        three_bst.delete(val)
    assert three_bst._size == 0
    assert three_bst.root is None


def test_delete_then_insert(balance_bst):
    balance_bst.delete(3)
    balance_bst.insert(3)
    assert balance_bst.contains(3)
    result = list(balance_bst.in_order())
    assert result == sorted(result)


def test_delete_node_parent_pointer_updated(balance_bst):
    balance_bst.delete(3)
    replacement = balance_bst.root.left
    assert replacement.parent == balance_bst.root
