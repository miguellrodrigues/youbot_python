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