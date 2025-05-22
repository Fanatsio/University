import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import minimize

data_path = './lab1/AirQualityUCI.csv'
data = pd.read_csv(data_path, sep=';', decimal=",")
data_clean = data.dropna(subset=['RH'])
time_series = data_clean['RH'][2500:3250].copy()

ts_values = time_series.values.astype(float)

# Настройки модели
p = 20  # Порядок авторегрессии
n_forecast = 25  # Количество шагов для прогноза

phi = np.random.rand(p)

def calculate_error(ts, phi, p):
    preds = np.zeros(len(ts))
    for t in range(p, len(ts)):
        preds[t] = sum(phi[i] * ts[t - i - 1] for i in range(p))  # Авторегрессия
    errors = ts[p:] - preds[p:]
    return np.sum(errors**2) / len(errors)

def optimize_params(params):
    global phi
    phi = params[:p]
    return calculate_error(ts_values, phi, p)

initial_params = np.copy(phi)
result = minimize(optimize_params, initial_params, method='L-BFGS-B')

phi = result.x[:p]

predictions = []
ts_extended = np.copy(ts_values)
for _ in range(n_forecast):
    next_value = sum(phi[i] * ts_extended[-(i + 1)] for i in range(p))
    predictions.append(next_value)
    ts_extended = np.append(ts_extended, next_value)

plt.figure(figsize=(14, 7))
plt.plot(time_series.index, time_series.values, label="Фактические данные", color="blue")
plt.plot(range(time_series.index[-1] + 1, time_series.index[-1] + 1 + n_forecast), predictions, label=f"Прогноз AR({p})", color="red", linestyle="--")
plt.xlabel("Индекс")
plt.ylabel("Концентрация RH")
plt.title(f"Прогноз временного ряда с использованием AR({p})")
plt.legend()
plt.show()
