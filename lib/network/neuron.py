#  * Copyright (c) 17/02/2021 13:28
#  *
#  * Last modified 17/02/2021 13:28
#  * Miguel L. Rodrigues
#  * All rights reserved
from math import tanh


def sigmoid_activation(value):
    return value / (1 + abs(value))


def sigmoid_derived(value):
    return 1 / pow(1 + abs(value), 2)


class Neuron:
    RELU = 0
    SIGM = 1
    TANH = 2

    def __init__(self, value, activation_type):
        self.value = value
        self.activation_type = activation_type

        self.activated_value = .0
        self.derived_value = .0

    def set_value(self, value):
        self.value = value

        self.activate()
        self.derive()

    def activate(self):
        if self.activation_type == self.RELU:
            if self.value > 0:
                self.activated_value = self.value
            else:
                self.activated_value = 0
        elif self.activation_type == self.SIGM:
            self.activated_value = sigmoid_activation(self.value)
        elif self.activation_type == self.TANH:
            self.activated_value = tanh(self.value)
        else:
            self.activated_value = sigmoid_activation(self.value)

    def derive(self):
        if self.activation_type == self.RELU:
            if self.activated_value > 0:
                self.derived_value = 1
            else:
                self.derived_value = 0
        elif self.activation_type == self.SIGM:
            self.derived_value = sigmoid_derived(self.activated_value)
        elif self.activation_type == self.TANH:
            self.derived_value = (1 - pow(tanh(self.activated_value), 2))
        else:
            self.derived_value = sigmoid_derived(self.activated_value)
