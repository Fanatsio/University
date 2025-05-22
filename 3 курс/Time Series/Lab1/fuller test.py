import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller



# Загрузка данных из CSV файла с использованием правильного разделителя
df = pd.read_csv('AirQualityUCI.csv', sep=';', dtype={'Date': str, 'Time': str}, na_values=['NA', 'NaN'])
df['Date'] = df['Date'].astype(str)
df['Time'] = df['Time'].astype(str)

df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format = '%d/%m/%Y %H.%M.%S')


# Преобразование данных в числовой формат, начиная со столбца 'CO(GT)'
for column in df.columns[2:]:
    df[column] = pd.to_numeric(df[column], errors='coerce')

for column in df.columns[2:]:  # 10 - следующий после последнего столбца, который нужно проверить
    # Проверка наличия данных в столбце
    if df[column].notnull().any():
        # Проверка, содержит ли столбец хотя бы два уникальных значения
        if df[column].nunique() > 1:
            # Проведение теста Дики-Фуллера для выбранного столбца
            result = adfuller(df[column].dropna())  # Удаляем NaN значения перед тестом
            # Вывод результатов теста
            print(f'Столбец {column}:')
            print('ADF статистика:', result[0])
            print('p-value:', result[1])
            print('Критические значения:', result[4])
            print('Стационарен' if result[1] < 0.05 else 'Не стационарен')
            print()
        else:
            print(f'Столбец {column} содержит только одно уникальное значение и не может быть проанализирован.')
    else:
        print(f'Столбец {column} не содержит данных.')