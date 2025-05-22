import pytest
from test_data import *

from tree_node import TreeNode


@pytest.mark.treenode
@pytest.mark.parametrize("value", [*SINGLE_VALUES1, *SINGLE_VALUES2])
def test_single_node_init(value):
    n = TreeNode(value)
    assert isinstance(n, TreeNode)
    assert n.value == value
    assert n.left is None
    assert n.right is None


@pytest.mark.treenode
def test_wrong_init_raises_exception():
    with pytest.raises(TypeError):
        TreeNode(1, 2)
    with pytest.raises(TypeError):
        TreeNode(1, 0.2)
    with pytest.raises(TypeError):
        TreeNode(1, "2")
    with pytest.raises(TypeError):
        TreeNode(1, [2])
    with pytest.raises(TypeError):
        TreeNode(1, (2))
    with pytest.raises(TypeError):
        TreeNode(1, {2})
    with pytest.raises(TypeError):
        TreeNode(1, {2: 2})


@pytest.mark.treenode
@pytest.mark.parametrize("value1, value2", DOUBLE_VALUES)
def test_left_node_init(value1, value2):
    lft = TreeNode(value2)
    n = TreeNode(value1, left=lft)
    assert isinstance(n, TreeNode)
    assert isinstance(n.left, TreeNode)
    assert n.value == value1
    assert n.left.value == value2
    assert n.right is None
    assert n.left.left is None
    assert n.left.right is None


@pytest.mark.treenode
@pytest.mark.parametrize("value1, value2", DOUBLE_VALUES)
def test_right_node_init(value1, value2):
    rgt = TreeNode(value2)
    n = TreeNode(value1, right=rgt)
    assert isinstance(n, TreeNode)
    assert isinstance(n.right, TreeNode)
    assert n.value == value1
    assert n.right.value == value2
    assert n.left is None
    assert n.right.left is None
    assert n.right.right is None


@pytest.mark.treenode
@pytest.mark.parametrize("value1, value2, value3", TRIPLE_VALUES)
def test_both_node_init(value1, value2, value3):
    lft = TreeNode(value3)
    rgt = TreeNode(value2)
    n = TreeNode(value1, right=rgt, left=lft)
    assert isinstance(n, TreeNode)
    assert isinstance(n.left, TreeNode)
    assert isinstance(n.right, TreeNode)
    assert n.value == value1
    assert n.right.value == value2
    assert n.left.value == value3
    assert n.left.left is None
    assert n.left.right is None
    assert n.right.left is None
    assert n.right.right is None


#     0
#   1   2
# 3       4
@pytest.mark.treenode
@pytest.mark.parametrize("values", [SINGLE_VALUES1, SINGLE_VALUES2])
def test_5_node_init(values):
    n = TreeNode(
        values[0],
        left=TreeNode(values[1], left=TreeNode(values[3])),
        right=TreeNode(values[2], right=TreeNode(values[4])),
    )
    assert isinstance(n, TreeNode)
    assert isinstance(n.left, TreeNode)
    assert isinstance(n.right, TreeNode)
    assert isinstance(n.left.left, TreeNode)
    assert n.left.right is None
    assert isinstance(n.right.right, TreeNode)
    assert n.right.left is None
    assert n.value == values[0]
    assert n.left.value == values[1]
    assert n.right.value == values[2]
    assert n.left.left.value == values[3]
    assert n.right.right.value == values[4]
    assert n.left.left.left is None
    assert n.left.left.right is None
    assert n.right.right.left is None
    assert n.right.right.right is None


@pytest.mark.treenode
@pytest.mark.parametrize("value", SINGLE_VALUES2)
def test_single_node_str(value):
    n = TreeNode(value)
    assert str(n) == f"({value})"


@pytest.mark.treenode
@pytest.mark.parametrize("value1, value2, value3", TRIPLE_VALUES)
def test_triple_node_str(value1, value2, value3):
    n = TreeNode(value1, left=TreeNode(value2), right=TreeNode(value3))
    assert str(n) == f"({value1}, l -> ({value2}), r -> ({value3}))"

    n = TreeNode(value1, left=TreeNode(value2, right=TreeNode(value3)))
    assert str(n) == f"({value1}, l -> ({value2}, r -> ({value3})))"

    n = TreeNode(value1, left=TreeNode(value2, left=TreeNode(value3)))
    assert str(n) == f"({value1}, l -> ({value2}, l -> ({value3})))"

    n = TreeNode(value1, right=TreeNode(value2, right=TreeNode(value3)))
    assert str(n) == f"({value1}, r -> ({value2}, r -> ({value3})))"


@pytest.mark.treenode
@pytest.mark.parametrize("value", SINGLE_VALUES1)
def test_single_node_not_eq(value):
    node1 = TreeNode(value)
    node2 = TreeNode(value + 1)
    assert node1 != node2

    node1 = TreeNode(value)
    node2 = value
    assert node1 != node2


@pytest.mark.treenode
@pytest.mark.parametrize("value", SINGLE_VALUES2)
def test_single_node_eq(value):
    node1 = TreeNode(value)
    node2 = TreeNode(value)
    assert node1 == node2


@pytest.mark.treenode
@pytest.mark.parametrize("value1, value2", DOUBLE_VALUES)
def test_double_node_not_eq(value1, value2):
    node1 = TreeNode(value1, left=TreeNode(value2))
    node2 = TreeNode(value1, left=TreeNode(value2 - 1))
    assert node1 != node2

    node1 = TreeNode(value1, left=TreeNode(value2))
    node2 = TreeNode(value1, right=TreeNode(value2))
    assert node1 != node2


@pytest.mark.treenode
@pytest.mark.parametrize("value1, value2", DOUBLE_VALUES)
def test_double_node_eq(value1, value2):
    node1 = TreeNode(value1, left=TreeNode(value2))
    node2 = TreeNode(value1, left=TreeNode(value2))
    assert node1 == node2

    node1 = TreeNode(value1, right=TreeNode(value2))
    node2 = TreeNode(value1, right=TreeNode(value2))
    assert node1 == node2


@pytest.mark.treenode
@pytest.mark.parametrize("value1, value2, value3", TRIPLE_VALUES)
def test_triple_node_not_eq(value1, value2, value3):
    n1 = TreeNode(value1, left=TreeNode(value2), right=TreeNode(value3))
    n2 = TreeNode(value1 + 1, left=TreeNode(value2), right=TreeNode(value3))
    assert n1 != n2

    n1 = TreeNode(value1, left=TreeNode(value2), right=TreeNode(value3))
    n2 = TreeNode(value1, left=TreeNode(value2 + 1), right=TreeNode(value3))
    assert n1 != n2

    n1 = TreeNode(value1, left=TreeNode(value2), right=TreeNode(value3))
    n2 = TreeNode(value1, left=TreeNode(value2), right=TreeNode(value3 + 1))
    assert n1 != n2

    n1 = TreeNode(value1, left=TreeNode(value2), right=TreeNode(value3))
    n2 = TreeNode(value1, right=TreeNode(value2), left=TreeNode(value3))
    assert n1 != n2


@pytest.mark.treenode
@pytest.mark.parametrize("value1, value2, value3", TRIPLE_VALUES)
def test_triple_node_eq(value1, value2, value3):
    n1 = TreeNode(value1, left=TreeNode(value2), right=TreeNode(value3))
    n2 = TreeNode(value1, left=TreeNode(value2), right=TreeNode(value3))
    assert n1 == n2


@pytest.mark.treenode
@pytest.mark.parametrize("values", [SINGLE_VALUES1, SINGLE_VALUES2])
def test_5_node_not_eq(values):
    n1 = TreeNode(
        values[0],
        left=TreeNode(values[1], left=TreeNode(values[3])),
        right=TreeNode(values[2], right=TreeNode(values[4])),
    )
    n2 = TreeNode(
        values[0],
        left=TreeNode(values[1], left=TreeNode(values[3])),
        right=TreeNode(values[2], right=TreeNode(values[4] + 1)),
    )
    assert n1 != n2

    n1 = TreeNode(
        values[0],
        left=TreeNode(values[1], left=TreeNode(values[3])),
        right=TreeNode(values[2], right=TreeNode(values[4])),
    )
    n2 = TreeNode(
        values[0],
        left=TreeNode(values[1], left=TreeNode(values[3])),
        right=TreeNode(values[2], left=TreeNode(values[4])),
    )
    assert n1 != n2


@pytest.mark.treenode
@pytest.mark.parametrize("values", [SINGLE_VALUES1, SINGLE_VALUES2])
def test_5_node_eq(values):
    n1 = TreeNode(
        values[0],
        left=TreeNode(values[1], left=TreeNode(values[3])),
        right=TreeNode(values[2], right=TreeNode(values[4])),
    )
    n2 = TreeNode(
        values[0],
        left=TreeNode(values[1], left=TreeNode(values[3])),
        right=TreeNode(values[2], right=TreeNode(values[4])),
    )
    assert n1 == n2
