import numpy as np
from functions import phi

def gradient(x, h=1e-6):
    """Вычисление градиента численным методом"""
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[i] += h
        x_minus[i] -= h
        grad[i] = (phi(x_plus) - phi(x_minus)) / (2 * h)
    return grad

def golden_section_minimize(func, a, b, eps=1e-6):
    """Минимизация функции одной переменной методом золотого сечения"""
    tau = (np.sqrt(5) - 1) / 2
    c = b - tau * (b - a)
    d = a + tau * (b - a)
    
    while abs(b - a) > eps:
        if func(c) < func(d):
            b = d
        else:
            a = c
        
        c = b - tau * (b - a)
        d = a + tau * (b - a)
    
    return (a + b) / 2

def coordinate_descent(x0, eps=1e-6, max_iter=1000, callback=None):
    """Метод покоординатного спуска"""
    x = np.array(x0, dtype=float)
    history = [x.copy()]
    k = 0
    
    while k < max_iter:
        x_prev = x.copy()
        
        # Цикл по координатам
        for i in range(len(x)):
            # Минимизация по i-ой координате
            def phi_i(alpha):
                x_temp = x.copy()
                x_temp[i] = alpha
                return phi(x_temp)
            
            # Определяем интервал для поиска
            step = 1.0
            a, b = x[i] - step, x[i] + step
            
            # Расширяем интервал, если минимум на границах
            for _ in range(5):
                if phi_i(a) < phi_i(x[i]) or phi_i(b) < phi_i(x[i]):
                    step *= 2
                    a, b = x[i] - step, x[i] + step
                else:
                    break
            
            # Одномерная минимизация
            x[i] = golden_section_minimize(phi_i, a, b, eps / 10)
        
        # Вычисляем норму разности и градиент
        diff_norm = np.linalg.norm(x - x_prev)
        grad = gradient(x)
        grad_norm = np.linalg.norm(grad)
        
        # Вызываем callback если предоставлен
        if callback:
            callback(k, x, phi(x), grad_norm, diff_norm)
        
        history.append(x.copy())
        
        # Проверка критерия выхода
        if diff_norm < eps:
            break
            
        k += 1
    
    return x, k+1, phi(x), grad_norm, eps, np.array(history)