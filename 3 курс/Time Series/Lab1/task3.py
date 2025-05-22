import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Шаг 1: Загрузка и подготовка данных
data_path = './lab1/AirQualityUCI.csv'
data = pd.read_csv(data_path, sep=';', decimal=",")
data_clean = data.dropna(subset=['RH'])
time_series = data_clean['RH'][2500:3250].copy()

# Шаг 2: Расчет скользящих средних
ma_3 = time_series.rolling(window=3).mean()
ma_5 = time_series.rolling(window=5).mean()
ma_10 = time_series.rolling(window=10).mean()
ma_50 = time_series.rolling(window=50).mean()

# Шаг 3: Визуализация скользящих средних
plt.figure(figsize=(14, 7))
plt.plot(time_series.index, time_series, label='Исходный ряд', color='black')
plt.plot(time_series.index, ma_3, label='Скользящее среднее (окно 3)', color='red')
plt.plot(time_series.index, ma_5, label='Скользящее среднее (окно 5)', color='blue')
plt.plot(time_series.index, ma_10, label='Скользящее среднее (окно 10)', color='green')
plt.plot(time_series.index, ma_50, label='Скользящее среднее (окно 50)', color='orange')
plt.xlabel('Время')
plt.ylabel('Концентрация CO(GT)')
plt.title('Скользящие средние для временного ряда CO(GT)')
plt.legend()
plt.show()

# Шаг 4: Построение и визуализация прогноза с использованием модели скользящего среднего (MA)
# Подготовка данных (оставляем без изменений)

# Построение и визуализация прогноза с использованием модели скользящего среднего (MA)
model_ma = ARIMA(time_series.astype(float), order=(0, 0, 5))  # Приведение к float для избежания ошибок
model_ma_fitted = model_ma.fit()

# Создание прогноза на 10 шагов вперед
forecast_ma = model_ma_fitted.forecast(steps=10)

# Подготовка индексов для прогноза
last_idx = time_series.index[-1]  # Последний индекс исходного временного ряда
forecast_idx = range(last_idx + 1, last_idx + 11)  # Создание новых индексов для прогноза

plt.figure(figsize=(14, 7))
plt.plot(time_series.index[0:], time_series.values[0:], label='Фактические данные', color='blue')
plt.plot(forecast_idx, forecast_ma.values, label='Прогноз MA(5)', color='red', linestyle='--')
plt.xlabel('Индекс')
plt.ylabel('Концентрация RH')
plt.title('Прогноз концентрации RH с использованием модели скользящего среднего MA(5)')
plt.legend()
plt.show()

#Скользящее среднее используется для сглаживания временного ряда, чтобы выделить долгосрочные тренды или циклы. Оно вычисляется как среднее значение для каждого подмножества данных, состоящего из N последовательных измерений (окно N).
#В вашем коде рассчитываются скользящие средние с окнами размером в 3, 5, 10, и 50 точек. Большие окна сильнее сглаживают ряд, но делают его менее чувствительным к короткосрочным изменениям.
# На графике изображен исходный временной ряд и скользящие средние с разными окнами. Это позволяет визуально сравнить исходные данные с их сглаженными версиями и оценить тенденции.
#Используется модель ARIMA с параметрами (0, 0, 5), что означает, что модель является чисто моделью скользящего среднего (MA) пятого порядка без авторегрессии (AR) и без дифференциации (I).
#Модель MA используется для прогнозирования будущих значений на основе шума (ошибок) предыдущих прогнозов.
