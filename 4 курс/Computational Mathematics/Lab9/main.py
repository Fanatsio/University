import numpy as np
import time

CONFIG = {
    "eps": 1e-6,
    "max_iter": 100,
    "x0": np.array([-2., -2.])
}

def F(x: np.ndarray) -> np.ndarray:
    x1, x2 = x
    return np.array([
        np.sin(0.2 * x2) - np.cos(0.4 * x1) + 0.1,
        np.exp(-((x1 - 2) / 4) ** 2 - ((x2 - 1) / 3) ** 2) - 0.1
    ])

def J(x: np.ndarray) -> np.ndarray:
    x1, x2 = x
    e_part = np.exp(-((x1 - 2) / 4) ** 2 - ((x2 - 1) / 3) ** 2)

    df1_dx1 = 0.4 * np.sin(0.4 * x1)
    df1_dx2 = 0.2 * np.cos(0.2 * x2)
    df2_dx1 = e_part * (-2 * (x1 - 2) / 16)
    df2_dx2 = e_part * (-2 * (x2 - 1) / 9)
 
    return np.array([[df1_dx1, df1_dx2], [df2_dx1, df2_dx2]])

def newton_implicit(F, J, x0: np.ndarray, eps=1e-6, max_iter=100):
    x = x0.copy()
    history = []
    start_time = time.time()

    for k in range(max_iter):
        Fx = F(x)
        Jx = J(x)
        detJ = np.linalg.det(Jx)

        if abs(detJ) < 1e-10:
            raise np.linalg.LinAlgError(f"Якобиан вырожден на итерации {k}, det(J)={detJ:.3e}")

        dx = np.linalg.solve(Jx, -Fx)
        x_new = x + dx
        norm_dx = np.linalg.norm(dx)
        history.append((k + 1, x[0], x[1], norm_dx))

        if norm_dx < eps:
            elapsed = time.time() - start_time
            return x_new, k + 1, F(x_new), eps, history, elapsed

        x = x_new

    elapsed = time.time() - start_time
    raise Exception(f"Метод Ньютона не сошёлся за {max_iter} итераций. Последнее x={x}, ||F(x)||={np.linalg.norm(F(x)):.3e}, время={elapsed:.2f} c")

def print_results(result, x0):
    print("\n" + "=" * 50)
    print("        РЕЗУЛЬТАТЫ РАБОТЫ МЕТОДА НЬЮТОНА")
    print("=" * 50)

    print(f"Начальное приближение: x₀ = [{x0[0]:.4f}, {x0[1]:.4f}]")
    print(f"Количество итераций:   {result[1]}")
    print(f"Найденное решение:     x* = [{result[0][0]:.6f}, {result[0][1]:.6f}]")
    print(f"Вектор невязки:        F(x*) = [{result[2][0]:.3e}, {result[2][1]:.3e}]")
    print(f"Точность ε:            {result[3]}")
    print(f"Время выполнения:      {result[5]:.6f} c\n")

    print("-" * 50)
    print(f"{'k':<5}{'x1':>12}{'x2':>12}{'||Δx||':>12}")
    print("-" * 50)
    for k, x1, x2, dx_norm in result[4]:
        print(f"{k:<5}{x1:>12.6f}{x2:>12.6f}{dx_norm:>12.3e}")
    print("-" * 50)
    print("✅ Метод Ньютона успешно сошёлся!")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    x0 = CONFIG["x0"]
    result = newton_implicit(F, J, x0, eps=CONFIG["eps"], max_iter=CONFIG["max_iter"])
    print_results(result, x0)
