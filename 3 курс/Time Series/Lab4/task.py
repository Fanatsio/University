import math
import matplotlib.pyplot as plt
import numpy as np

def taylor_coeff_sin(n):
    return (-1)**(n // 2) / math.factorial(n) if n % 2 == 1 else 0

def taylor_series_sin(x, num_terms):
    return sum(taylor_coeff_sin(n) * x**n for n in range(num_terms))

x_values = np.linspace(-4, 4, 100)
plt.figure(figsize=(8, 6))

plt.subplot(2, 1, 1)
plt.plot(x_values, np.sin(x_values), label="sin(x)", color='b')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Оригинальная функция sin(x)')
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
for num_terms in [3, 5, 10, 25, 50]:
    y_values = [taylor_series_sin(x, num_terms) for x in x_values]
    plt.plot(x_values, y_values, label=f'Ряд Тейлора ({num_terms} членов)')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Аппроксимация sin(x) рядом Тейлора')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
