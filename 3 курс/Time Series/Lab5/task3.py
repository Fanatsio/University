import numpy as np
import time

#task1
def DFT(f):
    N = len(f)
    F = np.zeros(N, dtype=complex)
    for k in range(N):
        for n in range(N):
            F[k] += f[n] * np.exp(-2j * np.pi * k * n / N)
    return F

def FFT(x):
    N = len(x)
    if N <= 1:
        return x
    even = FFT(x[::2])
    odd = FFT(x[1::2])
    factor = np.exp(-2j * np.pi * np.arange(N) / N)
    # Объединение результатов
    return np.concatenate([even + factor[:N // 2] * odd, even - factor[:N // 2] * odd])

def IDFT(F):
    N = len(F)
    f_reconstructed = np.zeros(N, dtype=complex)
    for n in range(N):
        for k in range(N):
            f_reconstructed[n] += F[k] * np.exp(2j * np.pi * k * n / N) / N
    return f_reconstructed.real

# Исходный сигнал
A0 = 1
w0 = 2 * np.pi
phi0 = np.pi / 4
N = 512
x = np.linspace(0, 2 * np.pi, N)
f = A0 * np.sin(w0 * x + phi0)

# Измерение времени выполнения ДПФ
start_time = time.time()
F_dft = DFT(f)[:N//2]
dft_times = time.time() - start_time

# Измерение времени выполнения БПФ
start_time = time.time()
F_fft = FFT(f)[:N//2]
fft_times = time.time() - start_time

from scipy.fftpack import fft, ifft
import matplotlib.pyplot as plt

f_reconstructed_dft = IDFT(F_dft)
f_reconstructed_scipy_fft = np.real(ifft(F_fft))

plt.figure(figsize=(12, 8))

# Исходный сигнал
plt.subplot(3, 1, 1)
plt.plot(x, f, label='Исходный сигнал')
plt.title('Исходный сигнал')
plt.grid(True)

# Спектр сигнала (Амплитудный спектр)
plt.subplot(3, 1, 2)
plt.plot(np.abs(F_fft), label='Амплитудный спектр (F_fft)', color='g', linestyle='--' )
plt.plot(np.abs(F_dft), label='Амплитудный спектр (F_dft)', color='r', linestyle=':')
plt.title('Амплитудный спектр')
plt.legend()
plt.grid(True)

# Восстановленный сигнал из ДПФ и БПФ
plt.subplot(3, 1, 3)
plt.plot(x[:N//2], f_reconstructed_dft, label='Восстановленный сигнал (ДПФ)', linestyle='--')
plt.plot(x[:N//2], f_reconstructed_scipy_fft, label='Восстановленный сигнал (БПФ)', linestyle=':')
plt.title('Восстановление сигнала')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

print("Среднее время выполнения ДПФ:", np.mean(dft_times))
print("Среднее время выполнения БПФ:", np.mean(fft_times))

import re

test_list = [1e-16, 1e-10, 1e-6]
for i in test_list:
    print(f"Тест с {i}:")
    try:
        np.testing.assert_allclose(F_dft, F_fft, rtol=i, atol=i)
        print("Результаты совпадают.")  # Вывод при успешном сравнении
    except AssertionError as e:
        # Извлечение информации из сообщения об ошибке
        match = re.search(r"Mismatched elements: (\d+) / (\d+) \(.+\)\nMax absolute difference: (.+)\nMax relative difference: (.+)", str(e))
        if match:
            mismatched, total, abs_diff, rel_diff = match.groups()
            print(f"Mismatched elements: {mismatched} / {total}")
            print(f"Max absolute difference: {abs_diff}")
            print(f"Max relative difference: {rel_diff}")
        else:
            print(e)