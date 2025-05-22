import numpy as np

class Neuron:
    def __init__(self, num_inputs):
        self.weights = np.random.uniform(-1, 1, num_inputs)
        self.bias = np.random.uniform(1e-6, 2e-6)
        self.accuracy = 1e-5

    def predict(self, x):
        summator = np.dot(x, self.weights) + self.bias
        return summator

    def update_weights_backprop(self, x, y, learning_rate):
        x = np.array(x)
        prediction = self.predict(x)
        error = y - prediction

        self.weights += learning_rate * error * x
        self.bias += learning_rate * error

    def train(self, inputs, target, learning_rate):
        self.update_weights_backprop(inputs, target, learning_rate)

    def get_weights(self):
        return self.weights, self.bias

class NeuralNetwork:
    def __init__(self, num_neurons, num_inputs_per_neuron):
        self.neurons = [Neuron(num_inputs_per_neuron) for _ in range(num_neurons)]

def create_neural_network(num_neurons, num_inputs_per_neuron):
    return NeuralNetwork(num_neurons, num_inputs_per_neuron)

def train_neural_network(neural_net, training_set, learning_rate, epochs):
    for _ in range(epochs):
        total_loss = 0.0
        for inputs, target in training_set:
            predictions = [neuron.predict(inputs) for neuron in neural_net.neurons]

            errors = np.array([target - prediction for target, prediction in zip([target], predictions)])
            total_loss += 1/2 * np.sum(errors ** 2)

            for neuron, error, input_value in zip(neural_net.neurons, errors, inputs):
                neuron.train(input_value, error, learning_rate)

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

    accuracy = correct_predictions / total_samples
    print(f"Accuracy: {accuracy * 100:.2f}%")

def split_data(data, train_fraction):
    num_samples = len(data)
    train_size = int(train_fraction * num_samples)
    train_data = data[:train_size]
    test_data = data[train_size:]
    return train_data, test_data
