import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x + 2 * np.sin(x) + np.cos(3 * x)

def f_prime(x):
    return 1 + 2 * np.cos(x) - 3 * np.sin(3 * x)

def f_double_prime(x):
    return -2 * np.sin(x) - 9 * np.cos(3 * x)

def plot_function_with_parabola(x0):
    x_vals = np.linspace(-2, 2, 1000)
    y_vals = f(x_vals)

    parabola = (
        f(x0) + f_prime(x0) * (x_vals - x0) + 0.5 * f_double_prime(x0) * (x_vals - x0)**2
    )

    plt.plot(x_vals, y_vals, label="f(x)", color="blue")
    plt.plot(x_vals, parabola, '--', label="Taylor parabola", color="orange")
    plt.scatter([x0], [f(x0)], color="red", label=f"x0 = {x0:.4f}")
    plt.axhline(0, color="black", linewidth=0.5)
    plt.axvline(0, color="black", linewidth=0.5)
    plt.legend()
    plt.grid()
    plt.title("Метод параболы")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.show()

def parabola_method(a, b, eps=1e-4, max_iter=1000):
    x0 = b
    for k in range(max_iter):
        x1 = (a + b) / 2
        fx1 = f(x1)

        print(f"Итерация {k+1:3d}: x = {x1: .6f}, f(x) = {fx1: .10f}, точность = {eps:.1e}")

        if abs(x1 - x0) < eps:
            plot_function_with_parabola(x0)
            print(f"Решение найдено: x = {x1:.6f}, f(x) = {fx1:.10f}, количество итераций = {k+1}, точность = {eps}")
            return x1, k+1

        if np.sign(f(a)) * np.sign(fx1) < 0:
            b = x1
        else:
            a = x1

        x0 = x1

    plot_function_with_parabola(x0)
    print(f"Решение не найдено за {max_iter} итераций, точность = {eps}")
    return None, max_iter

a, b = -1, 0

parabola_method(a, b)
