import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.ar_model import AutoReg

# Шаг 1: Загрузка данных
data_path = './lab1/AirQualityUCI.csv'
data = pd.read_csv(data_path, sep=';', decimal=",")

# Шаг 2: Проверка на стационарность
# Удаление строк с отсутствующими значениями для выбранного ряда
data_clean = data.dropna(subset=['RH'])

# Преобразование во временной ряд
time_series = data_clean['RH'][2500:3250].copy()
plt.plot(time_series)
plt.show()

# Тест Дики-Фуллера на стационарность ряда
def Augmented_Dickey_Fuller_test(time_series):
    result = adfuller(time_series, autolag='AIC')
    test_statistic, p_value, used_lag, nobs, critical_values, aic = result

    print("\nРезультаты теста Дики-Фуллера")
    print(f"Статистика теста (ADF): {test_statistic:.4f}, p-значение: {p_value:.2e}, Использовано лагов: {used_lag}, Число наблюдений после лагов: {nobs}")
    print("Критические значения:")
    for key, value in critical_values.items():
        print(f"{key}: {value:.4f}")
    print(f"AIC: {aic:.2f}")

    if p_value < 0.05:
        print("\n✅ Временной ряд стационарный (нулевая гипотеза отвергнута)")
    else:
        print("\n❌ Временной ряд нестационарный (нулевая гипотеза не отвергнута, возможен тренд)")

Augmented_Dickey_Fuller_test(time_series)

# Приведение ряда к стационарному методом дифференциирования (вычислением разностей)
time_series_diff = time_series.diff().dropna()

Augmented_Dickey_Fuller_test(time_series_diff)

# Шаг 3: Определение лага авторегрессии
# Построение графика PACF
'''
PACF — это инструмент, используемый для анализа временных рядов, который показывает, как значения ряда коррелируют с его собственными лагами,
при этом учитывая влияние всех предыдущих лагов.
'''

# Создание временного индекса (например, ежедневные данные)
time_series.index = pd.date_range(start='2023-01-01', periods=len(time_series), freq='D') # Не является обязательным, но библиотека statsmodels выкидывает Warning из-за отсутствия временного индекса.

fig, ax = plt.subplots(figsize=(10, 6))
plot_pacf(time_series, ax=ax, lags=30, method='ywm')
plt.show()

# Шаг 4: Построение модели AR
# Определение количества лагов на основе графика PACF
lags = 2 # Примерное количество значимых лагов, видимых на графике

# Создание и обучение модели AR
model = AutoReg(time_series, lags=lags)
model_fitted = model.fit()
print(model_fitted.summary())

# Шаг 5: Прогнозирование
# Создание прогноза на 10 шагов вперед
forecast_steps = 10
forecast_end_idx = len(time_series) + forecast_steps - 1  # Индекс последнего прогнозируемого значения
forecast_index = range(len(time_series), len(time_series) + forecast_steps)  # Генерация новых индексов для прогноза

forecast = model_fitted.predict(start=len(time_series), end=forecast_end_idx, dynamic=True)
forecast.index = forecast_index  # Присвоение новых индексов прогнозу

# Визуализация фактических данных и прогноза
plt.figure(figsize=(14, 7))
plt.plot(range(len(time_series)), time_series.values, label='Фактические данные', color='blue')
plt.plot(forecast.index, forecast.values, label='Прогноз', color='red', linestyle='--')
plt.xlabel('Индекс времени')
plt.ylabel('Концентрация RH')
plt.title('Прогноз концентрации RH с использованием модели авторегрессии')
plt.legend()
plt.show()
