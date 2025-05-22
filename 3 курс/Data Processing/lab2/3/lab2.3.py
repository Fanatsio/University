import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_3d_graph(x1, x2, y, title, color='b'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x1, x2, y, c=color, marker='o')
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_zlabel('Y')
    plt.title(title)
    plt.show()

x1 = list(range(1, 101))
x2 = list(range(100, 0, -1))
y = [x1_val * 6 + x2_val * 5 for x1_val, x2_val in zip(x1, x2)]

data = {'x1': x1, 'x2': x2, 'y': y}
df = pd.DataFrame(data)

plot_3d_graph(df['x1'], df['x2'], df['y'], '3D график до добавленния шумом', color='b')

noise = np.random.uniform(0.01, 0.1, size=len(x1))
df['y'] += noise

plot_3d_graph(df['x1'], df['x2'], df['y'], '3D график с добавленным шумом', color='r')

df.to_csv('data.3.csv', index=False)
