import numpy as np
import matplotlib.pyplot as plt

def g1(x):
    return np.cos(3 * x) + np.sin(x)

def g2(x):
    return np.exp(-0.5 * x**2)

def g3(x):
    return np.tan(x) * np.heaviside(x, 0.5)

def g4(x):
    return np.abs(np.cos(x)) + np.log1p(np.abs(x))

def g5(x):
    return np.sinh(x) / (1 + np.cosh(x))

def cross_correlation(x, y, max_lag):
    result = np.zeros(2 * max_lag + 1, dtype=float)

    for lag in range(-max_lag, max_lag + 1):
        sum_val = 0
        for i in range(len(x)):
            j = i - lag
            if 0 <= j < len(y):
                sum_val += x[i] * y[j]
        result[lag + max_lag] = sum_val

    return result

x_values = np.linspace(-5, 5, 1000)

functions = [g1, g2, g3, g4, g5]

for i in range(len(functions)):
    for j in range(i + 1, len(functions)):
        y1 = functions[i](x_values)
        y2 = functions[j](x_values)

        cross_corr_result = cross_correlation(y1, y2, 50)
        lags = np.arange(-50, 51)

        plt.figure(figsize=(10, 6))

        plt.subplot(2, 1, 1)
        plt.plot(x_values, y1, label=f'Function {i + 1}')
        plt.plot(x_values, y2, label=f'Function {j + 1}')
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(lags, cross_corr_result, label='Cross-correlation')
        plt.xlabel('Lag')
        plt.ylabel('Correlation')
        plt.legend()

        plt.tight_layout()
        plt.show()
