import numpy as np
import matplotlib.pyplot as plt

def sinusoid(x):
    return np.sin(x)

def cosinusoid(x):
    return np.cos(x)

def exponential(x):
    return np.exp(-x)

def parabola(x):
    return x ** 2

def straight_line(x):
    return x

def plot_functions(x, y1, y2, label1, label2, title):
    """
    Построение графиков двух функций.

    Parameters:
    x (ndarray): Массив значений x.
    y1 (ndarray): Значения функции 1.
    y2 (ndarray): Значения функции 2.
    label1 (str): Подпись для функции 1.
    label2 (str): Подпись для функции 2.
    title (str): Заголовок графика.

    Returns:
    None
    """
    plt.plot(x, y1, label=label1)
    plt.plot(x, y2, label=label2)
    plt.legend()
    plt.title(title)

def plot_cross_correlation(x, y1, y2, label, title):
    """
    Построение графика кросс-корреляции двух функций.

    Parameters:
    x (ndarray): Массив значений x.
    y1 (ndarray): Значения функции 1.
    y2 (ndarray): Значения функции 2.
    label (str): Подпись для графика.
    title (str): Заголовок графика.

    Returns:
    None
    """
    plt.plot(x, np.correlate(y1, y2, mode='same'), label=label)
    plt.legend()
    plt.title(title)

if __name__ == "__main__":
    x = np.linspace(-5, 5, 100)

    plt.figure(figsize=(12, 8))

    plt.subplot(3, 2, 1)
    plot_functions(x, sinusoid(x), cosinusoid(x), 'sin(x)', 'cos(x)', 'Sinusoid vs Cosinusoid')

    plt.subplot(3, 2, 2)
    plot_cross_correlation(x, sinusoid(x), cosinusoid(x), 'Cross-Correlation', 'Cross-Correlation: sin(x) and cos(x)')

    plt.subplot(3, 2, 3)
    plot_functions(x, exponential(x), parabola(x), 'e^(-x)', 'x^2', 'Exponential vs Parabola')

    plt.subplot(3, 2, 4)
    plot_cross_correlation(x, exponential(x), parabola(x), 'Cross-Correlation', 'Cross-Correlation: e^(-x) and x^2')

    plt.subplot(3, 2, 5)
    plot_functions(x, straight_line(x), parabola(x), 'x', 'x^2', 'Straight Line vs Parabola')

    plt.subplot(3, 2, 6)
    plot_cross_correlation(x, straight_line(x), parabola(x), 'Cross-Correlation', 'Cross-Correlation: x and x^2')

    plt.tight_layout()
    plt.show()
