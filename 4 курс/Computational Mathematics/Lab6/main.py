import numpy as np
import matplotlib.pyplot as plt

a = 0
b = 10
N = 150
n_values = range(1, 6)

def f(x):
    return x + 2 * np.sin(x) + np.cos(3 * x)

x_nodes = np.linspace(a, b, N)

x_tilde = x_nodes + (0.001 - 0.002 * np.random.random(len(x_nodes)))
f_tilde = f(x_tilde) + (0.01 - 0.02 * np.random.random(len(x_tilde)))

fig, axes = plt.subplots(1, len(n_values), figsize=(18, 6), sharey=True)

for idx, n in enumerate(n_values):
    coefficients = np.polyfit(x_tilde, f_tilde, n)
    S = np.poly1d(coefficients)
    x_plot = np.linspace(a, b, 5000)

    # Определяем совпадающие точки
    epsilon = 1e-1  # точность совпадения
    approx_points_x = x_tilde[np.abs(S(x_tilde) - f(x_tilde)) < epsilon]
    approx_points_y = S(approx_points_x)

    ax = axes[idx]
    ax.plot(x_plot, f(x_plot), color="blue", label="Истинная функция")
    ax.plot(x_plot, S(x_plot), color="red", label="Аппроксимация")
    ax.scatter(x_tilde, f_tilde, color="green", s=10, label="Исходные данные")
    ax.scatter(approx_points_x, approx_points_y, color="orange", s=20, label="Совпадающие точки")
    ax.set_title(f"Степень {n}")
    ax.set_xlabel("x")
    ax.grid(True)
    if idx == 0:
        ax.set_ylabel("y")
    ax.legend()

fig.suptitle(f"Среднеквадратическое приближение функции, N={N}", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.95])

plt.show()
