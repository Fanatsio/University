import pytest
from bst import BST
from recursion_detection import is_recursive

from tree_node import TreeNode


EXPECTED_PREORDER = (
    [],
    [1],
    [1, 2, 3],
    [5, 2, 1, 3, 4, 6],
    [8, 5, 1, 7, 10, 12],
    [25, 15, 10, 4, 12, 22, 18, 24, 50, 35, 31, 44, 70, 66, 90],
)

EXPECTED_POSTORDER = (
    [],
    [1],
    [3, 2, 1],
    [1, 4, 3, 2, 6, 5],
    [1, 7, 5, 12, 10, 8],
    [4, 12, 10, 18, 24, 22, 15, 31, 44, 35, 66, 90, 70, 50, 25],
)

EXPECTED_LEVELORDER = (
    [],
    [1],
    [1, 2, 3],
    [5, 2, 6, 1, 3, 4],
    [8, 5, 10, 1, 7, 12],
    [25, 15, 50, 10, 22, 35, 70, 4, 12, 18, 24, 31, 44, 66, 90],
)

TEST_TREES = (
    [],
    [1],
    [1, 2, 3],
    [5, 2, 1, 3, 6, 4],
    [8, 5, 1, 7, 10, 12],
    [25, 15, 10, 4, 12, 22, 18, 24, 50, 35, 31, 44, 70, 66, 90],
)


@pytest.mark.traversal
@pytest.mark.parametrize("tree, pre", zip(TEST_TREES, EXPECTED_PREORDER))
def test_preorder(tree, pre):
    t = BST()
    t.insert_list(tree)
    assert len(t) == len(tree)
    f_rec = lambda: t.recursive_preorder_traverse()
    f_iter = lambda: t.iterative_preorder_traverse()
    if tree:
        assert is_recursive(f_rec)
    assert not is_recursive(f_iter)
    assert f_rec() == f_iter() == pre


@pytest.mark.traversal
@pytest.mark.parametrize("tree", TEST_TREES)
def test_inorder(tree):
    t = BST()
    t.insert_list(tree)
    assert len(t) == len(tree)
    f_rec = lambda: t.recursive_inorder_traverse()
    f_iter = lambda: t.iterative_inorder_traverse()
    if tree:
        assert is_recursive(f_rec)
    assert not is_recursive(f_iter)
    assert f_rec() == f_iter() == sorted(tree)


@pytest.mark.traversal
@pytest.mark.parametrize("tree, post", zip(TEST_TREES, EXPECTED_POSTORDER))
def test_postorder(tree, post):
    t = BST()
    t.insert_list(tree)
    assert len(t) == len(tree)
    f_rec = lambda: t.recursive_postorder_traverse()
    f_iter = lambda: t.iterative_postorder_traverse()
    if tree:
        assert is_recursive(f_rec)
    assert not is_recursive(f_iter)
    assert f_rec() == f_iter() == post


@pytest.mark.traversal
@pytest.mark.parametrize("tree, level", zip(TEST_TREES, EXPECTED_LEVELORDER))
def test_levelorder(tree, level):
    t = BST()
    t.insert_list(tree)
    assert len(t) == len(tree)
    f = lambda: t.level_order_traverse()
    assert not is_recursive(f)
    assert f() == level


@pytest.mark.traversal
def test_delete_root():
    t = BST()
    t.insert_list(TEST_TREES[-1])
    assert len(t) == len(TEST_TREES[-1])
    t.delete_node(25)
    assert 25 not in t
    assert len(t) == len(TEST_TREES[-1]) - 1
    assert t.root.value == 31
    assert t.root.right.left.left is None
    assert t.recursive_preorder_traverse() == [31, 15, 10, 4, 12, 22, 18, 24, 50, 35, 44, 70, 66, 90]
    assert t.recursive_inorder_traverse() == [4, 10, 12, 15, 18, 22, 24, 31, 35, 44, 50, 66, 70, 90]
    assert t.recursive_postorder_traverse() == [4, 12, 10, 18, 24, 22, 15, 44, 35, 66, 90, 70, 50, 31]
    assert t.level_order_traverse() == [31, 15, 50, 10, 22, 35, 70, 4, 12, 18, 24, 44, 66, 90]


@pytest.mark.traversal
def test_delete_full_node():
    t = BST()
    t.insert_list(TEST_TREES[-1])
    assert len(t) == len(TEST_TREES[-1])
    t.delete_node(15)
    assert 15 not in t
    assert len(t) == len(TEST_TREES[-1]) - 1
    assert t.root.left.value == 18
    assert t.root.left.right.left is None
    assert t.recursive_preorder_traverse() == [25, 18, 10, 4, 12, 22, 24, 50, 35, 31, 44, 70, 66, 90]
    assert t.recursive_inorder_traverse() == [4, 10, 12, 18, 22, 24, 25, 31, 35, 44, 50, 66, 70, 90]
    assert t.recursive_postorder_traverse() == [4, 12, 10, 24, 22, 18, 31, 44, 35, 66, 90, 70, 50, 25]
    assert t.level_order_traverse() == [25, 18, 50, 10, 22, 35, 70, 4, 12, 24, 31, 44, 66, 90]


@pytest.mark.traversal
def test_delete_leaf():
    t = BST()
    t.insert_list(TEST_TREES[-1])
    assert len(t) == len(TEST_TREES[-1])
    t.delete_node(66)
    assert 66 not in t
    assert len(t) == len(TEST_TREES[-1]) - 1
    assert t.root.right.right.left is None
    assert t.recursive_preorder_traverse() == [25, 15, 10, 4, 12, 22, 18, 24, 50, 35, 31, 44, 70, 90]
    assert t.recursive_inorder_traverse() == [4, 10, 12, 15, 18, 22, 24, 25, 31, 35, 44, 50, 70, 90]
    assert t.recursive_postorder_traverse() == [4, 12, 10, 18, 24, 22, 15, 31, 44, 35, 90, 70, 50, 25]
    assert t.level_order_traverse() == [25, 15, 50, 10, 22, 35, 70, 4, 12, 18, 24, 31, 44, 90]




if __name__ == "__main__":
    t = BST()
    t.insert_list(TEST_TREES[-1])

    t.delete_node(66)

    print('  preorder', t.recursive_preorder_traverse())
    print('   inorder', t.recursive_inorder_traverse())
    print(' postorder', t.recursive_postorder_traverse())
    print('levelorder', t.level_order_traverse())

    t.visualize()


