import pytest


@pytest.fixture
def test_queues():
    from a_queue import Queue
    zero = Queue()
    one = Queue([3])
    multi = Queue([1, 2, 3, 4, 5])
    return zero, one, multi


def test_enqueue_adds_data(test_queues):
    test_queues[0].enqueue(3)
    assert test_queues[0].queue == [3]


def test_enqueue_adds_data_to_tail(test_queues):
    test_queues[1].enqueue(2)
    assert test_queues[1].queue == [3, 2]


def test_enqueue_adds_to_size(test_queues):
    test_queues[2].enqueue(6)
    assert len(test_queues[2].queue) == 6


def test_dequeue_removes_data(test_queues):
    test_queues[1].dequeue()
    assert test_queues[1].queue == []


def test_dequeue_removes_from_front(test_queues):
    test_queues[2].dequeue()
    assert test_queues[2].queue == [2, 3, 4, 5]


def test_dequeue_returns_correct_value(test_queues):
    assert test_queues[2].dequeue() == 1


def test_dequeue_reduces_size(test_queues):
    test_queues[2].dequeue()
    assert len(test_queues[2].queue) == 4


def test_peek_returns_front(test_queues):
    assert test_queues[2].peek() == 1


def test_peek_does_not_remove(test_queues):
    test_queues[2].peek()
    assert len(test_queues[2].queue) == 5


def test_peek_on_empty(test_queues):
    assert test_queues[0].peek() is None


def test_dequeue_entire_queue(test_queues):
    q = []
    while not test_queues[2].isEmpty():
        q.append(test_queues[2].dequeue())
    assert q == [1, 2, 3, 4, 5]


def test_dequeue_on_empty_raises(test_queues):
    with pytest.raises(IndexError):
        test_queues[0].dequeue()


def test_size_on_empty_queue(test_queues):
    assert len(test_queues[0].queue) == 0


def test_size_on_queue_of_one(test_queues):
    assert len(test_queues[1].queue) == 1


def test_size_on_longer_queue(test_queues):
    assert len(test_queues[2].queue) == 5