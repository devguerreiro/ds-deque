from typing import List, TypeVar

TNode = TypeVar("TNode", bound="Node")


class Node:
    value: int
    next: TNode | None = None
    previous: TNode | None = None

    def __init__(self, value: int):
        self.value = value


class Deque:
    _initial: Node | None = None
    _size: int = 0

    def _get_node(self, index: int, direction: str = "right"):
        _index = self._size + index if index < 0 else index
        if _index < 0:
            raise IndexError()
        node = self._initial
        for _ in range(_index):
            if node is None:
                raise IndexError()
            elif direction == "right":
                node = node.next
            else:
                node = node.previous
        return node

    def append(self, value: int):
        new_node = Node(value)
        if self._size == 0:
            self._initial = new_node
        else:
            last_node: Node = self._initial
            while last_node.next is not None:
                last_node = last_node.next
            last_node.next = new_node
            new_node.previous = last_node
        self._size += 1

    def append_left(self, value: int):
        new_node = Node(value)
        if self._size == 0:
            self._initial = new_node
        else:
            last_node: Node = self._initial
            while last_node.previous is not None:
                last_node = last_node.previous
            last_node.previous = new_node
            new_node.next = last_node
            self._initial = new_node
        self._size += 1

    def _extend(self, values: List[int], last_node: Node):
        for v in values:
            new_node = Node(v)
            last_node.next = new_node
            new_node.previous = last_node
            last_node = new_node
            self._size += 1

    def extend(self, values: List[int]):
        if self._size == 0:
            self._initial = Node(values[0])
            self._size += 1
            self._extend(values[1:], self._initial)
        else:
            last_node: Node = self._initial
            while last_node.next is not None:
                last_node = last_node.next
            self._extend(values, last_node)

    def _extend_left(self, values: List[int], last_node: Node):
        for v in values:
            new_node = Node(v)
            last_node.previous = new_node
            new_node.next = last_node
            last_node = new_node
            self._initial = new_node
            self._size += 1

    def extend_left(self, values: List[int]):
        if self._size == 0:
            self._initial = Node(values[0])
            self._size += 1
            self._extend_left(values[1:], self._initial)
        else:
            last_node: Node = self._initial
            while last_node.previous is not None:
                last_node = last_node.previous
            self._extend_left(values, last_node)

    def index(self, value: int):
        index = 0
        node = self._initial
        while node is not None:
            if node.value == value:
                return index
            node = node.next
            index += 1
        return -1

    def __len__(self):
        return self._size

    def __getitem__(self, key: int):
        if self._size == 0:
            raise IndexError()
        node = self._get_node(key)
        return node.value

    def __setitem__(self, key: int, value: int):
        node = self._get_node(key)
        node.value = value


if __name__ == "__main__":
    deque = Deque()

    BIG_INDEX = 2**100

    # add to right
    deque.append(10)
    deque.append(11)
    deque.append(12)

    assert len(deque) == 3

    # check getitem
    assert deque[0] == 10
    assert deque[1] == 11
    assert deque[2] == 12

    # check inverted getitem
    assert deque[-1] == 12
    assert deque[-2] == 11
    assert deque[-3] == 10

    # check index
    assert deque.index(10) == 0
    assert deque.index(11) == 1
    assert deque.index(12) == 2

    # check index of inexistent
    assert deque.index(BIG_INDEX) == -1

    # check getitem of an index bigger than length
    try:
        deque[BIG_INDEX]
        raise AssertionError()
    except Exception as e:
        assert isinstance(e, IndexError)

    # check getitem of an index smaller than negative length
    try:
        deque[-BIG_INDEX]
        raise AssertionError()
    except Exception as e:
        assert isinstance(e, IndexError)

    # check setitem
    deque[0] = 20
    deque[1] = 21
    deque[2] = 22

    assert deque[0] == 20
    assert deque[1] == 21
    assert deque[2] == 22

    # check inverted setitem
    deque[-1] = 32
    deque[-2] = 31
    deque[-3] = 30

    assert deque[2] == 32
    assert deque[1] == 31
    assert deque[0] == 30

    # check setitem of an index bigger than length
    try:
        deque[BIG_INDEX] = 1
        raise AssertionError()
    except Exception as e:
        assert isinstance(e, IndexError)

    # check setitem of an index smaller than negative length
    try:
        deque[-BIG_INDEX] = 1
        raise AssertionError()
    except Exception as e:
        assert isinstance(e, IndexError)

    deque2 = Deque()

    # extend to right from empty deque
    deque2.extend([1, 2, 3])

    assert len(deque2) == 3

    # check getitem
    assert deque2[0] == 1
    assert deque2[1] == 2
    assert deque2[2] == 3

    # extend to right
    deque2.extend([13, 14, 15])

    assert len(deque2) == 6

    assert deque2[3] == 13
    assert deque2[4] == 14
    assert deque2[5] == 15

    deque3 = Deque()

    # add to left
    deque3.append_left(10)
    deque3.append_left(11)
    deque3.append_left(12)

    assert len(deque3) == 3

    # check getitem
    assert deque3[0] == 12
    assert deque3[1] == 11
    assert deque3[2] == 10

    # extend to left
    deque3.extend_left([13, 14, 15])

    assert len(deque3) == 6

    assert deque3[2] == 13
    assert deque3[1] == 14
    assert deque3[0] == 15
