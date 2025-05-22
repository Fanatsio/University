import numpy as np
import matplotlib.pyplot as plt

# Функция для генерации ступенчатого сигнала в диапазоне [a, b)
def step_signal(x, a, b):
    return np.where((a <= x) & (x < b), 1, 0)

# Функция для вычисления свёртки двух дискретных сигналов
def convolution(f, g):
    N = len(f)
    M = len(g)
    result = np.zeros(N + M - 1)  # Размер результата N + M - 1

    for n in range(N + M - 1):  # Вычисление свёртки вручную
        sum_value = 0
        for k in range(N):
            if 0 <= n - k < M:
                sum_value += f[k] * g[n - k]
        result[n] = sum_value
    
    return result

# Создаём массив значений x от -1 до 3 с шагом 0.01
x = np.arange(-1, 3, 0.01)

# Генерируем два одинаковых ступенчатых сигнала
f_signal = step_signal(x, 0, 1)
g_signal = step_signal(x, 0, 1)

# Вычисляем их свёртку
conv_result = convolution(f_signal, g_signal)

# Корректируем оси для результата свёртки
conv_x = np.arange(-2, 4, 0.01)[:len(conv_result)]

# Исправленный участок: обрезаем x до нужного размера
conv_x = np.linspace(2 * x[0], 2 * x[-1], len(conv_result))

# Строим графики
plt.figure(figsize=(10, 6))

# График первого сигнала
plt.subplot(3, 1, 1)
plt.plot(x, f_signal, label='f(x)')
plt.legend()

# График второго сигнала
plt.subplot(3, 1, 2)
plt.plot(x, g_signal, label='g(x)')
plt.legend()

# График результата свёртки
plt.subplot(3, 1, 3)
plt.plot(conv_x, conv_result, label='(f * g)(x)')
plt.legend()

plt.tight_layout()
plt.show()
