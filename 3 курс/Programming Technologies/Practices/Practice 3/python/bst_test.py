import pytest
from test_data import *

from bst import BST
from tree_node import TreeNode


@pytest.mark.bst
def test_tree_init_empty():
    t1 = BST()
    assert isinstance(t1, BST)
    assert t1.root is None
    t2 = BST(None)
    assert isinstance(t2, BST)
    assert t2.root is None


@pytest.mark.bst
@pytest.mark.parametrize("value", SINGLE_VALUES1)
def test_tree_init_nonempty(value):
    t = BST(value)
    assert isinstance(t, BST)
    assert isinstance(t.root, TreeNode)
    assert t.root.value == value
    assert t.root.left is None
    assert t.root.right is None


@pytest.mark.bst
@pytest.mark.parametrize("value", SINGLE_VALUES2)
def test_tree_single_insert_in_empty(value):
    t = BST()
    t.insert_node(value)
    assert isinstance(t.root, TreeNode)
    assert t.root.value == value
    assert t.root.left is None
    assert t.root.right is None


@pytest.mark.bst
@pytest.mark.parametrize("value1, value2", DOUBLE_VALUES)
def test_tree_single_insert_in_nonempty(value1, value2):
    t = BST(value1)
    t.insert_node(value2)
    assert t.root.value == value1
    n = TreeNode(value2)
    if value2 < value1:
        assert t.root.left.value == value2
        assert t.root.left == n
        assert t.root.left.left is None
        assert t.root.left.right is None
        assert t.root.right is None
    else:
        assert t.root.right.value == value2
        assert t.root.right == n
        assert t.root.right.left is None
        assert t.root.right.right is None
        assert t.root.left is None


@pytest.mark.bst
@pytest.mark.parametrize("value1, value2, value3", TRIPLE_VALUES)
def test_tree_double_insert_in_nonempty(value1, value2, value3):
    t = BST(value1)
    t.insert_node(value2)
    t.insert_node(value3)
    assert t.root.value == value1
    # left tree
    if value1 > value2 > value3:
        assert t.root.right is None
        assert t.root.left.value == value2
        assert t.root.left.left.value == value3
        assert t.root.left.left.left is None
        assert t.root.left.left.right is None
        assert t.root.left.right is None
        return
    # left right tree
    if value1 > value2 < value3:
        assert t.root.right is None
        assert t.root.left.value == value2
        assert t.root.left.right.value == value3
        assert t.root.left.left is None
        assert t.root.left.right.left is None
        assert t.root.left.right.right is None
        return
    # balanced left first
    if value2 < value1 < value3:
        assert t.root.left.value == value2
        assert t.root.right.value == value3
        assert t.root.left.left is None
        assert t.root.left.right is None
        assert t.root.right.left is None
        assert t.root.right.right is None
        return
    # balanced right first
    if value3 < value1 < value2:
        assert t.root.left.value == value3
        assert t.root.right.value == value2
        assert t.root.left.left is None
        assert t.root.left.right is None
        assert t.root.right.left is None
        assert t.root.right.right is None
        return
    # right tree
    if value1 < value2 < value3:
        assert t.root.left is None
        assert t.root.right.value == value2
        assert t.root.right.right.value == value3
        assert t.root.right.left is None
        assert t.root.right.right.right is None
        assert t.root.right.right.left is None
        return
    # right left tree
    if value1 < value2 > value3:
        assert t.root.left is None
        assert t.root.right.value == value2
        assert t.root.right.left.value == value3
        assert t.root.right.right is None
        assert t.root.right.left.left is None
        assert t.root.right.left.right is None


@pytest.mark.bst
def test_tree_len_empty():
    t = BST()
    assert len(t) == 0


@pytest.mark.bst
def test_tree_len_nonempty():
    from random import randint
    t = BST(0)
    for i in range(1, 101):
        assert len(t) == i
        t.insert_node(randint(-100, 100))
        assert len(t) == i + 1


@pytest.mark.bst
def test_tree_str_empty():
    assert str(BST()) == "None"


@pytest.mark.bst
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_str_nonempty(values):
    t = BST()
    for v in values:
        t.insert_node(v)
        assert str(t) == str(t.root)


@pytest.mark.bst
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_list_repr_nonempty(values):
    t = BST()
    for v in values:
        t.insert_node(v)
        assert t.__repr__() == str(t)


@pytest.mark.bst
def test_tree_empty_contans_nothing():
    t = BST()
    for v in range(-100, 101):
        assert v not in t


@pytest.mark.bst
def test_tree_contains_nonempty():
    from random import randint
    t = BST(0)
    assert 0 in t
    were = {0}
    while len(were) < 100:
        v = randint(-100, 100)
        if v in were:
            continue
        were.add(v)
        assert v not in t
        t.insert_node(v)
        assert v in t


@pytest.mark.bst
def test_tree_delete_from_empty_raises_exception():
    t = BST()
    with pytest.raises(ValueError):
        t.delete_node(1)


@pytest.mark.bst
@pytest.mark.parametrize("value", SINGLE_VALUES2)
def test_tree_delete_single(value):
    t = BST(value)
    assert len(t) == 1
    assert value in t
    t.delete_node(value)
    assert value not in t
    assert len(t) == 0
    assert t.root is None
    t = BST()
    t.insert_node(value)
    assert len(t) == 1
    assert value in t
    t.delete_node(value)
    assert value not in t
    assert len(t) == 0
    assert t.root is None


@pytest.mark.bst
@pytest.mark.parametrize("values", DOUBLE_VALUES)
def test_tree_2_nodes_remove_root(values):
    t = BST(values[0])
    t.insert_node(values[1])
    t.delete_node(values[0])
    assert len(t) == 1
    assert t.root == TreeNode(values[1])
    assert t.root.left is None
    assert t.root.right is None


@pytest.mark.bst
@pytest.mark.parametrize("values", DOUBLE_VALUES)
def test_tree_2_nodes_remove_leaf(values):
    t = BST(values[0])
    t.insert_node(values[1])
    t.delete_node(values[1])
    assert len(t) == 1
    assert t.root == TreeNode(values[0])
    assert t.root.left is None
    assert t.root.right is None


@pytest.mark.bst
@pytest.mark.parametrize("values", TRIPLE_VALUES)
def test_tree_3_nodes_delete_second(values):
    t = BST(values[0])
    t.insert_node(values[1])
    t.insert_node(values[2])
    t.delete_node(values[1])
    assert len(t) == 2
    assert t.root.value == values[0]
    if values[2] < values[0]:
        assert t.root.left.value == values[2]
        assert t.root.left.left is None
        assert t.root.left.right is None
        assert t.root.right is None
    else:
        assert t.root.right.value == values[2]
        assert t.root.right.left is None
        assert t.root.right.right is None
        assert t.root.left is None


@pytest.mark.bst
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_tree_delete_absent_raises_exception(values):
    t = BST()
    for v in values:
        t.insert_node(v)
    expected_len = len(values)
    assert len(t) == expected_len
    with pytest.raises(ValueError):
        t.delete_node(0xCAFEBABE)
    assert len(t) == expected_len


@pytest.mark.bst
@pytest.mark.parametrize("values", DIFFERENT_LISTS)
def test_tree_delete_present(values):
    t = BST()
    for v in values:
        t.insert_node(v)
    expected_len = len(values)

    from random import choice
    to_delete = choice(values)
    t.delete_node(to_delete)
    assert to_delete not in t
    for v in values:
        if v != to_delete:
            assert v in t
    assert len(t) == expected_len - 1


@pytest.mark.bst
def test_tree_many_inserts_and_deletions():
    t = BST()
    from random import randint
    for _ in range(100):
        v = randint(-100, 100)
        t.insert_node(v)
        t.delete_node(v)
    assert len(t) == 0



@pytest.mark.bst
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_tree_clear(values):
    t = BST()
    src_id = id(t)
    for v in values:
        t.insert_node(v)
    t.clear()
    assert len(t) == 0
    assert id(t) == src_id
    assert t.root is None



@pytest.mark.bst
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_tree_copy(values):
    t1 = BST()
    for v in values:
        t1.insert_node(v)
    t2 = t1.copy()
    assert t1 == t2
    assert id(t1) != id(t2)
    assert len(t1) == len(t2) == len(values)
    assert str(t1) == str(t2)



@pytest.mark.bst
@pytest.mark.parametrize("value", SINGLE_VALUES1)
def test_tree_count_empty(value):
    t = BST()
    assert t.count(value) == 0


@pytest.mark.bst
@pytest.mark.parametrize("values", DIFFERENT_LISTS_WITH_EMPTY)
def test_tree_count_nonempty(values):
    t = BST()
    for v in values:
        assert t.count(v) == 0
        t.insert_node(v)
        assert t.count(v) == 1
    for v in values[::-1]:
        assert t.count(v) == 1


@pytest.mark.bst
def test_tree_count_same():
    from random import randint
    t = BST()
    for _ in range(randint(0, 900)):
        t.insert_node(42)
    assert t.count(42) == len(t)

