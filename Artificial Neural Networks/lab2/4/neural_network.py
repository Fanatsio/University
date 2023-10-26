import numpy as np
import pandas as pd
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


class Neuron:
    def __init__(self, num_inputs):
        self.weights = np.random.uniform(876, 876, num_inputs)
        self.bias = np.random.uniform(0.000001, 0.000002)
        self.accuracy = 0.00001

    def predict(self, x):
        summator = np.dot(x, self.weights) + self.bias
        return summator

    def update_weights(self, x, y, learning_rate):
        x = np.array(x)
        prediction = self.predict(x)
        error = y - prediction

        # Проверяем, не равны ли prediction и target
        if prediction != y:
            self.weights += learning_rate * error * x
            self.bias += learning_rate * error

    def update_weights_backprop(self, x, y, learning_rate):
        x = np.array(x)
        prediction = self.predict(x)
        error = y - prediction

        # Обновление весов с использованием метода обратного распространения ошибки
        self.weights += learning_rate * error * x
        self.bias += learning_rate * error

    def train(self, inputs, target, learning_rate):
        # Обучение нейрона
        self.update_weights_backprop(inputs, target, learning_rate)

    @staticmethod
    def calculate_mse_for_network(neural_net, test_data):
        total_error = 0
        num_neurons = len(neural_net.neurons)

        for inputs, target in test_data:
            predictions = [neuron.predict(inputs) for neuron in neural_net.neurons]

            errors = [(target - prediction) ** 2 for prediction in predictions]
            total_error += sum(errors)

        # Усредняем ошибку по всем нейронам и элементам тестовой выборки
        mse = total_error / (num_neurons * len(test_data))
        return mse

    def get_weights(self):
        return self.weights, self.bias


class NeuralNetwork:
    def __init__(self, num_neurons, num_inputs_per_neuron):
        self.neurons = [Neuron(num_inputs_per_neuron) for _ in range(num_neurons)]


def create_neural_network(num_neurons, num_inputs_per_neuron):
    return NeuralNetwork(num_neurons, num_inputs_per_neuron)


def train_neural_network(neural_net, training_set, learning_rate, epochs):
    for epoch in range(epochs):
        total_loss = 0.0
        for inputs, target in training_set:
            predictions = [neuron.predict(inputs) for neuron in neural_net.neurons]

            errors = np.array([target - prediction for target, prediction in zip([target], predictions)])
            total_loss += 1/2 * np.sum(errors ** 2)

            for neuron, error, input_value in zip(neural_net.neurons, errors, inputs):
                neuron.train(input_value, error, learning_rate)

    # Выводим среднеквадратичную ошибку после обучения
    mse = total_loss / len(training_set)
    print(f"Mean Squared Error: {mse}")


def evaluate_neural_network(neural_net, test_data):
    correct_predictions = 0
    total_samples = len(test_data)

    for inputs, target in test_data:
        predictions = [neuron.predict(inputs) for neuron in neural_net.neurons]
        predicted_class = 1 if np.mean(predictions) > 0.5 else 0  # Пороговое значение для бинарной классификации

        if predicted_class == target:
            correct_predictions += 1
        # else:
        #     print(f"pred = ({predictions}) = target = ({target})")

    accuracy = correct_predictions / total_samples
    print(f"Accuracy: {accuracy * 100:.2f}%")

def split_data(data, train_fraction):
    num_samples = len(data)
    train_size = int(train_fraction * num_samples)
    train_data = data[:train_size]
    test_data = data[train_size:]
    return train_data, test_data
