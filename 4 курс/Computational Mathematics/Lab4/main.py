import numpy as np

def read_matrix_from_file(filename):
    with open(filename, 'r') as file:
        n = int(file.readline().strip())
        A = [list(map(float, line.split()[:-1])) for line in file]
    return np.array(A), n

def to_upper_triangular(A, n):
    swap_count = 0
    print("Начинаем приведение матрицы к верхнетреугольному виду:\n")

    for i in range(n):
        print(f"Шаг {i+1}: Работаем с {i+1}-м столбцом.")

        max_row = i + np.argmax(np.abs(A[i:, i]))
        if i != max_row:
            A[[i, max_row]] = A[[max_row, i]]
            swap_count += 1
            print(f"  Перестановка строк {i+1} и {max_row+1}:\n", A, "\n")
        else:
            print(f"  Строки переставлять не нужно, максимальный элемент в {i+1}-й строке.")

        if A[i, i] == 0:
            print("  Элемент на главной диагонали равен 0, матрица вырожденная.")
            return A, swap_count, True

        # Обнуление элементов ниже главного
        for j in range(i + 1, n):
            factor = A[j, i] / A[i, i]  # Коэффициент для исключения
            A[j, i:] -= factor * A[i, i:]  # Вычитание строки для получения нуля ниже главного элемента
            print(f"  Обнуляем элемент в строке {j+1}, столбце {i+1}: Коэффициент = {factor:.6f}")
            print("  Матрица после обнуления:\n", A, "\n")

    print("\nМатрица успешно приведена к верхнетреугольному виду:\n", A, "\n")
    return A, swap_count, False

def gauss_determinant(A, n):
    print("Исходная матрица:\n", A, "\n")
    A, swap_count, singular = to_upper_triangular(A, n)

    if singular:
        print("Матрица вырожденная, определитель равен 0.")
        return 0

    det = (-1) ** swap_count
    for i in range(n):
        det *= A[i, i]

    print("Определитель вычисляется как произведение диагональных элементов с учётом перестановок.")
    print(f"Количество перестановок строк: {swap_count}")
    print(f"Определитель: {det:.6f}\n")
    return det

def check_determinant(A, n, computed_det):
    true_det = np.linalg.det(A)
    print(f"Проверка с помощью NumPy: {true_det:.6f}")

    if np.isclose(computed_det, true_det):
        print("Результат вычисления определителя совпадает с проверкой.")
    else:
        print("Результат вычисления определителя НЕ совпадает с проверкой.")

filename = './Lab4/matrix_data.txt'
A, n = read_matrix_from_file(filename)

computed_det = gauss_determinant(A.copy(), n)

check_determinant(A, n, computed_det)
