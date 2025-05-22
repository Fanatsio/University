import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('./lab3/lab3_data4.txt', sep='\t', header=None, names=['Тишина', 'Агрессивная', 'Белый шум', 'Классическая', 'Ритмичная'])
print(data)

time_series = {col: data[col].cumsum() / 1000 for col in data.columns}

plt.figure(figsize=(15, 10))
common_xticks = np.linspace(0, 12, num=7)  # Общие позиции отметок по оси X

for i, (name, series) in enumerate(time_series.items()):
    plt.subplot(len(time_series), 1, i + 1)
    plt.vlines(series[0:20], 0, 1, label=name)
    plt.title(name)
    plt.ylim(0, 1.2)
    plt.xlim(0, 12)  # Фиксируем границы оси X
    plt.xticks(common_xticks)  # Устанавливаем одинаковые отметки на всех графиках
    plt.legend()
plt.tight_layout()
plt.show()

heart_rate_series = []
for col in data.columns:
    heart_rate = 60000 / data[col]
    time_index = pd.Series(np.arange(len(heart_rate)), index=pd.date_range(start='2023-11-01', periods=len(heart_rate), freq='ms'))
    ts = pd.Series(heart_rate, index=time_index)
    heart_rate_series.append(ts)

plt.figure(figsize=(12, 8))
for i, ts in enumerate(heart_rate_series):
    plt.subplot(len(heart_rate_series), 1, i+1)
    plt.plot(ts, label=data.columns[i], color='blue')
    
    # Вычисляем статистику
    mean_hr = ts.mean()
    min_hr = ts.min()
    max_hr = ts.max()
    
    # Добавляем среднее значение (линия)
    plt.axhline(mean_hr, color='red', linestyle='--', label='Среднее')
    
    # Добавляем минимальную и максимальную точки
    min_index = ts.idxmin()
    max_index = ts.idxmax()
    plt.scatter([min_index], [min_hr], color='green', marker='o', label='Мин')
    plt.scatter([max_index], [max_hr], color='orange', marker='o', label='Макс')
    
    plt.xlabel('Время')
    plt.ylabel('ЧСС')
    plt.title(f'Сердечный ритм при прослушивании {data.columns[i]}')
    plt.legend()

plt.tight_layout()
plt.show()

