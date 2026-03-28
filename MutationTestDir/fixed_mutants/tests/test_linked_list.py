import pytest


@pytest.fixture
def empty_list():
    from linked_list import LinkedList
    return LinkedList()


@pytest.fixture
def one_list():
    from linked_list import LinkedList
    return LinkedList(5)


@pytest.fixture
def multi_list():
    from linked_list import LinkedList
    return LinkedList([1, 2, 3, 4, 5])


def test_node_has_data():
    from linked_list import LLNode
    n = LLNode(5)
    assert n.data == 5 and n.next is None


def test_push_adds_to_head(one_list):
    assert one_list.head.data == 5


def test_ll_has_head(multi_list):
    assert multi_list.head.data == 5


def test_empty_ll_head_none(empty_list):
    assert empty_list.head is None


def test_size_one(one_list):
    assert one_list._length == 1


def test_size_multi(multi_list):
    assert multi_list._length == 5


def test_size_empty(empty_list):
    assert empty_list._length == 0


def test_push_increases_length(one_list):
    length = one_list._length
    one_list.push(3)
    assert one_list._length == length + 1


def test_pop_updates_head(multi_list):
    multi_list.pop()
    assert multi_list.head.data == 4


def test_pop_returns_data(multi_list):
    assert multi_list.pop() == 5


def test_pop_decreases_length(multi_list):
    length = multi_list._length
    multi_list.pop()
    assert multi_list._length == length - 1


def test_pop_single_element(one_list):
    one_list.pop()
    assert one_list.head is None


def test_pop_decreases_length_to_zero(one_list):
    one_list.pop()
    assert one_list._length == 0


def test_pop_empty_raises(empty_list):
    with pytest.raises(IndexError):
        empty_list.pop()


def test_size_after_push(empty_list):
    length = empty_list.size()
    empty_list.push(4)
    assert empty_list.size() == length + 1


def test_size_after_pop(multi_list):
    length = multi_list.size()
    multi_list.pop()
    assert multi_list.size() == length - 1


def test_size_after_push_and_pop(multi_list):
    multi_list.push(4)
    multi_list.push(2)
    multi_list.pop()
    assert multi_list.size() == 6


def test_search_returns_node(multi_list):
    assert multi_list.search(2).data == 2


def test_search_missing_returns_none(multi_list):
    assert multi_list.search(9) is None


def test_remove_middle(multi_list):
    multi_list.remove(4)
    assert multi_list.size() == 4


def test_remove_second_to_last(multi_list):
    multi_list.remove(2)
    assert multi_list.size() == 4


def test_remove_last(multi_list):
    multi_list.remove(1)
    assert multi_list.size() == 4


def test_remove_head(multi_list):
    multi_list.remove(5)
    assert multi_list.size() == 4


def test_remove_single_element(one_list):
    one_list.remove(5)
    assert one_list.size() == 0


def test_remove_missing_raises(multi_list):
    with pytest.raises(ValueError):
        multi_list.remove(9)


def test_remove_from_empty_raises(empty_list):
    with pytest.raises(ValueError):
        empty_list.remove(1)


def test_display_multi(multi_list):
    assert multi_list.display() == '(5, 4, 3, 2, 1)'


def test_display_one(one_list):
    assert one_list.display() == '(5)'


def test_display_empty(empty_list):
    assert empty_list.display() == '()'