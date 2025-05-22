import pytest

from my_list import MyList, ListNode
from test_data import *


@pytest.fixture(params=[SINGLE_VALUES1, SINGLE_VALUES2])
def get_5_nodes(request):
    return {
        "values": request.param,
        "nodes": ListNode(
            request.param[0],
            ListNode(
                request.param[1],
                ListNode(
                    request.param[2],
                    ListNode(request.param[3], ListNode(request.param[4])),
                ),
            ),
        ),
        "str": get_list_str(request.param),
    }


@pytest.mark.listnode
@pytest.mark.parametrize("value", SINGLE_VALUES1)
def test_single_node_init(value):
    n = ListNode(value)
    assert isinstance(n, ListNode)
    assert n.value == value
    assert n.next is None


@pytest.mark.listnode
def test_wrong_init_raises_exception():
    with pytest.raises(TypeError):
        ListNode(1, 2)
    with pytest.raises(TypeError):
        ListNode(1, 0.2)
    with pytest.raises(TypeError):
        ListNode(1, "2")
    with pytest.raises(TypeError):
        ListNode(1, [2])
    with pytest.raises(TypeError):
        ListNode(1, (2))
    with pytest.raises(TypeError):
        ListNode(1, {2})
    with pytest.raises(TypeError):
        ListNode(1, {2: 2})


@pytest.mark.listnode
@pytest.mark.parametrize("value1, value2", DOUBLE_VALUES)
def test_double_node_init(value1, value2):
    n2 = ListNode(value2)
    n1 = ListNode(value1, n2)
    assert isinstance(n1, ListNode)
    assert n1.value == value1
    assert n1.next == n2

    assert isinstance(n2, ListNode)
    assert n2.value == value2
    assert n2.next is None


@pytest.mark.listnode
@pytest.mark.parametrize("value", SINGLE_VALUES2)
def test_single_node_str(value):
    n = ListNode(value)
    assert str(n) == f"({value}) -> None"


@pytest.mark.listnode
@pytest.mark.parametrize("values, str_values", STR_CHECK_2_VALUES)
def test_double_node_str(values, str_values):
    nodes = ListNode(values[0], ListNode(values[1]))
    assert str(nodes) == str_values


@pytest.mark.listnode
@pytest.mark.parametrize("values, str_values", STR_CHECK_3_VALUES)
def test_triple_node_str(values, str_values):
    nodes = ListNode(values[0], ListNode(values[1], ListNode(values[2])))
    assert str(nodes) == str_values


@pytest.mark.listnode
def test_5_node_str(get_5_nodes):
    nodes = get_5_nodes["nodes"]
    assert str(nodes) == get_5_nodes["str"]


@pytest.mark.listnode
@pytest.mark.parametrize("value", SINGLE_VALUES1)
def test_single_node_not_eq(value):
    node1 = ListNode(value)
    node2 = ListNode(value + 1)
    assert node1 != node2


@pytest.mark.listnode
@pytest.mark.parametrize("value", SINGLE_VALUES2)
def test_single_node_eq(value):
    node1 = ListNode(value)
    node2 = ListNode(value)
    assert node1 == node2


@pytest.mark.listnode
@pytest.mark.parametrize("value1, value2", DOUBLE_VALUES)
def test_double_node_not_eq(value1, value2):
    node1 = ListNode(value1, ListNode(value2))
    node2 = ListNode(value1, ListNode(value2 - 1))
    assert node1 != node2


@pytest.mark.listnode
@pytest.mark.parametrize("value1, value2", DOUBLE_VALUES)
def test_double_node_eq(value1, value2):
    node1 = ListNode(value1, ListNode(value2))
    node2 = ListNode(value1, ListNode(value2))
    assert node1 == node2


@pytest.mark.listnode
def test_multi_node_not_eq(get_5_nodes):
    node1 = get_5_nodes["nodes"]
    node2 = ListNode(0, get_5_nodes["nodes"])
    assert node1 != node2


@pytest.mark.listnode
def test_multi_node_eq(get_5_nodes):
    node1 = get_5_nodes
    node2 = get_5_nodes
    assert node1 == node2


@pytest.mark.mylist
def test_list_init_empty():
    lst1 = MyList()
    assert lst1.head is None
    assert isinstance(lst1, MyList)
    lst2 = MyList(None)
    assert isinstance(lst2, MyList)
    assert lst2.head is None


@pytest.mark.mylist
@pytest.mark.parametrize("value", SINGLE_VALUES1)
def test_list_init_nonempty(value):
    lst = MyList(value)
    assert isinstance(lst, MyList)
    assert isinstance(lst.head, ListNode)
    assert lst.head.value == value
    assert lst.head.next is None


@pytest.mark.mylist
@pytest.mark.parametrize("value", SINGLE_VALUES2)
def test_list_append_on_empty(value):
    lst = MyList()
    lst.append(value)
    assert isinstance(lst.head, ListNode)
    assert lst.head.value == value
    assert lst.head.next is None


@pytest.mark.mylist
@pytest.mark.parametrize("value1, value2", DOUBLE_VALUES)
def test_list_append_on_nonempty(value1, value2):
    lst = MyList(value1)
    lst.append(value2)
    assert lst.head.value == value1
    assert lst.head.next == ListNode(value2)
    assert lst.head.next.value == value2
    assert lst.head.next.next is None


@pytest.mark.mylist
@pytest.mark.parametrize("value1, value2, value3", TRIPLE_VALUES)
def test_list_double_append_on_nonempty(value1, value2, value3):
    lst = MyList(value1)
    lst.append(value2)
    lst.append(value3)
    assert lst.head.value == value1
    assert lst.head.next == ListNode(value2, ListNode(value3))
    assert lst.head.next.value == value2
    assert lst.head.next.next == ListNode(value3)
    assert lst.head.next.next.value == value3
    assert lst.head.next.next.next is None


@pytest.mark.mylist
def test_append_5_times(get_5_nodes):
    lst = MyList()
    values = get_5_nodes["values"]
    for v in values:
        lst.append(v)
    assert get_5_nodes["nodes"] == lst.head


@pytest.mark.mylist
def test_list_len_empty():
    lst = MyList()
    assert len(lst) == 0


@pytest.mark.mylist
def test_list_len_nonempty():
    lst = MyList(1)
    assert len(lst) == 1
    for i in range(2, 100):
        lst.append(1)
        assert len(lst) == i


@pytest.mark.mylist
def test_list_str_empty():
    assert str(MyList()) == "None"


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_str_nonempty(values):
    lst = MyList()
    for v in values:
        lst.append(v)
    assert str(lst) == get_list_str(values)


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_repr_nonempty(values):
    lst = MyList()
    for v in values:
        lst.append(v)
    assert str(lst) == lst.__repr__()


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS)
def test_list_eq(values):
    lst1 = MyList()
    assert lst1 is not None
    assert lst1 is not False
    assert lst1 != 0
    assert lst1 != 0.0
    assert lst1 != ""
    assert lst1 != []
    assert lst1 != ()
    assert lst1 != {}
    assert lst1 != dict()

    lst2 = MyList()
    assert lst1 == lst2
    assert lst1 is not lst2

    for v in values:
        lst1.append(v)
        assert lst1 != lst2
        lst2.append(v)
        assert lst1 == lst2


@pytest.mark.mylist
def test_list_contains_empty():
    lst = MyList()
    for v in range(100):
        assert v not in lst


@pytest.mark.mylist
def test_list_contains_nonempty():
    lst = MyList(-1)
    assert -1 in lst
    for v in range(100):
        assert v not in lst
        lst.append(v)
        assert v in lst


@pytest.mark.mylist
def test_list_remove_empty_raises_exception():
    lst = MyList()
    with pytest.raises(ValueError):
        lst.remove(None)


@pytest.mark.mylist
@pytest.mark.parametrize("value", SINGLE_VALUES2)
def test_list_remove_single(value):
    lst = MyList(value)
    assert len(lst) == 1
    assert value in lst
    lst.remove(value)
    assert len(lst) == 0
    assert lst.head is None
    assert value not in lst
    lst = MyList()
    lst.append(value)
    assert len(lst) == 1
    assert value in lst
    lst.remove(value)
    assert len(lst) == 0
    assert lst.head is None
    assert value not in lst


@pytest.mark.mylist
@pytest.mark.parametrize("values", DOUBLE_VALUES)
def test_list_2_nodes_remove_head(values):
    lst = MyList(values[0])
    lst.append(values[1])
    lst.remove(values[0])
    assert len(lst) == 1
    assert lst.head == ListNode(values[1])
    assert lst.head.next is None


@pytest.mark.mylist
@pytest.mark.parametrize("values", DOUBLE_VALUES)
def test_list_2_nodes_remove_tail(values):
    lst = MyList(values[0])
    lst.append(values[1])
    lst.remove(values[1])
    assert len(lst) == 1
    assert lst.head == ListNode(values[0])
    assert lst.head.next is None


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_remove_absent_raises_exception(values):
    lst = MyList()
    for v in values:
        lst.append(v)
    expected_len = len(values)
    assert len(lst) == expected_len
    with pytest.raises(ValueError):
        lst.remove(666)
    assert len(lst) == expected_len


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS)
def test_list_remove_present(values):
    lst = MyList()
    for v in values:
        lst.append(v)
    expected_len = len(values)
    lst.remove(values[-1])
    assert values[-1] not in lst
    for v in values[:-1]:
        assert v in lst
    assert len(lst) == expected_len - 1


@pytest.mark.mylist
def test_list_many_appends_and_removes():
    lst = MyList()
    for _ in range(100):
        lst.append(42)
        lst.remove(42)
    assert len(lst) == 0


@pytest.mark.mylist
def test_list_pop_empty_raises_exception():
    lst = MyList()
    with pytest.raises(IndexError):
        lst.pop()


@pytest.mark.mylist
@pytest.mark.parametrize("value", SINGLE_VALUES1)
def test_list_pop_single(value):
    lst = MyList(value)
    assert lst.pop() == value
    assert len(lst) == 0
    lst.append(value)
    assert lst.pop() == value
    assert len(lst) == 0


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS)
def test_list_pop_nonempty(values):
    lst = MyList()
    for v in values:
        lst.append(v)
    val_len = len(values)
    pop_cnt = 0
    for v in values[::-1]:
        assert lst.pop() == v
        pop_cnt += 1
        assert len(lst) == val_len - pop_cnt


@pytest.mark.mylist
@pytest.mark.parametrize("value", SINGLE_VALUES2)
def test_list_append_pop(value):
    lst = MyList(value)
    for _ in range(100):
        lst.append(lst.pop())
    assert len(lst) == 1
    assert value in lst
    assert lst == MyList(value)


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_clear(values):
    lst = MyList()
    src_id = id(lst)
    for v in values:
        lst.append(v)
    lst.clear()
    assert id(lst) == src_id
    assert lst.head is None
    assert len(lst) == 0


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_extend_empty(values):
    lst1 = MyList()
    lst2 = MyList()
    for v in values:
        lst2.append(v)
    lst1.extend(lst2)
    assert len(lst1) == len(values)
    assert str(lst1) == get_list_str(values)


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_extend_with_empty(values):
    lst1 = MyList()
    for v in values:
        lst1.append(v)
    lst2 = MyList()
    lst1.extend(lst2)
    assert len(lst1) == len(values)
    assert str(lst1) == get_list_str(values)


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_extend_nonempty(values):
    lst1 = MyList()
    for v in values:
        lst1.append(v)
    lst2 = MyList()
    for v in values[::-1]:
        lst2.append(v)
    lst1.extend(lst2)
    assert len(lst1) == len(values) * 2
    assert str(lst1) == get_list_str(values + values[::-1])


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_wrong_extend_raises_exception(values):
    lst = MyList()
    with pytest.raises(TypeError):
        lst.extend(values)
    with pytest.raises(TypeError):
        lst.extend(values[0] if values else 1)


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_copy(values):
    lst1 = MyList()
    for v in values:
        lst1.append(v)
    lst2 = lst1.copy()
    assert id(lst1) != id(lst2)
    assert len(lst1) == len(lst2) == len(values)
    assert str(lst1) == str(lst2)


@pytest.mark.mylist
@pytest.mark.parametrize("index, value", DOUBLE_VALUES)
def test_list_insert_in_empty(index, value):
    lst = MyList()
    lst.insert(index, value)
    assert len(lst) == 1
    assert lst.head == ListNode(value)
    assert lst.head.next is None


@pytest.mark.mylist
def test_list_wrong_insert_raises_exception():
    lst = MyList()
    with pytest.raises(IndexError):
        lst.insert(-1, -1)
    with pytest.raises(IndexError):
        lst.insert(1.2, 1.2)
    with pytest.raises(IndexError):
        lst.insert([12], 1.2)
    assert len(lst) == 0


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_insert_in_head(values):
    lst = MyList()
    for v in values:
        lst.append(v)
    to_insert = values[-1] if values else 42
    lst.insert(0, to_insert)
    assert len(lst) == len(values) + 1
    assert str(lst) == get_list_str([to_insert] + list(values))


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_insert_in_tail1(values):
    lst = MyList()
    for v in values:
        lst.append(v)
    to_insert = values[-1] if values else 42
    lst.insert(len(values) - 1 if values else 0, to_insert)
    assert len(lst) == len(values) + 1
    assert str(lst) == get_list_str(list(values) + [to_insert])


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_insert_in_tail2(values):
    lst = MyList()
    for v in values:
        lst.append(v)
    to_insert = values[-1] if values else 42
    lst.insert(555, to_insert)
    assert len(lst) == len(values) + 1
    assert str(lst) == get_list_str(list(values) + [to_insert])


@pytest.mark.mylist
@pytest.mark.parametrize("values", [SINGLE_VALUES1, SINGLE_VALUES2])
def test_list_insert_in_nth_pos(values):
    for i in range(1, 5):
        new_values = values.copy()
        lst = MyList()
        for v in new_values:
            lst.append(v)
        new_values.insert(i, 42)
        lst.insert(i, 42)
        assert len(lst) == len(new_values)
        assert str(lst) == get_list_str(new_values)


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_reverse(values):
    lst1 = MyList()
    for v in values:
        lst1.append(v)
    lst2 = MyList()
    for v in values[::-1]:
        lst2.append(v)
    src_id = id(lst1)
    lst1.reverse()
    assert id(lst1) == src_id
    assert len(lst1) == len(values)
    assert str(lst1) == str(lst2)


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_index(values):
    lst = MyList()
    for v in values:
        lst.append(v)
    for i, v in enumerate(values):
        assert i == lst.index(v)


@pytest.mark.mylist
def test_list_index_empty_raises_exception():
    lst = MyList()
    with pytest.raises(ValueError):
        lst.index(69)


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_index_absent_raises_exception(values):
    lst = MyList()
    for v in values:
        lst.append(v)
    with pytest.raises(ValueError):
        lst.index(42069)


@pytest.mark.mylist
@pytest.mark.parametrize("value", SINGLE_VALUES1)
def test_list_count_empty(value):
    lst = MyList()
    assert lst.count(value) == 0


@pytest.mark.mylist
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_count_nonempty(values):
    lst = MyList()
    for v in values:
        lst.append(v)
    for v in values:
        assert lst.count(v) == 1


@pytest.mark.mylist
def test_list_count_same():
    from random import randint

    lst = MyList()
    for _ in range(randint(0, 1000)):
        lst.append(42)
    assert lst.count(42) == len(lst)
