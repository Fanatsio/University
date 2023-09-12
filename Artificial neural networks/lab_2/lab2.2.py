import pandas as pd
from src.neural_network import create_neural_network, train_neural_network_1, split_data

data = pd.read_csv('2lab_data.csv')

input_features = data[['x1', 'x2', 'x3', 'x4', 'x5', 'x6']]
target = data['y3']

training_set = list(zip(input_features.values, target.values))

train_data, test_data = split_data(training_set, train_fraction=0.8)

num_neurons = 3
num_inputs_per_neuron = 6
neural_net = create_neural_network(num_neurons, num_inputs_per_neuron)

train_neural_network_1(neural_net, train_data, epochs=100, learning_rate=0.0001, target_error=0.01)

test_error = 0
for inputs, target in test_data:
    prediction = neural_net.neurons[0].predict(inputs)
    test_error += (target - prediction) ** 2

test_error /= len(test_data)
print(f"Ошибка на тестовой выборке для сети с 3 нейронами: {test_error}")

print("\nВеса и смещения после обучения для сети с 3 нейронами:")
for i, neuron in enumerate(neural_net.neurons):
    neuron_weights, neuron_bias = neuron.get_weights()
    print(f"Нейрон {i + 1} - Веса: {neuron_weights}, Смещение: {neuron_bias}")
