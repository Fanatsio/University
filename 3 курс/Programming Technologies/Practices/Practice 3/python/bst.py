from tree_visualizer import TreeVisualizer
from tree_node import TreeNode
class BST:
    # Функция для визуализации дерева с использованием внешней утилиты TreeVisualizer
    def visualize(self):
        TreeVisualizer.visualize(self.root)
    
    # Конструктор класса BST
    def __init__(self, value=None):
        # Инициализация корня дерева; если значение не предоставлено, корень будет None
        self.root = None if value is None else TreeNode(value)
        # Инициализация размера дерева; 0, если корень None, иначе 1
        self.size = 0 if value is None else 1
    
    # Строковое представление объекта класса BST
    def __str__(self):
        # Если корень None, возвращаем строку "None"
        if self.root is None:
            return "None"
        # Иначе возвращаем строковое представление корневого узла
        else:
            return str(self.root)

    # Метод для вставки значения в BST
    def insert_node(self, value):
        # Если корень дерева None, создаем новый узел и увеличиваем размер дерева
        if self.root is None:
            self.root = TreeNode(value)
            self.size += 1
            return
        # Иначе рекурсивно вставляем значение начиная с корня
        self._insert_recursive(self.root, value)
        self.size += 1  # Увеличиваем размер дерева на 1

    # Рекурсивный метод для вставки значения в дерево
    def _insert_recursive(self, current, value):
        # Если достигли места вставки, создаем новый узел
        if current is None:
            return TreeNode(value)
        # Если значение уже существует, увеличиваем счетчик и возвращаем узел
        elif value == current.value:
            current.count += 1  
            return current
        # Если значение меньше текущего, двигаемся влево
        elif value < current.value:
            current.left = self._insert_recursive(current.left, value)
        # Если значение больше текущего, двигаемся вправо
        elif value > current.value:
            current.right = self._insert_recursive(current.right, value)
        # Возвращаем текущий узел после вставки
        return current

    # Метод для удаления узла с определенным значением из BST
    def delete_node(self, value):
        # Если дерево пусто, вызываем исключение
        if self.root is None:
            raise ValueError("Tree is empty")
        # Иначе вызываем рекурсивную функцию удаления
        self.root = self._delete_recursive(self.root, value)

    # Рекурсивная функция для удаления узла из дерева
    def _delete_recursive(self, node, value):
        # Если узел не найден, вызываем исключение
        if node is None:
            raise ValueError("Value not found in the tree")
        # Если значение меньше текущего, идем налево
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        # Если значение больше текущего, идем направо
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        # Найден узел для удаления
        else:
            # Если у узла нет правого поддерева, возвращаем левое
            if node.left is None:
                temp = node.right
                node = None
                self.size -= 1  # Уменьшаем размер дерева
                return temp
            # Если у узла нет левого поддерева, возвращаем правое
            elif node.right is None:
                temp = node.left
                node = None
                self.size -= 1  # Уменьшаем размер дерева
                return temp
            # Если у узла есть два поддерева, находим минимальное значение в правом поддереве
            temp = self._min_value_node(node.right)
            node.value = temp.value  # Копируем значение минимального узла в текущий узел
            node.right = self._delete_recursive(node.right, temp.value)  # Удаляем минимальный узел
        return node

    # Метод для поиска узла с минимальным значением в поддереве
    def _min_value_node(self, node):
        current = node
        # Двигаемся налево до самого нижнего узла
        while current.left is not None:
            current = current.left
        return current


    # Метод для проверки наличия значения в дереве
    def __contains__(self, value):
        current = self.root
        while current:
            # Если значение найдено, возвращаем True
            if value == current.value:
                return True
            # Если искомое значение меньше текущего, переходим к левому поддереву
            elif value < current.value:
                current = current.left
            # Иначе переходим к правому поддереву
            else:
                current = current.right
        # Если значение не найдено, возвращаем False
        return False

    # Метод для получения количества узлов в дереве
    def __len__(self):
        return self.size

    # Метод для очистки дерева (удаления всех узлов)
    def clear(self):
        self.root = None
        self.size = 0

    # Метод для создания копии дерева
    def copy(self):
        new_tree = BST()
        self._copy_recursive(self.root, new_tree)
        return new_tree

    # Вспомогательный рекурсивный метод для копирования узлов из текущего дерева в новое
    def _copy_recursive(self, node, tree):
        if node is not None:
            tree.insert_node(node.value)  # Вставляем узел в новое дерево
            self._copy_recursive(node.left, tree)  # Копируем левое поддерево
            self._copy_recursive(node.right, tree)  # Копируем правое поддерево

    # Метод для подсчета количества узлов с заданным значением
    def count(self, value):
        return self._count_recursive(self.root, value)
    
    # Вспомогательный рекурсивный метод для подсчета узлов с заданным значением
    def _count_recursive(self, current, value):
        if current is None:
            return 0  # Если узел не найден, возвращаем 0
        elif value == current.value:
            return current.count  # Возвращаем количество, если значение найдено
        elif value < current.value:
            return self._count_recursive(current.left, value)  # Ищем в левом поддереве
        else:
            return self._count_recursive(current.right, value)  # Ищем в правом поддереве
    
    # Метод для строкового представления объекта класса BST
    def __repr__(self):
        return str(self)
    
    # Метод для сравнения двух объектов BST на равенство
    def __eq__(self, other):
        if not isinstance(other, BST):
            return False  # Возвращаем False, если объект не является экземпляром BST
        return self._trees_are_equal(self.root, other.root)  # Сравниваем деревья на структурное равенство

    # Вспомогательный метод для сравнения двух деревьев
    def _trees_are_equal(self, node1, node2):
        if node1 is None and node2 is None:
            return True  # Оба узла None, деревья равны
        if node1 is not None and node2 is not None:
            # Рекурсивно сравниваем значения узлов и их поддеревья
            return (node1.value == node2.value and
                    self._trees_are_equal(node1.left, node2.left) and
                    self._trees_are_equal(node1.right, node2.right))
        return False  # Узлы различаются, деревья не равны

    
    # Метод для вставки списка значений в дерево
    def insert_list(self, values):
        for value in values:  # Итерируемся по списку значений
            self.insert_node(value)  # Вставляем каждое значение в дерево с помощью уже существующего метода

    # Метод для рекурсивного прямого обхода (preorder traversal) дерева
    def recursive_preorder_traverse(self):
        return self._preorder_traverse(self.root)  # Начинаем обход с корня дерева
    
    # Вспомогательный метод для рекурсивного прямого обхода
    def _preorder_traverse(self, node):
        if node is None:  # Базовый случай: если узел отсутствует
            return []
        # Возвращаем список значений, начиная с текущего узла, затем рекурсивно левое и правое поддерево
        return [node.value] + self._preorder_traverse(node.left) + self._preorder_traverse(node.right)
    
    # Метод для итеративного прямого обхода дерева
    def iterative_preorder_traverse(self):
        if self.root is None:  # Если дерево пусто
            return []
        stack, result = [self.root], []  # Инициализация стека корневым узлом и списка для результатов
        while stack:  # Пока в стеке есть элементы
            node = stack.pop()  # Извлекаем узел из стека
            if node is not None:
                result.append(node.value)  # Добавляем значение узла в результат
                stack.append(node.right)  # Добавляем правое поддерево в стек
                stack.append(node.left)  # Добавляем левое поддерево в стек
        return result  # Возвращаем результат обхода
    
    # Метод для рекурсивного центрированного обхода (inorder traversal) дерева
    def recursive_inorder_traverse(self):
        return self._inorder_traverse(self.root)  # Начинаем обход с корня
    
    # Вспомогательный метод для рекурсивного центрированного обхода
    def _inorder_traverse(self, node):
        if node is None:  # Базовый случай: если узел отсутствует
            return []
        # Возвращаем список значений, начиная с левого поддерева, текущего узла, затем правого поддерева
        return self._inorder_traverse(node.left) + [node.value] + self._inorder_traverse(node.right)
    
    # Метод для итеративного центрированного обхода дерева
    def iterative_inorder_traverse(self):
        result, stack, current = [], [], self.root  # Инициализация списка для результатов, стека и текущего узла
        while stack or current:  # Пока в стеке есть элементы или есть текущий узел
            while current:  # Пока есть текущий узел
                stack.append(current)  # Добавляем текущий узел в стек
                current = current.left  # Перемещаемся в левое поддерево
            current = stack.pop()  # Извлекаем узел из стека
            result.append(current.value)  # Добавляем значение узла в результат
            current = current.right  # Перемещаемся в правое поддерево
        return result  # Возвращаем результат обхода
    
    # Метод для рекурсивного обратного обхода (postorder traversal) дерева
    def recursive_postorder_traverse(self):
        return self._postorder_traverse(self.root)  # Начинаем обход с корня
    
    # Вспомогательный метод для рекурсивного обратного обхода
    def _postorder_traverse(self, node):
        if node is None:  # Базовый случай: если узел отсутствует
            return []
        # Возвращаем список значений, начиная с левого поддерева, правого поддерева, затем текущего узла
        return self._postorder_traverse(node.left) + self._postorder_traverse(node.right) + [node.value]

    
    def iterative_postorder_traverse(self):
        if self.root is None:
            return []
        stack, result = [self.root], []
        while stack:
            node = stack.pop()
            if node:
                result.append(node.value)
                stack.append(node.left)
                stack.append(node.right)
        return result[::-1]  
    
    def level_order_traverse(self):
        if not self.root:
            return []
        queue, result = [self.root], []
        while queue:
            node = queue.pop(0)
            if node:
                result.append(node.value)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        return result

def generate_trees(n):
    # Если n равно 0, возвращаем список с одним элементом None, т.к. нет узлов для создания дерева
    if n == 0:
        return [None]
    # В противном случае начинаем рекурсивный процесс генерации деревьев от 1 до n
    return generate_trees_recursive(1, n)

def generate_trees_recursive(start, end):
    # Если начальное значение больше конечного, возвращаем список с одним элементом None, что обозначает отсутствие поддерева
    if start > end:
        return [None]
    # Список для хранения всех возможных уникальных BST
    all_trees = []


    # Перебираем каждое число в заданном диапазоне как корень потенциального дерева
    for i in range(start, end + 1):
        # Рекурсивно генерируем все возможные левые поддеревья для значений меньше i
        left_trees = generate_trees_recursive(start, i - 1)
        # Рекурсивно генерируем все возможные правые поддеревья для значений больше i
        right_trees = generate_trees_recursive(i + 1, end)
        
        # Комбинируем все левые и правые поддеревья с текущим узлом как корнем
        for l in left_trees:
            for r in right_trees:
                # Создаем новый узел с текущим значением i
                current_tree = TreeNode(i)
                # Назначаем левое и правое поддеревья текущему узлу
                current_tree.left = l
                current_tree.right = r
                # Добавляем текущее дерево в список всех деревьев
                all_trees.append(current_tree)
    # Возвращаем список всех сгенерированных деревьев для данного диапазона
    return all_trees

tree = generate_trees(3)
print(type(tree[0]), tree[0])

for t in tree:
    TreeVisualizer.visualize(t)


