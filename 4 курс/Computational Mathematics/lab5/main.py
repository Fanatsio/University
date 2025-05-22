import numpy as np

def read_matrix_from_file(filename):
    with open(filename, 'r') as file:
        _ = int(file.readline().strip())
        A = []
        b = []
        
        for line in file:
            *row, bi = map(float, line.split())
            A.append(row)
            b.append(bi)
        
        A = np.array(A)
        b = np.array(b)
        
    return A, b

def seidel(A, b, epsilon=1e-4, max_iter=1000):
    m = len(A)
    x = np.zeros(m)
    count = 0
    while True:
        x_new = np.copy(x)
        for i in range(m):
            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i + 1, m))
            if A[i][i] == 0.0:
                print(f"Элемент A[{i}][{i}] равен нулю. Метод Зейделя не применим.")
                break
            x_new[i] = (b[i] - s1 - s2) / A[i][i]

        print(f"Итерация {count}: x = {x_new}")
        pogr = sum(abs(x_new[i] - x[i]) for i in range(m))
        if pogr < epsilon:
            return count, x_new, pogr

        x = x_new
        count += 1    

        if count >= max_iter:
            raise ValueError("Метод не сходится за заданное количество итераций.")

def calculate_residuals(A, b, x):
    residuals = np.dot(A, x) - b
    return np.dot(A, x), residuals

def verify_solution(a, x):
    return [sum(a[i][j] * x[j] for j in range(len(x))) for i in range(len(a))]

filename = './lab5/matrix_data.txt'
A, b = read_matrix_from_file(filename)

print(f"Исходная матрица A:\n{A}")
print(f"\nВектор свободных членов b:\n{b}\n")

count, x, pogr = seidel(A, b)

print(f"\nКоличество итераций: {count}")
print(f"Решение системы уравнений: {x}")
print(f"Общее значение невязки (погрешности): {pogr}")

Ax, residuals = calculate_residuals(A, b, x)

print("\nПроверка решения (A * x):")
print(f"Истинные значения b: {b}")
print(f"Полученные значения A * x: {Ax}")
print(f"Невязка для каждого уравнения: {residuals}")
