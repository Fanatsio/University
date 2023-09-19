class Perceptron:
    def __init__(self):
        self.weights = [1, 1]
        self.bias = -0.5

    @staticmethod
    def step_function(x):
        return 1 if x <= 0 else 0

    def predict(self, x):
        u = x[0] * self.weights[0] + x[1] * self.weights[1]
        return self.step_function(u + self.bias)


neuron = Perceptron()

input_data = [(0, 0), (0, 1), (1, 0), (1, 1)]

for x1, x2 in input_data:
    result = neuron.predict([x1, x2])
    print(f"Input: ({x1}, {x2}), Output: {result}")
