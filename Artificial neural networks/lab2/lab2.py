import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Веса для входного слоя и скрытого слоя
        self.weights_input_hidden = np.random.randn(self.input_size, self.hidden_size)
        # Веса для скрытого слоя и выходного слоя
        self.weights_hidden_output = np.random.randn(self.hidden_size, self.output_size)
        
        # Смещения для скрытого слоя и выходного слоя
        self.bias_hidden = np.zeros((1, self.hidden_size))
        self.bias_output = np.zeros((1, self.output_size))
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def feedforward(self, X):
        # Прямое распространение
        self.hidden_sum = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        self.activated_hidden = self.sigmoid(self.hidden_sum)
        self.output_sum = np.dot(self.activated_hidden, self.weights_hidden_output) + self.bias_output
        self.activated_output = self.sigmoid(self.output_sum)
        return self.activated_output
    
    def backward(self, X, y, output):
        # Обратное распространение ошибки
        self.output_error = y - output
        self.output_delta = self.output_error * self.sigmoid_derivative(output)
        
        self.hidden_error = self.output_delta.dot(self.weights_hidden_output.T)
        self.hidden_delta = self.hidden_error * self.sigmoid_derivative(self.activated_hidden)
        
        # Обновление весов и смещений
        self.weights_hidden_output += self.activated_hidden.T.dot(self.output_delta)
        self.weights_input_hidden += X.T.dot(self.hidden_delta)
        self.bias_output += np.sum(self.output_delta, axis=0)
        self.bias_hidden += np.sum(self.hidden_delta, axis=0)
        
    def train(self, X, y, epochs):
        for epoch in range(epochs):
            output = self.feedforward(X)
            self.backward(X, y, output)
            
            if epoch % 1000 == 0:
                loss = np.mean(np.square(y - self.feedforward(X)))
                print(f"Epoch {epoch}, Loss: {loss:.4f}")
                
# Пример использования
if __name__ == "__main__":
    # Пример данных
    X = np.array([[0, 0],
                  [0, 1],
                  [1, 0],
                  [1, 1]])
    y = np.array([[0], [1], [1], [0]])
    
    # Создание нейронной сети с произвольным количеством входов
    input_size = 2  # Количество входов
    hidden_size = 4  # Количество нейронов в скрытом слое
    output_size = 1  # Количество выходов
    
    nn = NeuralNetwork(input_size, hidden_size, output_size)
    
    # Обучение сети
    nn.train(X, y, epochs=10000)
    
    # Вывод результата
    print("Output after training:")
    print(nn.feedforward(X))
