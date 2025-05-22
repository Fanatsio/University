import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt

def butter_bandstop(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandstop')
    return b, a

def bandstop_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandstop(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Пример использования фильтра:
if __name__ == "__main__":
    # Параметры сигнала
    fs = 5000.0       # Частота дискретизации, Гц
    T = 1.0           # Продолжительность сигнала, секунды
    t = np.linspace(0, T, int(T * fs), endpoint=False)
    
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

    # Создание сигнала с частотами 50 Гц и 1000 Гц
    sig = channel0

    # Применение полосно-заграждающего фильтра
    lowcut = 50.0
    highcut = 55.0
    filtered_sig = bandstop_filter(sig, lowcut, highcut, fs, order=6)

    # Отображение исходного и фильтрованного сигнала
    plt.figure(1)
    plt.subplot(2, 1, 1)
    plt.plot(t, sig)
    plt.title('Исходный сигнал')
    plt.subplot(2, 1, 2)
    plt.plot(t, filtered_sig)
    plt.title('Фильтрованный сигнал')
    plt.xlabel('Время [сек]')
    plt.tight_layout()
    plt.show()

    # Отображение частотного отклика фильтра
    w, h = freqz(*butter_bandstop(lowcut, highcut, fs, order=6), worN=2000)
    plt.figure(2)
    plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
    plt.plot([0, 0.5*fs], [np.sqrt(0.5), np.sqrt(0.5)], '--', color='gray')
    plt.xlabel('Частота [Гц]')
    plt.ylabel('Амплитуда')
    plt.title('Частотный отклик полосно-заграждающего фильтра')
    plt.grid()
    plt.show()
