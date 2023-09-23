from PIL import Image
import numpy as np
from neural_network import create_neural_network, train_neural_network, split_data, Neuron

image = Image.open('kotik.jpg')

image_array = np.array(image)

target_color = [10, 106, 69]

pixels_with_color = []
pixels_without_color = []

for i in range(image_array.shape[0]):
    for j in range(image_array.shape[1]):
        pixel = image_array[i, j]
        if np.array_equal(pixel, target_color):
            pixels_with_color.append(pixel)
        else:
            pixels_without_color.append(pixel)

pixels_with_color = np.array(pixels_with_color)
pixels_without_color = np.array(pixels_without_color)

labels_with_color = np.ones((pixels_with_color.shape[0], 1))
labels_without_color = np.zeros((pixels_without_color.shape[0], 1))

data = np.vstack((pixels_with_color, pixels_without_color))
labels = np.vstack((labels_with_color, labels_without_color))

network = create_neural_network(1, 3)

training_set = [(pixel, label) for pixel, label in zip(data, labels)]

train_data, test_data = split_data(training_set, train_fraction=0.8)

train_neural_network(network, train_data, epochs=100)

print(Neuron.calculate_mse_for_network(network, test_data))

print("\nВеса после обучения для сети с одним нейроном:")
neuron_weights, bias = network.neurons[0].get_weights()
print(f"Веса нейрона: {neuron_weights}")
print(f"Смещение (bias): {bias}")
