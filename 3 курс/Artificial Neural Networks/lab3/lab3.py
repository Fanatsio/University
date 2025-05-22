from src.neural_network import NeuralNetwork
import numpy as np
import pandas as pd

data = pd.read_csv('lab3/data/3lab_data.csv')
X = data[['x1', 'x2', 'x3']].values
y = data[['y1', 'y2']].values

network = NeuralNetwork(n_inputs=3, n_hidden=3, n_outputs=2)

# 1. Нормализация данных
X_max = np.max(X, axis=0)
y_max = np.max(y, axis=0)
X_normalized = X / X_max
y_normalized = y / y_max

# 2. Обучение нейронной сети на нормализованных данных
network.fit(X_normalized, y_normalized, learning_rate=0.1, epochs=1000)
