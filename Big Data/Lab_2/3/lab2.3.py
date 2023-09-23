import pandas as pd
import numpy as np
from neural_network import plot_3d_graph

x1 = list(range(1, 101))
x2 = list(range(100, 0, -1))
y = [x1_val * 3 + x2_val * 8 for x1_val, x2_val in zip(x1, x2)]

data = {'x1': x1, 'x2': x2, 'y': y}
df = pd.DataFrame(data)

plot_3d_graph(data['x1'], data['x2'], data['y'], '3D график до добавленния шумом', color='b')

noise = np.random.uniform(0.01, 0.1, size=len(x1))
df['y'] += noise

plot_3d_graph(data['x1'], data['x2'], data['y'], '3D график с добавленным шумом', color='r')

df.to_csv('data.3.csv', index=False)
