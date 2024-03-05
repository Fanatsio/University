import random

class Neuron:
    def __init__(self, n):
        # Инициализация весов случайными значениями
        self.weights = [random.randint(1, 200) / 1000 for _ in range(n)]

    def predict(self, x: list) -> float:
        # Предсказание на основе входных данных и весов
        return x[0] * self.weights[0] + x[1] * self.weights[1]

class NeuralNetwork:
    def __init__(self, n):
        # Создание нейронов для нейронной сети
        self.neurons = [Neuron(2) for _ in range(n)]
        # Установка скорости обучения
        self.a = 0.00005

    def predict(self, x: list):
        # Предсказание на основе первого нейрона
        return self.neurons[0].predict(x)
    
    def fit(self, x_train: list, y_train: list, x_test: list, y_test: list, learning_rate: float, desired_error: float, max_iterations: int):
        for neuron in self.neurons:
            neuron.weights = [random.randint(1, 200) / 1000 for _ in range(len(neuron.weights))]

        self.a = learning_rate
        mse_train = float('inf')
        mse_test = float('inf')
        iteration = 0

        while mse_train > desired_error and iteration < max_iterations:
            mse_train = 0
            for i in range(len(x_train)):
                y_pred = self.predict(x_train[i])
                error = y_train[i] - y_pred
                for j in range(len(self.neurons[0].weights)):
                    self.neurons[0].weights[j] += self.a * error * x_train[i][j]
                mse_train += error ** 2
            mse_train /= len(x_train)

            mse_test = 0
            for i in range(len(x_test)):
                y_pred = self.predict(x_test[i])
                error = y_test[i] - y_pred
                mse_test += error ** 2
            mse_test /= len(x_test)

            iteration += 1

        print(f"Mean square error (train) -> {mse_train}")
        print(f"Mean square error (test) -> {mse_test}")
        

        return self.neurons[0].weights

    def fit1(self, x_train: list, y_train: list, x_test: list, y_test: list):
        mse_train = 0
        length_train = len(x_train)

        # Обучение на обучающей выборке
        for i in range(length_train):
            y_pred = self.predict(x_train[i])
            # Вычисление среднеквадратичной ошибки на обучающей выборке
            mse_train += ((y_pred - y_train[i]) ** 2) / length_train
            # Обновление весов нейрона
            self.neurons[0].weights[0] += (y_train[i] - y_pred) / sum(self.neurons[0].weights)
            self.neurons[0].weights[1] += (y_train[i] - y_pred) / sum(self.neurons[0].weights)

        # Оценка на тестовой выборке
        mse_test = 0
        length_test = len(x_test)
        for i in range(length_test):
            y_pred = self.predict(x_test[i])
            mse_test += ((y_pred - y_test[i]) ** 2) / length_test

        print(f"Mean square error (train) -> {mse_train}")
        print(f"Mean square error (test)  -> {mse_test}")

        return [self.neurons[0].weights[0], self.neurons[0].weights[1]]

    def fit2(self, x_train: list, y_train: list, x_test: list, y_test: list):
        mse_train = 0
        length_train = len(x_train)

        # Обучение на обучающей выборке
        for i in range(length_train):
            y_pred = self.predict(x_train[i])
            mse_train += ((y_pred - y_train[i]) ** 2) / length_train
            # Обновление весов нейрона с учетом скорости обучения
            self.neurons[0].weights[0] -= self.a * (y_pred - y_train[i]) * x_train[i][0]
            self.neurons[0].weights[1] -= self.a * (y_pred - y_train[i]) * x_train[i][1]

        # Оценка на тестовой выборке
        mse_test = 0
        length_test = len(x_test)
        for i in range(length_test):
            y_pred = self.predict(x_test[i])
            mse_test += ((y_pred - y_test[i]) ** 2) / length_test

        print(f"Mean square error (train) -> {mse_train}")
        print(f"Mean square error (test)  -> {mse_test}")

        return [self.neurons[0].weights[0], self.neurons[0].weights[1]]

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

nn = NeuralNetwork(1)
nn1 = NeuralNetwork(1)
nn2 = NeuralNetwork(1)

print("------------")
print(nn1.fit1(x_train, y_train, x_test, y_test))
print("------------")
print(nn2.fit2(x_train, y_train, x_test, y_test))
print("------------")

# Задаем параметры обучения
learning_rate = 0.1
desired_error = 0.01
max_iterations = 1000

# Обучаем нейронную сеть
print("------------")
#print(nn.fit(x_train, y_train, x_test, y_test, learning_rate, desired_error, max_iterations))
