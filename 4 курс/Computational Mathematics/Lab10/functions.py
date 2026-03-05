import numpy as np

def f1(x1, x2):
    """Первая функция системы"""
    return np.sin(0.2 * x2) - np.cos(0.4 * x1) + 0.1

def f2(x1, x2):
    """Вторая функция системы"""
    return np.exp(-((x1 - 2) / 4) ** 2) * np.exp(-((x2 - 1) / 3) ** 2) - 0.1

def phi(x):
    """Целевая функция Φ(x,y) = f1² + f2²"""
    x1, x2 = x[0], x[1]
    return f1(x1, x2)**2 + f2(x1, x2)**2