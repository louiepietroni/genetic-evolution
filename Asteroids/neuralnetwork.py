import math
import numpy as np
import random


class NeuralNetwork:
    def __init__(self, layer_sizes):
        self.layer_sizes = layer_sizes
        self.learning_rate = 0.2
        self.weights = []

        for end_layer_size, start_layer_size in zip(layer_sizes[1:], layer_sizes[:-1]):
            r = 4 * math.sqrt(6 / (end_layer_size + start_layer_size))
            self.weights.append(np.random.uniform(-r, r, size=(end_layer_size, start_layer_size)))

        self.biases = []
        for end_layer_size in layer_sizes[1:]:
            # r = 4 * math.sqrt(6 / end_layer_size)
            self.biases.append(np.random.uniform(-1, 1, size=(end_layer_size, 1)))


    @staticmethod
    def vectorised_sigmoid(n):
        return 1 / (1 + np.exp(-n))

    @staticmethod
    def vectorised_gradient_sigmoid(n):
        return n * (1 - n)

    @staticmethod
    def feed_through_layer(weight_matrix, bias_matrix, input_matrix):
        # Generate layer weighted sum values
        values = weight_matrix @ input_matrix
        values = values + bias_matrix

        # Pass output values through activation function
        values = NeuralNetwork.vectorised_sigmoid(values)
        return values

    def feed_forward(self, inputs_array):
        # Convert input array to column vector
        inputs = np.array(inputs_array).reshape(-1, 1)

        # For each layer, multiply by weights and add the biases
        for weight_matrix, bias_matrix in zip(self.weights, self.biases):
            inputs = self.feed_through_layer(weight_matrix, bias_matrix, inputs)

        # Convert column vector to python list to output
        return inputs.reshape(1, -1).tolist()[0]

    def train(self, inputs_array, targets_array):
        # Convert input array to column vector
        inputs = np.array(inputs_array).reshape(-1, 1)

        layer_outputs = [inputs]

        for weight_matrix, bias_matrix in zip(self.weights, self.biases):
            inputs = self.feed_through_layer(weight_matrix, bias_matrix, inputs)
            layer_outputs.append(inputs)

        # Convert targets array to column vector
        targets = np.array(targets_array).reshape(-1, 1)

        # Error = target - output
        next_errors = targets - layer_outputs[-1]

        for i in range(1, len(self.layer_sizes)):
            current_values = layer_outputs[-i]
            previous_values = layer_outputs[-(i + 1)]

            # Calculate gradients for current layer
            gradients = NeuralNetwork.vectorised_gradient_sigmoid(current_values)
            gradients = gradients * next_errors
            gradients = gradients * self.learning_rate

            # Calculate deltas for current layer
            previous_values = np.transpose(previous_values)
            weight_matrix_deltas = gradients @ previous_values

            # Adjust weights by deltas
            self.weights[-i] = self.weights[-i] + weight_matrix_deltas

            # Adjust biases by deltas - just the hidden gradient
            self.biases[-i] = self.biases[-i] + gradients

            current_weights_transposed = np.transpose(self.weights[-i])
            next_errors = current_weights_transposed @ next_errors

    def copy(self):
        # Makes a new neural network instance with the same weights and biases
        network_copy = NeuralNetwork(self.layer_sizes)
        network_copy.weights = self.weights.copy()
        network_copy.biases = self.biases.copy()
        return network_copy

    @staticmethod
    def mutate_matrix(n, probability):
        # Mutate the values of a matrix by adding a small value to some weights
        new = n
        if random.random() < probability:
            new += random.gauss(0, 1)
        return new


    def mutate(self, probability):
        # For each of the matrices that make up the network, pass it through the mutate function
        mutate_matrix = np.vectorize(NeuralNetwork.mutate_matrix)
        self.weights = [mutate_matrix(matrix, probability) for matrix in self.weights]
        self.biases = [mutate_matrix(matrix, probability) for matrix in self.biases]
