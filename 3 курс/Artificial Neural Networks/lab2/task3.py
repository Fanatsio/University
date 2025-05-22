from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import csv
from tqdm import tqdm

class RedDetectionNeuron:
    def __init__(self, input_size):
        self.weights = np.random.randn(input_size)
        self.bias = np.random.randn()

    def predict(self, x):
        return 1 if np.dot(self.weights, x) + self.bias > 0 else 0

    def update_weights(self, x, error, learning_rate):
        self.weights += learning_rate * error * np.array(x)
        self.bias += learning_rate * error

# Чтение обучающей выборки
train_pixels = []
train_labels = []
with open('lab2/data/2lab_data_3_train.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Пропуск заголовка
    for row in reader:
        r, g, b, y = map(int, row)
        train_pixels.append([r, g, b])
        train_labels.append(y)

# Чтение тестовой выборки
test_pixels = []
test_labels = []
with open('lab2/data/2lab_data_3_test.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Пропуск заголовка
    for row in reader:
        r, g, b, y = map(int, row)
        test_pixels.append([r, g, b])
        test_labels.append(y)

# Создание и обучение нейрона
red_neuron = RedDetectionNeuron(3)
learning_rate = 0.0001
epochs = 1000
print("Обучение нейрона...")
for _ in tqdm(range(epochs), desc="Эпохи обучения"):
    for pixel, label in zip(train_pixels, train_labels):
        output = red_neuron.predict(pixel)
        error = label - output
        red_neuron.update_weights(pixel, error, learning_rate)

# Проверка точности на тестовой выборке
correct = 0
for pixel, label in zip(test_pixels, test_labels):
    prediction = red_neuron.predict(pixel)
    if prediction == label:
        correct += 1
accuracy = correct / len(test_labels)
print(f"Точность на тестовой выборке: {accuracy * 100:.2f}%")

# Открытие изображения
image = Image.open('lab2/data/pic.jpg')
a = np.asarray(image)

# Прогнозирование на пикселях изображения с прогресс-баром
reshaped_a = a.reshape(-1, 3)
result = []
print("Обработка изображения...")
for pixel in tqdm(reshaped_a, desc="Пиксели"):
    result.append(red_neuron.predict(pixel))

# Отображение результата
res_image = np.array(result).reshape(a.shape[:2])
plt.imshow(res_image, cmap='gray')
plt.show()
