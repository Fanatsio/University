import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

def f(x):
    return x + 2 * np.sin(x) + np.cos(3 * x)

def simpson_method(a, b, f, epsilon, true_value=None):
    n = 5  # Начальное количество сегментов (чётное число)
    h = (b - a) / n  # Начальный шаг
    
    integral_old = (f(a) + f(b)) / 2.0
    iterations = 0

    print("Шаги метода Симпсона:")
    
    while True:
        integral_new = 0
        sum_odd = sum(f(a + (2 * i - 1) * h) for i in range(1, n // 2 + 1))
        sum_even = sum(f(a + 2 * i * h) for i in range(1, n // 2))
        integral_new = (f(a) + f(b) + 4 * sum_odd + 2 * sum_even) * h / 3

        iterations += 1
        print(f"Итерация {iterations}: n = {n}, интеграл ≈ {integral_new}")

        if abs(integral_new - integral_old) < epsilon:
            break

        n *= 2
        h /= 2
        integral_old = integral_new
    
    return integral_new

a = 0
b = np.pi
epsilon = 1e-10

true_value, _ = quad(f, a, b)

integral_value = simpson_method(a, b, f, epsilon, true_value=true_value)

print(f"\nИнтеграл с точностью {epsilon}: {integral_value}")
print(f"Точный результат (с использованием quad): {true_value}")
print(f"Абсолютная ошибка между результатами: {abs(true_value - integral_value)}")

x_vals = np.linspace(a, b, 1000)
y_vals = f(x_vals)

plt.plot(x_vals, y_vals, label="f(x) = x + 2sin(x) + cos(3x)", color='b')
plt.fill_between(x_vals, 0, y_vals, color='lightblue', alpha=0.5, label="Область под графиком")

plt.title("График функции f(x) с областью под графиком (интеграл)")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid(True)
plt.show()
