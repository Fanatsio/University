import numpy as np

# Система уравнений, приведенная к виду F(x) = 0
def F(x):
    x1, x2 = x
    f1 = np.sin(0.2 * x2) - np.cos(0.4 * x1) + 0.1
    f2 = np.exp(-((x1 - 2) / 4)**2) * np.exp(-((x2 - 1) / 3)**2) - 0.1
    return np.array([f1, f2])

# Якобиан (матрица производных)
def J(x):
    x1, x2 = x

    df1_dx1 = 0.4 * np.sin(0.4 * x1)
    df1_dx2 = 0.2 * np.cos(0.2 * x2)

    exp_part = np.exp(-((x1 - 2) / 4)**2) * np.exp(-((x2 - 1) / 3)**2)
    df2_dx1 = exp_part * (- (x1 - 2) / 8)
    df2_dx2 = exp_part * (- 2 * (x2 - 1) / 9)

    return np.array([
        [df1_dx1, df1_dx2],
        [df2_dx1, df2_dx2]
    ])

# Неявный метод Ньютона
def newton_system(x0, eps):
    x = np.array(x0, dtype=float)
    iter = 0
    print("Начальное приближение:", x0)

    while True:
        Fx = F(x)
        Jx = J(x)

        delta = np.linalg.solve(Jx, Fx)
        x_new = x - delta

        if np.linalg.norm(x_new - x) < eps:
            print("x =", x_new)
            print("Итераций:", iter + 1)
            print("F(x) =", F(x_new))
            print("Точность (eps):", eps)
            return x_new

        x = x_new
        iter += 1

x0 = [0.888889, 3.0]
solution = newton_system(x0, eps=1e-6)