import random

class Neuron:
    def __init__(self, n):
        self.weights = [random.randint(1, 200) / 1000 for _ in range(n)]

    def predict(self, x: list) -> float:
        return x[0] * self.weights[0] + x[1] * self.weights[1]

class NeuralNetwork:
    def __init__(self, n):
        self.neurons = [Neuron(2) for _ in range(n)]
        self.a = 0.00005

    def predict(self, x: list):
        return self.neurons[0].predict(x)

    def fit(self, x_train: list, y_train: list, x_test: list, y_test: list, learning_rate: float, desired_error: float, max_iterations: int):
        self.a = learning_rate
        mse_train = 0
        mse_test = 0
        iteration = 0

        while mse_train > desired_error and iteration < max_iterations:
            #mse_train = 0
            length_train = len(x_train)
            for i in range(length_train):
                y_pred = self.predict(x_train[i])
                # error = y_train[i] - y_pred
                # for j in range(len(self.neurons[0].weights)):
                #     self.neurons[0].weights[j] += self.a * error * x_train[i][j]
                mse_train += ((y_pred - y_train[i]) ** 2) / length_train
                
                self.neurons[0].weights[0] += (y_train[i] - y_pred) / sum(self.neurons[0].weights)
                self.neurons[0].weights[1] += (y_train[i] - y_pred) / sum(self.neurons[0].weights)
                
            mse_train /= len(x_train)

            #mse_test = 0
            length_test = len(x_test)
            for i in range(len(x_test)):
                y_pred = self.predict(x_test[i])
                #error = y_test[i] - y_pred
                mse_test += ((y_pred - y_test[i]) ** 2) / length_test
            mse_test /= len(x_test)

            iteration += 1

        print(f"Mean square error (train) -> {mse_train}")
        print(f"Mean square error (test) -> {mse_test}")

        return self.neurons[0].weights

# Чтение данных из файла CSV
data_file = 'data.csv'
data = []
with open(data_file, 'r') as file:
    for line in file:
        if not line.startswith('x1'):
            values = line.strip().split(',')
            x = [int(values[0]), int(values[1])]
            y = float(values[2])
            data.append((x, y))

# Разделение данных на обучающую и тестовую выборки
split_index = int(0.8 * len(data))
train_data = data[:split_index]
test_data = data[split_index:]

# Разделение x и y для обучающей и тестовой выборок
x_train, y_train = zip(*train_data)
x_test, y_test = zip(*test_data)

# Создание и обучение нейронной сети
nn = NeuralNetwork(1)

# Задаем параметры обучения
learning_rate = 0.1
desired_error = 0.01
max_iterations = 1000

# Обучаем нейронную сеть
trained_weights = nn.fit(x_train, y_train, x_test, y_test, learning_rate, desired_error, max_iterations)
print("Trained weights:", trained_weights)
