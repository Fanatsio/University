import pytest
from test_data import *

from bst import BST
from tree_node import TreeNode
from bst import generate_trees
from tree_visualizer import *

# Тестирование инициализации пустого BST
@pytest.mark.bst
def test_tree_init_empty():
    t1 = BST()
    # Проверка, что t1 является экземпляром класса BST
    assert isinstance(t1, BST)
    # Проверка, что корневой узел t1 отсутствует
    assert t1.root is None
    t2 = BST(None)
    # Проверка, что t2 также является экземпляром BST
    assert isinstance(t2, BST)
    # Проверка, что корневой узел t2 также отсутствует
    assert t2.root is None

# Тестирование инициализации BST с одним узлом
@pytest.mark.bst
@pytest.mark.parametrize("value", SINGLE_VALUES1)
def test_tree_init_nonempty(value):
    t = BST(value)
    # Проверка, что объект t является экземпляром BST
    assert isinstance(t, BST)
    # Проверка, что корневой узел t является экземпляром TreeNode
    assert isinstance(t.root, TreeNode)
    # Проверка, что значение корневого узла равно переданному значению
    assert t.root.value == value
    # Проверка, что у корневого узла нет левого поддерева
    assert t.root.left is None
    # Проверка, что у корневого узла нет правого поддерева
    assert t.root.right is None

# Тест для проверки длины пустого дерева
@pytest.mark.bst
def test_tree_len_empty():
    t = BST()
    # Проверка, что длина пустого дерева равна 0
    assert len(t) == 0

# Функция для проверки, что дерево является BST
def is_bst(node, lower = float('-inf'), upper=float('inf')):
    if not node:
        return True
    val = node.value
    if val <= lower or val >= upper:
        return False
    if not is_bst(node.right, val, upper):
        return False
    if not is_bst(node.left, lower, val):
        return False
    return True



# Функция для проверки уникальности всех деревьев
def are_all_trees_unique(trees):
    seen = set()
    for tree in trees:
        structure = serialize_tree(tree)
        if structure in seen:
            return False
        seen.add(structure)
    return True

def serialize_tree(node):
    if not node:
        return "None"
    return f"{node.value}({serialize_tree(node.left)},{serialize_tree(node.right)})"

@pytest.mark.parametrize("n, expected_count", [
    (0, 1),
    (1, 1),
    (2, 2),
    (3, 5),
    (4, 14),
    (5, 42)
])
def test_generate_trees(n, expected_count):
    trees = generate_trees(n)
    assert len(trees) == expected_count, f"Expected {expected_count} trees for n={n}, got {len(trees)}"
    assert all(is_bst(tree) for tree in trees), "All trees must be valid BSTs"
    assert are_all_trees_unique(trees), "All trees must be structurally unique"

