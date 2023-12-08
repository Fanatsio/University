import numpy as np

#1
def max_element(arr):
    zero_indices = np.where(arr[:-1] == 0)[0]
    if len(zero_indices) == 0:
        return None
    max_after_zero = np.max(arr[zero_indices + 1])
    return max_after_zero

# Пример использования:
x = np.array([6, 2, 0, 3, 0, 0, 5, 7, 0])
result = max_element(x)
print(result)  # Вывод: 5

#2
def nearest_value(X, v):
    flattened_X = X.flatten()
    index = np.argmin(np.abs(flattened_X - v))
    return flattened_X[index]

# Пример использования:
X = np.arange(0, 10).reshape((2, 5))
v = 3.6
result = nearest_value(X, v)
print(result)  # Вывод: 4

#3
def scale(X):
    means = np.mean(X, axis=0)
    stds = np.std(X, axis=0)
    scaled_X = (X - means) / np.where(stds == 0, 1, stds)  # Предотвращение деления на ноль
    return scaled_X

# Пример использования:
random_matrix = np.random.randint(0, 10, size=(3, 4))
scaled_matrix = scale(random_matrix)
print(scaled_matrix)

#4
def get_stats(X):
    determinant = np.linalg.det(X)
    trace = np.trace(X)
    min_element = np.min(X)
    max_element = np.max(X)
    frobenius_norm = np.linalg.norm(X, 'fro')
    eigenvalues = np.linalg.eigvals(X)

    try:
        inverse_matrix = np.linalg.inv(X)
    except np.linalg.LinAlgError:
        inverse_matrix = None

    return {
        'determinant': determinant,
        'trace': trace,
        'min_element': min_element,
        'max_element': max_element,
        'frobenius_norm': frobenius_norm,
        'eigenvalues': eigenvalues,
        'inverse_matrix': inverse_matrix
    }


# Пример использования:
random_matrix = np.random.randn(3, 3)
stats = get_stats(random_matrix)
for key, value in stats.items():
    print(f'{key}: {value}')


#5
max_elements = []

for exp_num in range(100):
    # Генерация двух матриц 10x10 из стандартного нормального распределения
    matrix1 = np.random.randn(10, 10)
    matrix2 = np.random.randn(10, 10)

    # Перемножение матриц
    result_matrix = np.dot(matrix1, matrix2)

    # Нахождение максимального элемента
    max_element = np.max(result_matrix)

    max_elements.append(max_element)

# Вычисление среднего значения и 95-процентной квантили
mean_max_element = np.mean(max_elements)
quantile_95 = np.percentile(max_elements, 95)

print(f'Среднее значение максимальных элементов: {mean_max_element}')
print(f'95-процентная квантиль максимальных элементов: {quantile_95}')