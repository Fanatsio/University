import pandas as pd
import numpy as np
from src.neural_network import NeuralNetwork

data = pd.read_csv('lab2/data/data.csv')
X = data.iloc[:, :2].values
y = data.iloc[:, 2:].values

train_size = int(0.8 * len(X))  # 80% для обучения
X_train, X_test = X[:train_size], X[train_size:]  # Обучающая и тестовая выборки
y_train, y_test = y[:train_size], y[train_size:]

# Создание двух нейронных сетей с двумя входами
nn_1 = NeuralNetwork(n_neurons=1, n_inputs=2)  # По формуле (1)
nn_2 = NeuralNetwork(n_neurons=1, n_inputs=2)  # По формуле (4)

print("Обучение сети по формуле (1):")
nn_1.fit_1(X_train, y_train, learning_rate=0.00001, epochs=200)

print("\nОбучение сети по формуле (4):")
nn_2.fit_2(X_train, y_train, learning_rate=0.000001, epochs=200)

predictions_1 = nn_1.predict(X_test)
predictions_2 = nn_2.predict(X_test)

mse_1 = np.mean((np.array(predictions_1).flatten() - np.array(y_test).flatten()) ** 2)
mse_2 = np.mean((np.array(predictions_2).flatten() - np.array(y_test).flatten()) ** 2)

print(f"\nСреднеквадратичная ошибка для сети с формулой (1): {mse_1}")
print(f"Среднеквадратичная ошибка для сети с формулой (4): {mse_2}")

print("\nИтоговые веса для сети с формулой (1):")
print(f"Веса: {nn_1.neurons[0].weights}")

print("\nИтоговые веса для сети с формулой (4):")
print(f"Веса: {nn_2.neurons[0].weights}")
