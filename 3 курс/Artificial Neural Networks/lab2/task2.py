import pandas as pd
from src.neural_network import NeuralNetwork
import numpy as np

data = pd.read_csv('lab2/data/2lab_data.csv')
X = data.iloc[:, :6].values
y = data.iloc[:, 6:].values

train_size = int(0.8 * len(X))  # 80% для обучения
X_train, X_test = X[:train_size], X[train_size:]  # Обучающая и тестовая выборки
y_train, y_test = y[:train_size], y[train_size:]

nn_3 = NeuralNetwork(n_neurons=3, n_inputs=6)
nn_3.fit_2(X_train, y_train, learning_rate=0.00001, epochs=100)

# Преобразуем список предсказаний в массив NumPy
predictions_1 = np.array(nn_3.predict(X_test))

if predictions_1.ndim == 1:
    predictions_1 = predictions_1[:, np.newaxis]  # Преобразуем в 2D, если это одномерный массив
if predictions_1.shape[0] != y_test.shape[0]:
    predictions_1 = predictions_1.T  # Меняем форму, чтобы соответствовать (20, 3)
'''
Зачем это нужно:
Предполагается, что predict может вернуть массив в "перевернутой" форме (3,20)(3 предсказания для 20 примеров), а для вычислений нужно (20,3), чтобы каждая строка соответствовала одному примеру из y_test.
Почему это важно:
Для вычисления MSE: mse = np.mean((predictions_1 - y_test) ** 2) требуется, чтобы predictions_1 и y_test имели одинаковую форму (в данном случае (20,3)).
'''

mse = np.mean((predictions_1 - y_test) ** 2)

print(f"\nСреднеквадратичная ошибка для сети: {mse}")

print("\nИтоговые веса для сети:")
for i, neuron in enumerate(nn_3.neurons):
    print(f"Веса {i + 1} нейрона: {neuron.weights}")
