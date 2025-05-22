import pytest
from double_linked_list import StudentNode, DoublyLinkedList


@pytest.fixture
def sample_list():
    dll = DoublyLinkedList()
    dll.append(StudentNode("Ivanov", 2000, 2018, [5, 4, 3]))
    dll.append(StudentNode("Petrov", 1999, 2017, [5, 5, 5]))
    dll.append(StudentNode("Sidorov", 2001, 2019, [3, 4, 4]))
    dll.append(StudentNode("Zaytsev", 2000, 2018, [5, 4, 4]))
    dll.append(StudentNode("Borisov", 1998, 2016, [4, 4, 4]))
    return dll


# Tests for append method
def test_append():
    dll = DoublyLinkedList()
    node = StudentNode("Ivanov", 2000, 2018, [5, 4, 3])
    dll.append(node)
    assert dll.head == node
    assert dll.tail == node
    assert dll.head.next is None
    assert dll.head.prev is None


def test_append_multiple():
    dll = DoublyLinkedList()
    nodes = [StudentNode(f"Student{i}", 2000 + i, 2018 + i, [5, 4, 3]) for i in range(5)]
    for node in nodes:
        dll.append(node)
    assert dll.head == nodes[0]
    assert dll.tail == nodes[-1]
    assert len(dll) == len(nodes)


def test_append_empty_list():
    dll = DoublyLinkedList()
    assert dll.head is None
    assert dll.tail is None


def test_append_single():
    dll = DoublyLinkedList()
    node = StudentNode("Solo", 2000, 2018, [5])
    dll.append(node)
    assert dll.head == node
    assert dll.tail == node
    assert dll.head.next is None
    assert dll.head.prev is None


# Tests for sort method
def test_sort(sample_list):
    sample_list.sort()
    sorted_surnames = [node.surname for node in sample_list]
    assert sorted_surnames == ["Borisov", "Ivanov", "Petrov", "Sidorov", "Zaytsev"]


def test_sort_already_sorted():
    dll = DoublyLinkedList()
    nodes = [StudentNode(name, 2000, 2018, [5, 4, 3]) for name in ["A", "B", "C", "D"]]
    for node in nodes:
        dll.append(node)
    dll.sort()
    sorted_names = [node.surname for node in dll]
    assert sorted_names == ["A", "B", "C", "D"]


def test_sort_reverse_sorted():
    dll = DoublyLinkedList()
    nodes = [StudentNode(name, 2000, 2018, [5, 4, 3]) for name in ["D", "C", "B", "A"]]
    for node in nodes:
        dll.append(node)
    dll.sort()
    sorted_names = [node.surname for node in dll]
    assert sorted_names == ["A", "B", "C", "D"]


def test_sort_empty_list():
    dll = DoublyLinkedList()
    dll.sort()
    assert len(dll) == 0


# Tests for remove method
def test_remove_head(sample_list):
    head_node = sample_list.head
    sample_list.remove(head_node)
    assert sample_list.head.surname != head_node.surname


def test_remove_tail(sample_list):
    tail_node = sample_list.tail
    sample_list.remove(tail_node)
    assert sample_list.tail.surname != tail_node.surname


def test_remove_middle(sample_list):
    middle_node = sample_list.head.next.next
    sample_list.remove(middle_node)
    remaining_surnames = [node.surname for node in sample_list]
    assert middle_node.surname not in remaining_surnames


def test_remove_single_node():
    dll = DoublyLinkedList()
    node = StudentNode("Solo", 2000, 2018, [5])
    dll.append(node)
    dll.remove(node)
    assert dll.head is None
    assert dll.tail is None


# Tests for binary_search_by_surname method
def test_binary_search_by_surname(sample_list):
    sample_list.sort()
    node = sample_list.binary_search_by_surname("Petrov")
    assert node is not None
    assert node.surname == "Petrov"

    node = sample_list.binary_search_by_surname("NonExistent")
    assert node is None


def test_binary_search_first_node(sample_list):
    sample_list.sort()
    node = sample_list.binary_search_by_surname("Borisov")
    assert node is not None
    assert node.surname == "Borisov"


def test_binary_search_last_node(sample_list):
    sample_list.sort()
    node = sample_list.binary_search_by_surname("Zaytsev")
    assert node is not None
    assert node.surname == "Zaytsev"


def test_binary_search_empty_list():
    dll = DoublyLinkedList()
    node = dll.binary_search_by_surname("NonExistent")
    assert node is None


# Tests for magic methods
def test_studentnode_eq():
    node1 = StudentNode("Ivanov", 2000, 2018, [5, 4, 3])
    node2 = StudentNode("Ivanov", 2000, 2018, [5, 4, 3])
    assert node1 == node2


def test_studentnode_ne():
    node1 = StudentNode("Ivanov", 2000, 2018, [5, 4, 3])
    node2 = StudentNode("Petrov", 1999, 2017, [5, 5, 5])
    assert node1 != node2


def test_studentnode_lt():
    node1 = StudentNode("Ivanov", 2000, 2018, [5, 4, 3])
    node2 = StudentNode("Petrov", 1999, 2017, [5, 5, 5])
    assert node1 < node2


def test_studentnode_gt():
    node1 = StudentNode("Petrov", 1999, 2017, [5, 5, 5])
    node2 = StudentNode("Ivanov", 2000, 2018, [5, 4, 3])
    assert node1 > node2


def test_studentnode_le():
    node1 = StudentNode("Ivanov", 2000, 2018, [5, 4, 3])
    node2 = StudentNode("Petrov", 1999, 2017, [5, 5, 5])
    assert node1 <= node1
    assert node1 <= node2


def test_studentnode_ge():
    node1 = StudentNode("Petrov", 1999, 2017, [5, 5, 5])
    node2 = StudentNode("Ivanov", 2000, 2018, [5, 4, 3])
    assert node1 >= node1
    assert node1 >= node2
