import pandas as pd
import numpy as np
from neural_network import plot_3d_graph

# Создайте списки для x1, x2 и y
x1 = list(range(1, 101))  # x1 от 1 до 100
x2 = list(range(100, 0, -1))  # x2 от 100 до 1
y = [x1_val * 3 + x2_val * 8 for x1_val, x2_val in zip(x1, x2)]  # Вычислите y по формуле

# Создайте DataFrame
data = {'x1': x1, 'x2': x2, 'y': y}
df = pd.DataFrame(data)

plot_3d_graph(df['x1'], df['x2'], df['y'],
              '3D график до добавленния шумом', color='b')

# Добавляем небольшой шум в интервале [5, 100]
noise = np.random.uniform(0.01, 0.1, size=len(x1))
df['y'] += noise  # Изменяем данные в DataFrame

plot_3d_graph(df['x1'], df['x2'], df['y'],
              '3D график с добавленным шумом', color='r')

# Сохраните данные в формате CSV
df.to_csv('data.3.csv', index=False)
