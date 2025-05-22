import numpy as np
import matplotlib.pyplot as plt

# Параметры сигнала
A0 = 1  # Амплитуда
w0 = 6# Угловая частота
phi0 = 2  # Фаза

# Временной диапазон
x_min = 0
x_max = 6
N = 512 # Количество точек

# Генерация данных
x = np.linspace(x_min, x_max, N)
f = A0 * np.sin(w0 * x + phi0)

#2

def DFT(f):
    N = len(f)
    F = np.zeros(N, dtype=complex)
    for k in range(N):
        for n in range(N):
            F[k] += f[n] * np.exp(-2j * np.pi * k * n / N)
    return F

F = DFT(f)[:N//2]

#3
def IDFT(F):
    N = len(F)
    f = np.zeros(N, dtype=complex)
    for n in range(N):
        for k in range(N):
            f[n] += F[k] * np.exp(2j * np.pi * k * n / N) / N
    return f.real

f_restored = IDFT(F)

#4
from scipy.fft import fft, ifft

F_fft = fft(f)[:N//2]
f_ifft = ifft(F_fft)


plt.figure(figsize=(12, 8))

# Исходный сигнал
plt.subplot(3, 2, 1)
plt.plot(x, f)
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Исходный сигнал")
plt.grid(True)

# Амплитудный спектр (ДПФ)
plt.subplot(3, 2, 2)
plt.plot(np.abs(F))
plt.xlabel("Частота")
plt.ylabel("Амплитуда")
plt.title("Амплитудный спектр (ДПФ)")
plt.grid(True)

# Восстановленный сигнал (ОДПФ)
plt.subplot(3, 2, 3)
plt.plot(x[:N//2], f_restored)
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Восстановленный сигнал (ОДПФ)")
plt.grid(True)

# Амплитудный спектр (scipy.fft)
plt.subplot(3, 2, 4)
plt.plot(np.abs(F_fft))
plt.xlabel("Частота")
plt.ylabel("Амплитуда")
plt.title("Амплитудный спектр (scipy.fft)")
plt.grid(True)

# Восстановленный сигнал (scipy.fft)
plt.subplot(3, 2, 5)
plt.plot(x[:N//2], f_ifft.real)
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Восстановленный сигнал (scipy.fft)")
plt.grid(True)

plt.tight_layout()

plt.show()
