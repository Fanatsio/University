import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.linalg import hankel

# Загружаем данные из файла
file_path = "./lab8/lab5_data4.txt"  # Укажи путь к файлу, если он в другом месте
df = pd.read_csv(file_path, delimiter=";", decimal=",", encoding="cp1251")

# Удаляем лишний столбец, если есть
df = df.drop(columns=["Unnamed: 3"], errors="ignore")

# Преобразуем данные (используем только "Канал0")
time_series = df["Канал0"].astype(float).values

# Визуализируем исходный временной ряд
plt.figure(figsize=(12, 5))
plt.plot(time_series, label="Исходный временной ряд", color="b")
plt.xlabel("Отсчеты")
plt.ylabel("Значение")
plt.legend()
plt.title("Временной ряд Канал0")
plt.grid()
plt.show()

# Функция для формирования траекторной матрицы
def embed_series(series, window):
    """Формирует траекторную матрицу с оконным размером window."""
    N = len(series)
    return hankel(series[:window], series[window - 1:])

# Выбираем размер окна (обычно 30% от длины ряда)
window_size = int(len(time_series) * 0.3)
X = embed_series(time_series, window_size)

# Выполняем SVD разложение
U, s, Vt = np.linalg.svd(X, full_matrices=False)

# Визуализируем спектр сингулярных значений
plt.figure(figsize=(10, 5))
plt.plot(s, "o-", label="Сингулярные значения", color="r")
plt.yscale("log")
plt.xlabel("Компонента")
plt.ylabel("Сингулярное значение")
plt.legend()
plt.title("Спектр сингулярных значений (SSA)")
plt.grid()
plt.show()

# Выбираем первые 2 главные компоненты
k = 2
X_reconstructed = np.dot(U[:, :k], np.dot(np.diag(s[:k]), Vt[:k, :]))

# Восстановленный ряд
reconstructed_series = np.mean(X_reconstructed, axis=1)

# Визуализируем восстановленный ряд
plt.figure(figsize=(12, 5))
plt.plot(time_series, label="Исходный ряд", color="b", alpha=0.5)
plt.plot(reconstructed_series, label="Восстановленный ряд (SSA)", color="r")
plt.xlabel("Отсчеты")
plt.ylabel("Значение")
plt.legend()
plt.title("Восстановленный временной ряд (SSA)")
plt.grid()
plt.show()

# Прогнозирование (экстраполяция на 20 шагов вперед)
future_steps = 20
forecast = reconstructed_series[-window_size:]  # Берем последнее окно и усредняем

# Усредняем значения для прогнозирования
predicted_values = np.mean(forecast, axis=0)

# Генерируем временную шкалу для прогноза
time_extended = np.arange(len(time_series) + future_steps)
forecast_series = np.concatenate([reconstructed_series, predicted_values[:future_steps]])

# Визуализируем прогноз
plt.figure(figsize=(12, 5))
plt.plot(time_series, label="Исходный ряд", color="b", alpha=0.5)
plt.plot(time_extended, forecast_series, label="Прогноз SSA", color="g", linestyle="dashed")
plt.axvline(len(time_series), color="black", linestyle="--", label="Начало прогноза")
plt.xlabel("Отсчеты")
plt.ylabel("Значение")
plt.legend()
plt.title("Прогнозирование временного ряда методом SSA")
plt.grid()
plt.show()
