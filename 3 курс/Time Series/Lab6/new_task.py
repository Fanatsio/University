import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import iirnotch, lfilter, freqz

def load_data(file_path, delimiter=';', skip_header=1):
    return np.genfromtxt(file_path, delimiter=delimiter, skip_header=skip_header, encoding='cp1251')

def scale_signal(signal):
    signal_mean = np.mean(signal)
    return signal - signal_mean

def calculate_filter_coeffs(f0, Q, fs):
    return iirnotch(f0 / (fs / 2), Q)

def filter_signal(signal):
    b, a = calculate_filter_coeffs(f0, Q, fs)
    print(a,b)
    return lfilter(b, a, signal)

def plot_signals(signal1, filtered_signal1, signal2, filtered_signal2):
    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.plot(signal1, label='Original Signal', color='blue')
    plt.plot(filtered_signal1[:len(signal1)], '--', label='Filtered Signal', color='red')
    plt.xlabel('Samples')
    plt.ylabel('Amplitude')
    plt.title('Signal 1 before and after filtering')
    plt.legend()
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(signal2, label='Original Signal', color='blue')
    plt.plot(filtered_signal2[:len(signal2)], '--', label='Filtered Signal', color='red')
    plt.xlabel('Samples')
    plt.ylabel('Amplitude')
    plt.title('Signal 2 before and after filtering')
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()

def plot_filter_response(b, a, fs, title="Frequency Response"):
    w, h = freqz(b, a, worN=8000)
    plt.figure()
    plt.plot((fs * 0.5 / np.pi) * w, abs(h), 'b')
    plt.title(title)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid()
    plt.show()

if __name__ == "__main__":
    f0 = 0.2  # Частота для подавления (в Гц)
    Q = 10  # Добротность фильтра
    # Q = 0.1  # Добротность фильтра
    fs = 1.0  # Частота дискретизации

    data = load_data('lab5_data4.txt')
    signal1 = data[:, 1]
    signal2 = data[:, 2]

    signal1 = scale_signal(signal1)
    signal2 = scale_signal(signal2)

    filtered_signal1 = filter_signal(signal1)
    filtered_signal2 = filter_signal(signal2)

    plot_signals(signal1, filtered_signal1, signal2, filtered_signal2)
