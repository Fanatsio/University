import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt('./lab5/lab5_data4.txt', delimiter=';', skip_header=1, encoding='latin1')
samples = data[:, 0]
channel_0 = data[:, 1]
channel_1 = data[:, 2]

fft_channel_0 = np.fft.fft(channel_0)
fft_channel_1 = np.fft.fft(channel_1)

# Расчет частотных осей
N = len(samples)
freqs = np.fft.fftfreq(N)

# Расчет АЧХ и ФЧХ
achx_channel_0 = np.abs(fft_channel_0)
achx_channel_1 = np.abs(fft_channel_1)

fchx_channel_0 = np.angle(fft_channel_0)
fchx_channel_1 = np.angle(fft_channel_1)

# Построение графиков
plt.figure(figsize=(12, 6))

plt.subplot(3, 1, 1)
plt.plot(samples, channel_0, label='Канал 0')
plt.plot(samples, channel_1, label='Канал 1')
plt.title('Сигналы')
plt.legend()
plt.grid(True)

# График АЧХ
plt.subplot(3, 1, 2)
plt.plot(freqs[:N//2], achx_channel_0[:N//2], label='Канал 0')
plt.plot(freqs[:N//2], achx_channel_1[:N//2], label='Канал 1')
plt.title('Амплитудно-частотная характеристика (АЧХ)')
plt.xlabel('Частота, Гц')
plt.ylabel('Амплитуда')
plt.legend()
plt.grid(True)

# График ФЧХ
plt.subplot(3, 1, 3)
plt.plot(freqs[:N//2], fchx_channel_0[:N//2], label='Канал 0')
plt.plot(freqs[:N//2], fchx_channel_1[:N//2], label='Канал 1')
plt.title('Фазо-частотная характеристика (ФЧХ)')
plt.xlabel('Частота, Гц')
plt.ylabel('Фаза, рад')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
