import numpy as np
from .neuron import Neuron

class NeuralNetwork:
    def __init__(self, n_inputs, n_hidden, n_outputs):
        # Создание скрытого слоя
        self.hidden_layer = [Neuron(n_inputs) for _ in range(n_hidden)]
        # Создание выходного слоя
        self.output_layer = [Neuron(n_hidden) for _ in range(n_outputs)]

    def feedforward(self, x):
        # Прямой проход
        hidden_outputs = [neuron.activate(neuron.predict(x)) for neuron in self.hidden_layer]
        final_outputs = [neuron.activate(neuron.predict(hidden_outputs)) for neuron in self.output_layer]
        return hidden_outputs, final_outputs

    def backpropagation(self, x, y, learning_rate):
        # Прямой проход для предсказания
        hidden_outputs, final_outputs = self.feedforward(x)

        # Ошибка на выходном слое
        for i, neuron in enumerate(self.output_layer):
            error = y[i] - final_outputs[i]
            neuron.delta = error * neuron.sigmoid_derivative(final_outputs[i])

        # Ошибка на скрытом слое
        for i, neuron in enumerate(self.hidden_layer):
            error = sum(output_neuron.delta * output_neuron.weights[i] for output_neuron in self.output_layer)
            neuron.delta = error * neuron.sigmoid_derivative(hidden_outputs[i])

        # Обновление весов выходного слоя
        for neuron in self.output_layer:
            neuron.update_weights(hidden_outputs, learning_rate)

        # Обновление весов скрытого слоя
        for neuron in self.hidden_layer:
            neuron.update_weights(x, learning_rate)

    def fit(self, X, y, learning_rate=0.01, epochs=1000):
        for epoch in range(epochs):
            total_error = 0
            for i in range(len(X)):
                self.backpropagation(X[i], y[i], learning_rate)
                for j, neuron in enumerate(self.output_layer):
                    output = neuron.activate(neuron.predict(X[i]))  # Исправлено
                    error = y[i][j] - output
                    total_error += error ** 2
                    # Вывод информации об ошибке, весах и предсказании
                    print(
                        f"i = {i}, Epoch {epoch + 1}, Error {error},"
                        f" Веса {neuron.weights}, Предикт {output}, Таргет {y[i][j]}")

    def calculate_mse(self, X, y):
        total_error = 0
        for i in range(len(X)):
            outputs = self.predict(X[i])
            for j in range(len(outputs)):
                total_error += (y[i][j] - outputs[j]) ** 2
        mse = total_error / (len(X) * len(y[0]))  # Учитываем количество примеров и выходов
        return mse

    def predict(self, X):
        # Предсказание
        _, final_outputs = self.feedforward(X)
        return final_outputs
