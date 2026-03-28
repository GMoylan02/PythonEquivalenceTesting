import pytest


@pytest.fixture
def empty_heap():
    from binheap import Binheap
    bh = Binheap()
    return bh


@pytest.fixture
def heap():
    from binheap import Binheap
    bh = Binheap([10, 4, 2, 6, 13, 72, 1, 49])
    return bh


def test_push_val_to_head(empty_heap):
    empty_heap.push(3)
    assert empty_heap.container == [None, 3]


def test_push_val(empty_heap):
    empty_heap.push(3)
    empty_heap.push(2)
    assert empty_heap.container == [None, 3, 2]


def test_push_val_large(empty_heap):
    empty_heap.push(3)
    empty_heap.push(2)
    empty_heap.push(1)
    empty_heap.push(16)
    assert empty_heap.container == [None, 16, 3, 1, 2]


def test_push_on_empty(empty_heap):
    empty_heap.push(1)
    assert empty_heap.container == [None, 1]


def test_initialize_iterable(heap):
    assert heap.container == [None, 72, 49, 13, 10, 6, 2, 1, 4]


def test_display(heap):
    tree = '    72 \n  49 13 \n 10 6 2 1 \n4 \n'
    assert heap.display() == tree


def test_pop(heap):
    heap.pop()
    assert heap.container == [None, 49, 10, 13, 4, 6, 2, 1]


def test_pop_return_value(heap):
    assert heap.pop() == 72


def test_push_pop(heap):
    heap.push(5)
    heap.pop()
    assert heap.container == [None, 49, 10, 13, 5, 6, 2, 1, 4]


def test_pop_single_element(empty_heap):
    empty_heap.push(5)
    empty_heap.pop()
    assert empty_heap.container == [None]


def test_pop_returns_max_order(heap):
    results = [heap.pop() for _ in range(3)]
    assert results == [72, 49, 13]


def test_pop_empty(empty_heap):
    with pytest.raises(IndexError):
        empty_heap.pop()
