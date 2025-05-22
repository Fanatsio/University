import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve

def step_signal(x):
    """
    Генерация ступенчатого сигнала.

    Parameters:
    x (ndarray): Массив значений x.

    Returns:
    ndarray: Ступенчатый сигнал.
    """
    return np.where((0 <= x) & (x < 1), 1, 0)

def convolution(f, g):
    """
    Реализация свёртки двух функций.

    Parameters:
    f (ndarray): Первый сигнал.
    g (ndarray): Второй сигнал.

    Returns:
    ndarray: Результат свёртки f и g.
    """
    conv_result = convolve(f, g, mode='full')
    return conv_result

if __name__ == "__main__":
    x = np.arange(-2, 5, 0.01)

    f_signal = step_signal(x)
    g_signal = step_signal(x)

    conv_result = convolution(f_signal, g_signal)
    
    plt.figure(figsize=(10, 5))

    plt.subplot(3, 1, 1)
    plt.plot(x, f_signal, 'b', label='f(x)')
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(x, g_signal, 'g', label='g(x)')
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(conv_result, 'r', label='f(x) * g(x)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
