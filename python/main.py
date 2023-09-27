from typing import TypeVar

TNode = TypeVar("TNode", bound="Node")


class Node:
    value: int
    next: TNode | None = None
    previous: TNode | None = None

    def __init__(self, value: int):
        self.value = value


class LinkedList:
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
        self._size += 1

    def index(self, value: int):
        index = 0
        node = self._initial
        while node is not None:
            if node.value == value:
                return index
            node = node.next
            index += 1
        return -1

    def insert(self, index: int, value: int):
        new_node = Node(value)
        if index == 0:
            new_node.next = self._initial
            self._initial = new_node
        else:
            previous_node = self._get_node(index - 1)
            new_node.next = previous_node.next
            previous_node.next = new_node
        self._size += 1

    def remove(self, value: int):
        if self._size == 0:
            return ValueError()
        if self._initial.value == value:
            aux = self._initial.next
            self._initial.next = None
            self._initial = aux
            self._size -= 1
            return True
        else:
            previous_node = self._initial
            current_node = previous_node.next
            while current_node is not None:
                if current_node.value == value:
                    previous_node.next = current_node.next
                    current_node.next = None
                    self._size -= 1
                    return True
                previous_node = current_node
                current_node = current_node.next
            return False

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
    linked_list = LinkedList()

    BIG_INDEX = 2**100

    linked_list.append(10)
    linked_list.append(11)
    linked_list.append(12)

    # check length
    assert linked_list._size == 3
    assert len(linked_list) == 3

    # check getitem
    assert linked_list[0] == 10
    assert linked_list[1] == 11
    assert linked_list[2] == 12

    # check inverted getitem
    assert linked_list[-1] == 12
    assert linked_list[-2] == 11
    assert linked_list[-3] == 10

    # check index
    assert linked_list.index(10) == 0
    assert linked_list.index(11) == 1
    assert linked_list.index(12) == 2

    # check index of inexistent
    assert linked_list.index(BIG_INDEX) == -1

    # check getitem of an index bigger than length
    try:
        linked_list[BIG_INDEX]
        raise AssertionError()
    except Exception as e:
        assert isinstance(e, IndexError)

    # check getitem of an index smaller than negative length
    try:
        linked_list[-BIG_INDEX]
        raise AssertionError()
    except Exception as e:
        assert isinstance(e, IndexError)

    # check setitem
    linked_list[0] = 20
    linked_list[1] = 21
    linked_list[2] = 22

    assert linked_list[0] == 20
    assert linked_list[1] == 21
    assert linked_list[2] == 22

    # check inverted setitem
    linked_list[-1] = 32
    linked_list[-2] = 31
    linked_list[-3] = 30

    assert linked_list[2] == 32
    assert linked_list[1] == 31
    assert linked_list[0] == 30

    # check setitem of an index bigger than length
    try:
        linked_list[BIG_INDEX] = 1
        raise AssertionError()
    except Exception as e:
        assert isinstance(e, IndexError)

    # check setitem of an index smaller than negative length
    try:
        linked_list[-BIG_INDEX] = 1
        raise AssertionError()
    except Exception as e:
        assert isinstance(e, IndexError)

    # check insert before initial
    aux = linked_list[0]
    linked_list.insert(0, 150)
    assert linked_list[0] == 150
    assert linked_list[1] == aux
    assert len(linked_list) == 4

    # check insert in the middle
    aux = linked_list[2]
    linked_list.insert(2, 232)
    assert linked_list[2] == 232
    assert linked_list[3] == aux
    assert len(linked_list) == 5

    # check insert after last
    aux = linked_list[len(linked_list) - 1]
    linked_list.insert(len(linked_list), 345)
    assert linked_list[len(linked_list) - 1] == 345
    assert linked_list[len(linked_list) - 2] == aux
    assert len(linked_list) == 6

    linked_list = LinkedList()

    linked_list.append(10)
    linked_list.append(20)
    linked_list.append(30)
    linked_list.append(40)
    linked_list.append(50)

    # remove the first item
    aux = linked_list[1]
    assert linked_list.remove(10)
    assert linked_list[0] == aux
    assert len(linked_list) == 4

    # remove the middle item
    aux = linked_list[2]
    assert linked_list.remove(30)
    assert linked_list[1] == aux
    assert len(linked_list) == 3

    # remove the last item
    aux = linked_list[len(linked_list) - 2]
    assert linked_list.remove(50)
    assert linked_list[len(linked_list) - 1] == aux
    assert len(linked_list) == 2

    # remove inexistent item
    assert not linked_list.remove(30)
