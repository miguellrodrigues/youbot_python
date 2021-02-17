#  * Copyright (c) 17/02/2021 13:38
#  *
#  * Last modified 17/02/2021 13:38
#  * Miguel L. Rodrigues
#  * All rights reserved
from lib.network.neuron import Neuron
from lib.utils.matrix import Matrix


class Layer:
    VALUES = 0
    ACTIVATED_VALUES = 1
    DERIVED_VALUES = 2

    def __init__(self, neurons_size):
        self.neurons_size = neurons_size

        self.neurons = []

        for i in range(neurons_size):
            self.neurons.append(Neuron(.000, Neuron.SIGM))

    def set_neuron_value(self, index, value):
        self.neurons[index] = value

    def convert_to_matrix(self, convert_type):
        matrix = Matrix(self.neurons_size, 1)

        if convert_type == self.VALUES:
            for i in range(self.neurons_size):
                matrix.set_value(i, 0, self.neurons[i].value)
        elif convert_type == self.ACTIVATED_VALUES:
            for i in range(self.neurons_size):
                matrix.set_value(i, 0, self.neurons[i].activated_value)
        elif convert_type == self.DERIVED_VALUES:
            for i in range(self.neurons_size):
                matrix.set_value(i, 0, self.neurons[i].derived_value)

        return matrix
