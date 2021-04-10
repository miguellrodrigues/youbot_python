#  * Copyright (c) 17/02/2021 13:43
#  *
#  * Last modified 17/02/2021 13:43
#  * Miguel L. Rodrigues
#  * All rights reserved

from lib.network.layer import Layer
from lib.utils.matrix import Matrix, array_to_matrix, random_double, list_to_matrix
import json

from lib.utils.numbers import random_int, random_item


def sl(lists):
    values = []

    size = len(lists[0])

    p1 = random_int(1, size - 1)
    p2 = random_int(p1, size - 1)

    if p1 == p2:
        p2 += 1

    for _sl in lists:
        x = _sl[:p1]
        y = _sl[p1:p2]
        z = _sl[p2:]

        values.append([x, y, z])

    return values


def combine(slices):
    a = slices[0]
    b = slices[1]

    x = [
        a[0] + b[1] + a[2],
        b[0] + a[1] + b[2]
    ]

    return x


def load_network(path: str):
    with open(path) as file:
        data = json.load(file)

        network = Network(data['topology'])

        for i in range(len(network.weight_matrices)):
            network.weight_matrices[i].data = data['weight_matrices'][i]

        return network


def cross_over(net, father, mother):
    for i in range(len(net.weight_matrices)):
        father_weight = father.weight_matrices[i]
        mother_weight = mother.weight_matrices[i]

        slices = sl([father_weight.to_list(), mother_weight.to_list()])

        child = random_item(combine(slices))

        net.weight_matrices[i] = list_to_matrix(child, father_weight.rows, father_weight.cols)


class Network:
    def __init__(self, topology):
        self.topology = topology
        self.topology_size = len(topology)

        self.layers = []
        self.weight_matrices = []

        self.errors = []
        self.derived_errors = []

        self.bias = 0.01

        self.global_error = 0.0

        self.learning_rate = 0.0001

        self.output_index = self.topology_size - 1

        self.fitness = .0

        for i in range(self.topology_size):
            self.layers.append(Layer(topology[i]))

        for i in range(self.topology_size - 1):
            weight_matrix = Matrix(topology[i + 1], topology[i], True)

            self.weight_matrices.append(weight_matrix)

        for i in range(topology[self.topology_size - 1]):
            self.errors.append(.0)
            self.derived_errors.append(.0)

    def save(self, path: str):
        data = {'topology': self.topology, 'weight_matrices': []}

        for matrix in self.weight_matrices:
            data['weight_matrices'].append(matrix.data)

        with open(path, "w") as file:
            json.dump(data, file)

    def set_current_input(self, input_matrix: Matrix):
        for i in range(input_matrix.rows):
            self.layers[0].set_neuron_value(i, input_matrix.get_value(i, 0))

    def feed_forward(self):
        for i in range(self.topology_size - 1):
            if i != 0:
                left = self.layers[i].convert_to_matrix(Layer.ACTIVATED_VALUES)
            else:
                left = self.layers[i].convert_to_matrix(Layer.VALUES)

            right = self.weight_matrices[i]

            r = right.multiply(left)

            for j in range(r.rows):
                self.layers[i + 1].set_neuron_value(j, (r.get_value(j, 0) + self.bias))

    def set_errors(self, meta: Matrix):
        if meta.rows == 0:
            print('Invalid meta matrix')
            return

        output_layer_index = self.topology_size - 1

        if meta.rows != self.layers[output_layer_index].neurons_size:
            print('Invalid meta matrix')
            return

        self.global_error = 0.0

        output_neurons = self.layers[output_layer_index].neurons
        for i in range(meta.rows):
            t = meta.get_value(i, 0)
            y = output_neurons[i].get_derived_value()

            self.errors[i] = 0.5 * pow((t - y), 2.0)
            self.derived_errors[i] = (y - t)

            self.global_error += self.errors[i]

    def back_propagation(self):
        weights = []

        index_output_layer = self.topology_size - 1

        gradients = Matrix(self.topology[index_output_layer], 1)

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

                delta_value = delta_value * self.learning_rate

                temp_weights.set_value(i, j, (original_value - delta_value))

        weights.append(temp_weights)

        i = index_output_layer - 1

        while i > 0:
            _gradients = Matrix(gradients.rows, gradients.cols)

            _gradients.copy(gradients)

            transposed_weights = self.weight_matrices[i].transpose()

            gradients = transposed_weights.multiply(_gradients)

            # # # # # # # # # # # # # # # # # # # # # #

            derived_values = self.layers[i].convert_to_matrix(Layer.DERIVED_VALUES)

            layer_gradients = derived_values.hadamard(gradients)

            for j in range(layer_gradients.rows):
                for k in range(layer_gradients.cols):
                    gradients.set_value(j, k, layer_gradients.get_value(j, k))

            if i == 1:
                layer_values = self.layers[0].convert_to_matrix(Layer.VALUES)
            else:
                layer_values = self.layers[i - 1].convert_to_matrix(Layer.ACTIVATED_VALUES)

            delta_weights = gradients.multiply(layer_values.transpose())

            _temp_weights = Matrix(
                self.weight_matrices[i - 1].rows,
                self.weight_matrices[i - 1].cols
            )

            for j in range(_temp_weights.rows):
                for k in range(_temp_weights.cols):
                    original_value = self.weight_matrices[i - 1].get_value(j, k)
                    delta_value = delta_weights.get_value(j, k)

                    delta_value = delta_value * self.learning_rate

                    _temp_weights.set_value(j, k, (original_value - delta_value))

            weights.append(_temp_weights)

            i -= 1

        self.weight_matrices = []

        for matrix in reversed(weights):
            self.weight_matrices.append(matrix)

    def train(self, input_data, meta):
        self.set_current_input(array_to_matrix(input_data))

        self.feed_forward()
        self.set_errors(array_to_matrix(meta))
        self.back_propagation()

    def predict(self, input_data):
        self.set_current_input(array_to_matrix(input_data))
        self.feed_forward()

        return self.layers[self.output_index].convert_to_matrix(Layer.ACTIVATED_VALUES)

    def set_fitness(self, fitness):
        self.fitness = fitness

    def get_fitness(self):
        return self.fitness

    def mutate(self, rate):
        for weight_matrix in self.weight_matrices:
            count = int(rate * weight_matrix.cols)

            random_row = random_int(0, weight_matrix.rows - 1)

            for i in range(count):
                random_col = random_int(0, weight_matrix.cols - 1)

                value = weight_matrix.get_value(random_row, random_col)

                weight_matrix.set_value(random_row, random_col, value + random_double(-1.0, 1.0))

    def assign(self, other):
        for i in range(len(self.weight_matrices)):
            self.weight_matrices[i].data = other.weight_matrices[i].data
