import random


class Perceptron:
    def __init__(self, n):
        self.weights = [random.uniform(0.001, 0.2), random.uniform(0.001, 0.2)]
        self.bias = random.uniform(0.001, 0.2)
        self.accuracy = 0.1

    @staticmethod
    def step_function(x):
        return 1 if x <= 0 else 0
    
    def predict(self, x : list):
        u = x[0] * self.weights[0] + x[1] * self.weights[1]
        return self.step_function(u + self.bias)
    
    def getWeights(self):
        return self.weights


class NeuralNetwork:
    def __init__(self, n):
        pass
    
    def predict(self, x : list):
        pass
    
    def fit(self, x : list, y : list):
        pass
    
neuron = Perceptron(2) # Вместо 2 кол-во входов 

print(neuron.getWeights())