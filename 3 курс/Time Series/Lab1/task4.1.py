import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Шаг 1: Загрузка и подготовка данных
data_path = './lab1/AirQualityUCI.csv'
data = pd.read_csv(data_path, sep=';', decimal=",")
data_clean = data.dropna(subset=['RH'])
time_series = data_clean['RH'][2500:3250].astype(float).copy()

# Шаг 2: Построение модели ARMA(p, q) и предсказания
p, q = 2, 2  # Указываем порядок модели ARMA(p, q)
model_arma = ARIMA(time_series, order=(p, 0, q))  # ARMA — это ARIMA без интеграции (d=0)
model_arma_fitted = model_arma.fit()

# Прогноз на 10 шагов вперед
forecast_arma = model_arma_fitted.forecast(steps=10)

# Построение графика
plt.figure(figsize=(14, 7))
plt.plot(time_series.index, time_series, label='Фактический временной ряд', color='blue')
forecast_idx = range(time_series.index[-1] + 1, time_series.index[-1] + 11)
plt.plot(forecast_idx, forecast_arma.values, label=f'Прогноз ARMA({p},{q})', color='red', linestyle='--')
plt.xlabel('Индекс')
plt.ylabel('Концентрация RH')
plt.title(f'Прогноз временного ряда с использованием модели ARMA({p},{q})')
plt.legend()
plt.show()
