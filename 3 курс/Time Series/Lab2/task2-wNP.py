import numpy as np
import matplotlib.pyplot as plt

# Функция g1: сумма косинуса и синуса
def g1(x):
    return np.cos(3 * x) + np.sin(x)

# Функция g2: гауссовская экспонента
def g2(x):
    return np.exp(-0.5 * x**2)

# Функция g3: тангенс с условием Хевисайда
def g3(x):
    return np.tan(x) * np.heaviside(x, 0.5)

# Функция g4: сумма абсолютного косинуса и логарифма
def g4(x):
    return np.abs(np.cos(x)) + np.log1p(np.abs(x))

# Функция g5: гиперболический синус, деленный на 1 + гиперболический косинус
def g5(x):
    return np.sinh(x) / (1 + np.cosh(x))

# Функция вычисления взаимной корреляции двух сигналов
# x - первый сигнал
# y - второй сигнал
# max_lag - максимальный лаг для корреляции
# Возвращает массив значений корреляции

def cross_correlation_numpy(x, y, max_lag):
    return np.correlate(x, y, mode='full')[len(x)-max_lag-1:len(x)+max_lag]

# Создаем массив значений x от -5 до 5
x_values = np.linspace(-5, 5, 1000)

# Список функций
functions = [g1, g2, g3, g4, g5]

# Вычисляем и отображаем взаимную корреляцию для всех пар функций
for i in range(len(functions)):
    for j in range(i + 1, len(functions)):
        y1 = functions[i](x_values)
        y2 = functions[j](x_values)

        # Вычисляем взаимную корреляцию
        cross_corr_result = cross_correlation_numpy(y1, y2, 50)
        lags = np.arange(-50, 51)

        # Создаем графики
        plt.figure(figsize=(10, 6))

        # График функций
        plt.subplot(2, 1, 1)
        plt.plot(x_values, y1, label=f'Function {i + 1}')
        plt.plot(x_values, y2, label=f'Function {j + 1}')
        plt.legend()
        plt.title(f'Функции {i + 1} и {j + 1}')

        # График взаимной корреляции
        plt.subplot(2, 1, 2)
        plt.plot(lags, cross_corr_result, label='Cross-correlation')
        plt.xlabel('Lag')
        plt.ylabel('Correlation')
        plt.legend()
        plt.title('Взаимная корреляция')

        plt.tight_layout()
        plt.show()