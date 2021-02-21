#  * Copyright (c) 17/02/2021 13:28
#  *
#  * Last modified 17/02/2021 13:28
#  * Miguel L. Rodrigues
#  * All rights reserved

def sigmoid_activation(value):
    return value / (1 + abs(value))


def sigmoid_derived(value):
    return 1 / pow((1 + abs(value)), 2.0)


class Neuron:
    RELU = 0
    SIGM = 1
    TANH = 2

    def __init__(self, value, activation_type):
        self.value = value
        self.activation_type = activation_type

        self.activated_value = .0
        self.derived_value = .0

        self.set_value(value)

    def set_value(self, value):
        self.value = value

        self.activate()
        self.derive()

    def activate(self):
        self.activated_value = sigmoid_activation(self.value)

    def derive(self):
        self.derived_value = sigmoid_derived(self.activated_value)

    def get_value(self):
        return self.value

    def get_activated_value(self):
        return self.activated_value

    def get_derived_value(self):
        return self.derived_value
