class TreeNode:
    def __init__(self, value, left=None, right=None):
        # Проверка типов для аргументов left и right; должны быть либо None, либо экземпляры TreeNode
        allowed_types = (type(None), TreeNode)
        if not isinstance(left, allowed_types) or not isinstance(right, allowed_types):
            raise TypeError("Invalid argument type for 'left' or 'right'.")
        # Инициализация атрибутов узла: значение, левый и правый дочерние узлы
        self.value = value
        self.left = left
        self.right = right
        # Счётчик для поддержки возможных дубликатов значения в узле 
        self.count = 1

    def __str__(self):
        # Начинаем собирать строковое представление узла
        parts = [f"({self.value}"]
        # Добавляем представление левого и правого дочерних узлов, если они существуют
        if self.left or self.right:
            if self.left:
                parts.append(f", l -> {self.left}")
            if self.right:
                parts.append(f", r -> {self.right}")
        # Закрываем скобку для текущего узла
        parts.append(")")
        return "".join(parts)

    def __eq__(self, other):
        # Проверяем, является ли other экземпляром TreeNode
        if not isinstance(other, TreeNode):
            return False
        # Сравниваем текущий узел с другим узлом по значению и рекурсивно по левому и правому дочерним узлам
        return (self.value == other.value and
                self.left == other.left and
                self.right == other.right)

    def __repr__(self):
        # Возвращаем строковое представление узла (используется в отладочных целях)
        return self.__str__()

    def __ne__(self, value):
        # Определяем неэквивалентность на основе метода __eq__
        return not self == value
