import numpy as np

class Neuron:
    def __init__(self, n, activation='sigmoid'):
        # Инициализация весов для нейрона
        self.weights = np.random.uniform(0.001, 0.02, n)
        self.activation = activation  # Добавляем возможность выбора активации
        self.output = 0  # Выходное значение нейрона
        self.delta = 0   # Ошибка для обратного распространения

    def predict(self, x):
        # Прямой проход: скалярное произведение + смещение
        return np.dot(x, self.weights)

    def activate(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, output):
        # Производная сигмоиды
        return output * (1 - output)

    def update_weights(self, x, learning_rate):
        # Обновление весов и смещения для одного нейрона
        self.weights += learning_rate * self.delta * np.array(x)
