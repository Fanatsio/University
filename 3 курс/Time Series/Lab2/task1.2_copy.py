import matplotlib.pyplot as plt
import numpy as np

# Функция для генерации ступенчатого сигнала в диапазоне [a, b)
def step_signal(x, a, b):
    return np.where((a <= x) & (x < b), 1, 0)

# Создаем массив значений x от -1 до 3 с шагом 0.01
x = np.arange(-1, 3, 0.01)

# Генерируем два одинаковых ступенчатых сигнала
f_signal = step_signal(x, 0, 1)
g_signal = step_signal(x, 0, 1)

# Вычисляем свертку сигналов с помощью встроенной функции numpy
conv_result = np.convolve(f_signal, g_signal, mode='full')

# Корректируем ось X для результата свёртки
conv_x = np.linspace(2 * x[0], 2 * x[-1], len(conv_result))

# Создаем фигуру для отображения графиков
plt.figure(figsize=(10, 6))

# График первого сигнала
plt.subplot(3, 1, 1)
plt.plot(x, f_signal, label='f(x)')
plt.legend()
plt.title('Первый ступенчатый сигнал')

# График второго сигнала
plt.subplot(3, 1, 2)
plt.plot(x, g_signal, label='g(x)')
plt.legend()
plt.title('Второй ступенчатый сигнал')

# График результата свертки
plt.subplot(3, 1, 3)
plt.plot(conv_x, conv_result, label='(f * g)(x)')
plt.legend()
plt.title('Результат свертки сигналов')

# Улучшаем расположение графиков
plt.tight_layout()
plt.show()
