import pywt
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 1. Выбираем произвольную функцию из pywt.data
data = pywt.data.ecg()

# 2. Выбираем вейвлет (real)
wavelet = 'morl'

# 3. Вычисляем CWT
coeffs, freqs = pywt.cwt(data, scales=range(1, 31), wavelet=wavelet)
time = np.arange(len(data))

# 4. Построение скейлограммы
plt.figure(figsize=(10, 4))
plt.title("Скейлограмма")
plt.contourf(time, freqs, np.abs(coeffs), cmap='viridis')
plt.xlabel('Время')
plt.ylabel('Частота')
plt.colorbar()
plt.show()

# 5. Построение 3D-поверхности двухпараметрического спектра
frequencies = []
for scale in range(1, 31):
    frequency = pywt.central_frequency(wavelet) / scale  # Calculate frequency for the current scale
    frequencies.append(frequency)
frequencies = np.array(frequencies)  # Convert to NumPy array

time = np.arange(len(data))
time, frequencies = np.meshgrid(time, frequencies)
power = np.abs(coeffs)  # Делаем power двумерным

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')  # Исправленный вызов
surf = ax.plot_surface(time, frequencies, power, cmap='viridis', linewidth=0, antialiased=False)
ax.set_xlabel('Время')
ax.set_ylabel('Частота')
ax.set_zlabel('Мощность')
plt.title("3D-поверхность двухпараметрического спектра")
plt.show()

# 6. Построение плоскости с цветовыми областями вейвлет-преобразования
plt.figure(figsize=(10, 4))
plt.title("Плоскость с цветовыми областями вейвлет-преобразования")
plt.contourf(time, frequencies, power, cmap='viridis')
plt.xlabel('Время')
plt.ylabel('Частота')
plt.colorbar()
plt.show()

# 7. Построение сечений вейвлет-спектра
slice_times = [100, 500, 900]
for slice_time in slice_times:
    plt.figure()
    plt.plot(frequencies[:, slice_time], power[:, slice_time])
    plt.xlabel('Частота')
    plt.ylabel('Мощность')
    plt.title(f"Сечение вейвлет-спектра при t={slice_time}")
    plt.show()

# 8. Построение скелетона - линии локальных экстремумов
plt.figure(figsize=(10, 4))
plt.title("Скелетон - линии локальных экстремумов")
plt.contour(time, frequencies, power, colors='k', levels=[0.05, 0.1, 0.2, 0.5])
plt.xlabel('Время')
plt.ylabel('Частота')
plt.show()
