import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Загрузка данных
data_path = './lab1/AirQualityUCI.csv'
data = pd.read_csv(data_path, sep=';', decimal=",")
data_clean = data.dropna(subset=['RH'])
time_series = data_clean['RH'][2500:3250].copy()

# Приведение данных к numpy
ts_values = time_series.values.astype(float)

# Настройки модели
p = 20  # Порядок авторегрессии
q = 2  # Порядок скользящего среднего
n_forecast = 25  # Количество шагов для прогноза

# Инициализация коэффициентов (начальные значения)
phi = np.random.rand(p)
theta = np.random.rand(q)

# Вспомогательные переменные
errors = np.zeros(len(ts_values) + n_forecast)

# Функция для расчета ошибки
def calculate_error(ts, phi, theta, p, q):
    global errors
    preds = np.zeros(len(ts))
    for t in range(max(p, q), len(ts)):
        ar_part = sum(phi[i] * ts[t - i - 1] for i in range(p))  # Авторегрессия
        ma_part = sum(theta[i] * errors[t - i - 1] for i in range(q))  # MA
        preds[t] = ar_part + ma_part
        errors[t] = ts[t] - preds[t]  # Ошибка
    return np.sum(errors**2) / len(ts)

# Оптимизация параметров (глобально для примера)
from scipy.optimize import minimize

def optimize_params(params):
    global phi, theta
    phi = params[:p]
    theta = params[p:]
    return calculate_error(ts_values, phi, theta, p, q)

# Начальное приближение
initial_params = np.concatenate([phi, theta])
result = minimize(optimize_params, initial_params, method='L-BFGS-B')

# Итоговые параметры
phi = result.x[:p]
theta = result.x[p:]

# Прогнозирование
predictions = []
for t in range(len(ts_values), len(ts_values) + n_forecast):
    ar_part = sum(phi[i] * ts_values[t - i - 1] for i in range(p))
    ma_part = sum(theta[i] * errors[t - i - 1] for i in range(q))
    next_value = ar_part + ma_part
    predictions.append(next_value)
    ts_values = np.append(ts_values, next_value)  # Обновление ряда

# График
plt.figure(figsize=(14, 7))
plt.plot(time_series.index, time_series.values, label="Фактические данные", color="blue")
plt.plot(range(time_series.index[-1] + 1, time_series.index[-1] + 1 + n_forecast), predictions, label="Прогноз ARMA(2,2)", color="red", linestyle="--")
plt.xlabel("Индекс")
plt.ylabel("Концентрация RH")
plt.title("Прогноз временного ряда с использованием ARMA(2,2)")
plt.legend()
plt.show()