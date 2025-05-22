import numpy as np

class Neuron:
    def __init__(self, weights, activation='sigmoid'):
        self.weights = np.array(weights, dtype=float)
        self.activation = activation
        self.output = 0
        self.delta = 0

    def predict(self, x):
        return np.dot(x, self.weights)

    def activate(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, output):
        return output * (1 - output)

    def update_weights(self, x, learning_rate):
        self.weights += learning_rate * self.delta * np.array(x)


class NeuralNetwork:
    def __init__(self):
        # Инициализация сети заданными весами из задания
        self.hidden_layer = [
            Neuron([1, 4, -3]),  # w11
            Neuron([5, -2, 4]),  # w12
            Neuron([2, -3, 1])   # w13
        ]
        self.output_layer = [
            Neuron([2, 4, -2]),  # w21
            Neuron([-3, 2, 3])   # w22
        ]

    def feedforward(self, x):
        hidden_outputs = [neuron.activate(neuron.predict(x)) for neuron in self.hidden_layer]
        final_outputs = [neuron.activate(neuron.predict(hidden_outputs)) for neuron in self.output_layer]
        return hidden_outputs, final_outputs

    def backpropagation(self, x, y, learning_rate):
        hidden_outputs, final_outputs = self.feedforward(x)

        # Обратное распространение для выходного слоя
        for i, neuron in enumerate(self.output_layer):
            error = y[i] - final_outputs[i]
            neuron.delta = error * neuron.sigmoid_derivative(final_outputs[i])

        # Обратное распространение для скрытого слоя
        for i, neuron in enumerate(self.hidden_layer):
            error = sum(output_neuron.delta * output_neuron.weights[i] for output_neuron in self.output_layer)
            neuron.delta = error * neuron.sigmoid_derivative(hidden_outputs[i])

        # Обновление весов
        for neuron in self.output_layer:
            neuron.update_weights(hidden_outputs, learning_rate)
        for neuron in self.hidden_layer:
            neuron.update_weights(x, learning_rate)

    def fit(self, X, y, learning_rate=0.1, tolerance=1e-6, max_epochs=1000):
        for epoch in range(max_epochs):
            total_error = 0
            for i in range(len(X)):
                self.backpropagation(X[i], y[i], learning_rate)
                outputs = self.predict(X[i])
                errors = [(y[i][j] - outputs[j]) ** 2 for j in range(len(outputs))]
                total_error += sum(errors)

            mse = total_error / len(X)
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, MSE: {mse}")

            if mse < tolerance:
                print(f"Training stopped at epoch {epoch} due to tolerance level.")
                break

        # Вывод итоговых весов для проверки
        print("\nFinal weights after training:")
        print("Hidden layer:")
        for i, neuron in enumerate(self.hidden_layer):
            print(f"Neuron {i+1}: {neuron.weights}")
        print("Output layer:")
        for i, neuron in enumerate(self.output_layer):
            print(f"Neuron {i+1}: {neuron.weights}")

    def predict(self, X):
        _, final_outputs = self.feedforward(X)
        return final_outputs


# Данные, совместимые с заданными весами
X_train = np.array([
    [0, 0, 1],  # x3 = 1
    [1, 0, 0],  # x1 = 1
    [0, 1, 0],  # x2 = 1
    [1, 1, 1]   # x1 = x2 = x3 = 1
])

# Целевые выходы, вычисленные с заданными весами
y_train = np.array([
    [0.73105858, 0.04742587],  # Для [0, 0, 1]
    [0.11920292, 0.95257413],  # Для [1, 0, 0]
    [0.98201379, 0.26894142],  # Для [0, 1, 0]
    [0.99987661, 0.99908895]   # Для [1, 1, 1]
])

# Инициализация сети
network = NeuralNetwork()

# Проверка предсказаний до обучения
print("Predictions before training:")
for i in range(len(X_train)):
    pred = network.predict(X_train[i])
    print(f"Input: {X_train[i]}, Predicted: {pred}, Target: {y_train[i]}")

# Обучение сети
network.fit(X_train, y_train, learning_rate=0.001, tolerance=1e-10, max_epochs=1000)

# Проверка предсказаний после обучения
print("\nPredictions after training:")
for i in range(len(X_train)):
    pred = network.predict(X_train[i])
    print(f"Input: {X_train[i]}, Predicted: {pred}, Target: {y_train[i]}")