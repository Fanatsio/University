import numpy as np

class Neuron:
    def __init__(self, n):
        self.weights = np.random.uniform(0.001, 0.02, n)

    def predict(self, x):
        return np.dot(x, self.weights)

    # Обновление весов по формуле (1) (простой градиентный спуск)
    def update_weights_1(self, x, error, learning_rate):
        self.weights += learning_rate * error * np.array(x) / np.sum(self.weights)

    # Обновление весов по формуле (4) (Уидроу-Хофф)
    def update_weights_2(self, x, error, learning_rate):
        grad = -2 * error * np.array(x)
        self.weights -= learning_rate * grad
