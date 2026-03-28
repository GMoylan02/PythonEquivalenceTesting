import pytest


@pytest.fixture
def empty_list():
    from dll import DoubleLinkedList
    empty = DoubleLinkedList()
    return empty

@pytest.fixture
def one_list():
    from dll import DoubleLinkedList
    one = DoubleLinkedList(3)
    return one

@pytest.fixture
def multi_list():
    from dll import DoubleLinkedList
    multi = DoubleLinkedList([1, 2, 3, 4, 5])
    return multi


def test_node_class():
    from dll import DLLNode
    node = DLLNode(5)
    assert node.data == 5

def test_nodeas_list():
    from dll import DLLNode
    value = 5
    node = DLLNode(value)
    assert str(node) == f"Value: {value}"


def test_list_of_none(empty_list):
    assert empty_list.head is None
    assert empty_list.tail is None


def test_list_of_one(one_list):
    assert one_list.head == one_list.tail


def test_list_of_five(multi_list):
    assert multi_list.head.data == 5
    assert multi_list.tail.data == 1


def test_prev_pointer(multi_list):
    assert multi_list.tail.prev.data == 2


def test_next_pointer(multi_list):
    assert multi_list.head.next.data == 4


def test_push_increases_length(empty_list):
    empty_list.push(2)
    assert empty_list._length == 1


def test_push_updates_head(one_list):
    one_list.push(6)
    assert one_list.head.data == 6


def test_push_points_back(one_list):
    old_head = one_list.head
    one_list.push(6)
    assert one_list.head == old_head.prev


def test_pop_reduces_length(multi_list):
    old_length = multi_list._length
    multi_list.pop()
    assert multi_list._length == old_length - 1


def test_pop_removes_head(multi_list):
    new_head = multi_list.head.next.data
    multi_list.pop()
    assert multi_list.head.data == new_head


def test_pop_removes_prev_pointer(multi_list):
    multi_list.pop()
    assert multi_list.head.prev is None


def test_pop_list_one(one_list):
    one_list.pop()
    assert one_list._length == 0


def test_pop_returns_data(multi_list):
    assert multi_list.pop() == 5


def test_cant_pop_on_empty_list(empty_list):
    with pytest.raises(IndexError):
        empty_list.pop()


def test_append_increases_length(empty_list):
    empty_list.append(2)
    assert empty_list._length == 1


def test_append_updates_tail(one_list):
    one_list.append(6)
    assert one_list.tail.data == 6


def test_append_points_back(one_list):
    old_tail = one_list.tail
    one_list.append(6)
    assert one_list.tail == old_tail.next


def test_append_on_empty_list(empty_list):
    empty_list.append(6)
    assert empty_list.tail.data == 6
    assert empty_list.head.data == 6


def test_append_next_pointer_is_none(multi_list):
    multi_list.append(6)
    assert multi_list.tail.next is None


def test_pop_sequence(multi_list):
    l = []
    while True:
        try:
            popped_data = multi_list.pop()
            l.append(popped_data)
        except IndexError:
            break
    assert l == [5, 4, 3, 2, 1]


def test_push_pop(one_list):
    one_list.push(9)
    popped_data = one_list.pop()
    assert popped_data == 9


def test_shift_reduces_length(multi_list):
    old_length = multi_list._length
    multi_list.shift()
    assert multi_list._length == old_length - 1


def test_shift_removes_tail(multi_list):
    new_tail = multi_list.tail.prev.data
    multi_list.shift()
    assert multi_list.tail.data == new_tail


def test_shift_removes_next_pointer(multi_list):
    multi_list.shift()
    assert multi_list.tail.next is None


def test_shift_list_one(one_list):
    one_list.shift()
    assert one_list._length == 0


def test_cant_shift_on_empty_list(empty_list):
    with pytest.raises(IndexError):
        empty_list.shift()


def test_shift_sequence(multi_list):
    l = []
    while True:
        try:
            shifted_data = multi_list.shift()
            l.append(shifted_data)
        except IndexError:
            break
    assert l == [1, 2, 3, 4, 5]


def test_shift_append(one_list):
    one_list.append(9)
    shifted_data = one_list.shift()
    assert shifted_data == 9


def test_remove_middle_of_list(multi_list):
    multi_list.remove(3)
    assert multi_list.as_list() == [5, 4, 2, 1]


def test_remove_head_of_list(multi_list):
    multi_list.remove(5)
    assert multi_list.as_list() == [4, 3, 2, 1]


def test_remove_tail_of_list(multi_list):
    multi_list.remove(1)
    assert multi_list.as_list() == [5, 4, 3, 2]


def test_remove_middle_decreases_length(multi_list):
    multi_list.remove(3)
    assert multi_list._length == 4


def test_remove_head_decreases_length(multi_list):
    multi_list.remove(5)
    assert multi_list._length == 4


def test_remove_tail_decreases_length(multi_list):
    multi_list.remove(1)
    assert multi_list._length == 4


def test_remove_middle_updates_pointers(multi_list):
    multi_list.remove(3)
    assert multi_list.head.next.next.data == 2


def test_remove_head_pointers(multi_list):
    multi_list.remove(5)
    assert multi_list.head.data == 4
    assert multi_list.head.prev is None


def test_remove_tail_pointers(multi_list):
    multi_list.remove(1)
    assert multi_list.tail.data == 2
    assert multi_list.tail.next is None


def test_remove_list_of_one_length(one_list):
    one_list.remove(3)
    assert one_list._length == 0


def test_remove_list_of_one(one_list):
    one_list.remove(3)
    assert one_list.head is None
    assert one_list.tail is None


def test_remove_list_of_none(empty_list):
    with pytest.raises(ValueError):
        empty_list.remove(3)


def test_remove_of_list_false(multi_list):
    with pytest.raises(ValueError):
        multi_list.remove(9)
