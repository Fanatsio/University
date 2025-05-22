import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def calculate_taylor_coefficients(func, point, n_terms):
    """
    Рассчитывает коэффициенты ряда Тейлора для функции в заданной точке.

    Parameters:
    func (sympy.Expr): Исходная функция.
    point (float): Точка, в которой вычисляется ряд Тейлора.
    n_terms (int): Количество членов в ряде Тейлора.

    Returns:
    list: Список коэффициентов ряда Тейлора.
    """
    x = sp.symbols('x')
    taylor_coeffs = []
    for i in range(n_terms):
        coeff = func.diff(x, i).subs(x, point) / sp.factorial(i)
        taylor_coeffs.append(coeff)
    return taylor_coeffs

def print_taylor_coefficients(coeffs):
    """
    Выводит коэффициенты ряда Тейлора на экран в красивом формате.

    Parameters:
    coeffs (list): Коэффициенты ряда Тейлора.

    Returns:
    None
    """
    print("Тейлоровские коэффициенты:")
    for i, coeff in enumerate(coeffs):
        print(f"n={i}: {sp.pretty(coeff)}")

def evaluate_taylor_series(coeffs, point, x_values):
    """
    Вычисляет значения ряда Тейлора для заданных значений x.

    Parameters:
    coeffs (list): Коэффициенты ряда Тейлора.
    point (float): Точка, в которой вычисляется ряд Тейлора.
    x_values (array-like): Массив значений x, для которых нужно вычислить значения ряда Тейлора.

    Returns:
    ndarray: Массив значений ряда Тейлора для соответствующих значений x.
    """
    taylor_values = []
    for x in x_values:
        taylor_sum = sum(coeff * (x - point)**i for i, coeff in enumerate(coeffs))
        taylor_values.append(taylor_sum)
    return np.array(taylor_values)

if __name__ == "__main__":
    x = sp.symbols('x')
    func = sp.exp(x)
    expansion_point = 0
    n_terms_values = [3, 5, 10, 25, 50]

    for n_terms in n_terms_values:
        taylor_coeffs = calculate_taylor_coefficients(func, expansion_point, n_terms)
        print(f"Для n={n_terms}:")
        print_taylor_coefficients(taylor_coeffs)
        print()

    x_values = np.linspace(-5, 5, 100)
    y_analytical = np.exp(x_values)

    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_analytical, label='Аналитическое решение')

    for n_terms in n_terms_values:
        taylor_coeffs = calculate_taylor_coefficients(func, expansion_point, n_terms)
        y_taylor = evaluate_taylor_series(taylor_coeffs, expansion_point, x_values)
        plt.plot(x_values, y_taylor, label=f'Ряд Тейлора (n={n_terms})')

    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Аппроксимация функции $e^x$ с помощью ряда Тейлора')
    plt.legend()
    plt.grid(True)
    plt.show()
