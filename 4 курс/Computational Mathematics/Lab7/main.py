import numpy as np
import matplotlib.pyplot as plt

def compute_function(value):
    return value + 2 * np.sin(value) + np.cos(3 * value)

def exact_first_derivative(value):
    return 1 + 2 * np.cos(value) - 3 * np.sin(3 * value)

def exact_second_derivative(value):
    return -2 * np.sin(value) - 9 * np.cos(3 * value)

# Численные методы вычисления второй производной
def numerical_derivative_2nd_order(func, point, step):
    return (func(point + step) - 2 * func(point) + func(point - step)) / (step ** 2)

def numerical_derivative_4th_order(func, point, step):
    return (-func(point + 2 * step) + 16 * func(point + step) - 30 * func(point) + \
            16 * func(point - step) - func(point - 2 * step)) / (12 * step ** 2)

# Метод Рунге для оценки погрешности
def runge_estimation(result_1, result_2, accuracy_order):
    return abs(result_1 - result_2) / (2 ** accuracy_order - 1)

calculation_point = 2.5
step_sizes = [0.1, 0.01, 0.025]
x_range = np.linspace(0, 6, 1000)

plt.figure(figsize=(10, 6))
plt.plot(x_range, compute_function(x_range), label="f(x)")
plt.plot(x_range, exact_second_derivative(x_range), label="Точная f''(x)", color='orange')
plt.title("Функция и вторая производная")
plt.xlabel("x")
plt.ylabel("Значение")
plt.legend()
plt.grid()
plt.show()

results_log = []

def log_results(point, label):
    for step in step_sizes:
        second_order_result = numerical_derivative_2nd_order(compute_function, point, step)
        refined_second_order_result = numerical_derivative_2nd_order(compute_function, point, step / 2)
        error_2nd = runge_estimation(second_order_result, refined_second_order_result, 2)

        fourth_order_result = numerical_derivative_4th_order(compute_function, point, step)
        refined_fourth_order_result = numerical_derivative_4th_order(compute_function, point, step / 2)
        error_4th = runge_estimation(fourth_order_result, refined_fourth_order_result, 4)

        exact_value = exact_second_derivative(point)

        results_log.append(f"Точка: {label}, шаг: {step}")
        results_log.append(f"2-й порядок: f''(x) = {second_order_result}, ошибка Рунге = {error_2nd}")
        results_log.append(f"4-й порядок: f''(x) = {fourth_order_result}, ошибка Рунге = {error_4th}")
        results_log.append(f"Точное значение: f''(x) = {exact_value}")
        results_log.append("-")

log_results(calculation_point, "x~")
print("\n".join(results_log))

plt.figure(figsize=(10, 6))
plt.plot(x_range, exact_second_derivative(x_range), label="Точная f''(x)", color='orange')

for step in step_sizes:
    second_order_value = numerical_derivative_2nd_order(compute_function, calculation_point, step)
    fourth_order_value = numerical_derivative_4th_order(compute_function, calculation_point, step)
    plt.scatter([calculation_point], [second_order_value], label=f"2-й порядок, шаг={step}", marker='o', zorder=5)
    plt.scatter([calculation_point], [fourth_order_value], label=f"4-й порядок, шаг={step}", marker='s', zorder=5)

plt.title("Сравнение точной и численных производных")
plt.xlabel("x")
plt.ylabel("Значение")
plt.legend()
plt.grid()
plt.show()
