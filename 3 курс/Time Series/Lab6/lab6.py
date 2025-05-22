import numpy as np
import matplotlib.pyplot as plt

filename = 'lab5_data4.txt'
time = []
channel0 = []
channel1 = []

with open(filename, 'r') as file:
    for line in file:
        parts = line.strip().split(';')
        time.append(int(parts[0]))
        channel0.append(float(parts[1]))
        channel1.append(float(parts[2]))

# Определяем частоты отсечки
t1 = 50  # Нижняя частота отсечки
t2 = 150  # Верхняя частота отсечки

# Создаем режекторный фильтр
def reject_filter(signal, t1, t2, fs):
  """
  Режекторный фильтр, который задерживает полосу частот от t1 до t2.

  Args:
    signal: Входной сигнал.
    t1: Нижняя частота отсечки.
    t2: Верхняя частота отсечки.
    fs: Частота дискретизации.

  Returns:
    Отфильтрованный сигнал.
  """
  n = len(signal)
  freq = np.fft.fftfreq(n, d=1/fs)
  
  # Создаем маску для фильтрации
  mask = (freq >= t1/fs) & (freq <= t2/fs)
  
  # Преобразуем сигнал в частотную область
  fft_signal = np.fft.fft(signal)
  
  # Применяем маску к спектру сигнала
  fft_signal[mask] = 0
  
  # Обратное преобразование Фурье
  filtered_signal = np.fft.ifft(fft_signal)
  
  return filtered_signal

# Частота дискретизации (предполагается, что она известна)
fs = 1000

# Применяем фильтр к каналам
filtered_channel0 = reject_filter(channel0, t1, t2, fs)
filtered_channel1 = reject_filter(channel1, t1, t2, fs)

# Построим графики
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(channel0, label="Канал 0 (исходный)")
plt.plot(filtered_channel0.real, label="Канал 0 (отфильтрованный)")
plt.title("Канал 0")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(channel1, label="Канал 1 (исходный)")
plt.plot(filtered_channel1.real, label="Канал 1 (отфильтрованный)")
plt.title("Канал 1")
plt.legend()

plt.tight_layout()
plt.show()