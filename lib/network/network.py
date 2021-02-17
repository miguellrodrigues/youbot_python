#  * Copyright (c) 17/02/2021 13:43
#  *
#  * Last modified 17/02/2021 13:43
#  * Miguel L. Rodrigues
#  * All rights reserved
from lib.network.layer import Layer
from lib.utils.matrix import Matrix


class Network:
    def __init__(self, topology):
        self.topology = topology
        self.topology_size = len(topology)

        self.layers = []
        self.weight_matrices = []

        self.errors = []
        self.derived_errors = []

        self.bias = .01

        self.global_error = .0

        self.learning_rate = .001

        for i in range(self.topology_size):
            self.layers.append(Layer(topology[i]))

        for i in range(self.topology_size - 1):
            weight_matrix = Matrix(topology[i + 1], topology[i], True)

            self.weight_matrices.append(weight_matrix)

        for i in range(topology[self.topology_size - 1]):
            self.errors.append(.0)
            self.derived_errors.append(.0)

    def set_current_input(self, input_matrix: Matrix):
        for i in range(input_matrix.rows):
            self.layers[0].set_neuron_value(i, input_matrix.get_value(i, 0))

    def feed_forward(self):
        left = None
        right = None
        r = None

        for i in range(self.topology_size - 1):
            if i != 0:
                left = self.layers[i].convert_to_matrix(Layer.ACTIVATED_VALUES)
            else:
                left = self.layers[i].convert_to_matrix(Layer.VALUES)

            right = self.weight_matrices[i]

            r = right.multiply(left)

            for j in range(r.rows):
                self.layers[i + 1].set_neuron_value(j, r.get_value(j, 0) + self.bias)

    def set_errors(self, meta: Matrix):
        if meta.rows == 0:
            print('Invalid meta matrix')
            return

        output_layer_index = self.topology_size - 1

        if meta.rows != self.layers[output_layer_index].neurons_size:
            print('Invalid meta matrix')
            return

        self.global_error = .0

        output_neurons = self.layers[output_layer_index].neurons
        for i in range(meta.rows):
            t = meta.get_value(i, 0)
            y = output_neurons[i].derived_value

            self.errors[i] = 0.5 * pow((t - y), 2)
            self.derived_errors[i] = (y - t)

            self.global_error += self.errors[i]

    def back_propagation(self):
        weights = []

        index_output_layer = self.topology_size - 1

        gradients = Matrix(self.topology_size[index_output_layer], 1)

        derived_output_values = self.layers[index_output_layer].convert_to_matrix(Layer.DERIVED_VALUES)

        for i in range(self.topology[index_output_layer]):
            error = self.derived_errors[i]
            output = derived_output_values.get_value(i, 0)

            gradient = error * output

            gradients.set_value(i, 0, gradient)

        last_hidden_layer_activated = self.layers[index_output_layer - 1].convert_to_matrix(Layer.ACTIVATED_VALUES)

        delta_weights_last_hidden = gradients.multiply(last_hidden_layer_activated.transpose())

        temp_weights = Matrix(
            self.topology[index_output_layer],
            self.topology[index_output_layer - 1]
        )

        for i in range(temp_weights.rows):
            for j in range(temp_weights.cols):
                original_value = self.weight_matrices[index_output_layer - 1].get_value(i, j)
                delta_value = delta_weights_last_hidden.get_value(i, j)

                delta_value *= self.learning_rate

                temp_weights.set_value(i, j, (original_value - delta_value))

        weights.append(temp_weights)

        for i in reversed(range(index_output_layer - 1)):
            _gradients = Matrix(gradients.rows, gradients.cols)

            _gradients.assign(gradients)

            transposed_weights = self.weight_matrices[i].transpose()

            gradients = transposed_weights.multiply(_gradients)

            # # # # # # # # # # # # # # # # # # # # # #

            derived_values = self.layers[i].convert_to_matrix(Layer.DERIVED_VALUES)

            layer_gradients = derived_values.hadamard(gradients)

            for j in range(layer_gradients.rows):
                for k in range(layer_gradients.cols):
                    gradients.set_value(j, k, layer_gradients.get_value(j, k))

            layer_values = self.layers[0].convert_to_matrix(Layer.VALUES) if i == 1 else self.layers[
                i - 1].convert_to_matrix(Layer.ACTIVATED_VALUES)

            delta_weights = gradients.multiply(layer_values.transpose())

            _temp_weights = Matrix(
                self.weight_matrices[i - 1].rows,
                self.weight_matrices[i - 1].cols
            )

            for j in range(_temp_weights.rows):
                for k in range(_temp_weights.cols):
                    original_value = self.weight_matrices[i - 1].get_value(j, k)
                    delta_value = delta_weights.get_value(j, k)

                    delta_value *= self.learning_rate

                    _temp_weights.set_value(j, k, (original_value - delta_value))

            weights.append(_temp_weights)

        self.weight_matrices = []

        for matrix in reversed(weights):
            self.weight_matrices.append(matrix)

    def train(self, input: Matrix, meta: Matrix):
        self.set_current_input(input)

        self.feed_forward()
        self.set_errors(meta)
        self.back_propagation()

    def predict(self, input):
        self.set_current_input(input)
        self.feed_forward()

        return self.layers[self.topology_size - 1].convert_to_matrix(Layer.ACTIVATED_VALUES)
