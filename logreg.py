import numpy as np


# Sigmoid function
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Logistic Regression implementation
class LogisticRegression:
    def __init__(self, learning_rate=0.00001, num_iterations=10000):
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.weights = None
        self.bias = None

    def fit(self, inputs, outputs):
        (num_samples, num_features) = inputs.shape
        self.weights = np.zeros(num_features)
        self.bias = 0

        # Gradient descent optimization
        for _ in range(self.num_iterations):
            linear_model = np.dot(inputs, self.weights) + self.bias
            predictions = sigmoid(linear_model)

            # Compute gradients
            dw = (1 / num_samples) * np.dot(inputs.T, (predictions - outputs))
            db = (1 / num_samples) * np.sum(predictions - outputs)

            # Update parameters
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, inputs):
        linear_model = np.dot(inputs, self.weights) + self.bias
        prediction = sigmoid(linear_model)
        return prediction