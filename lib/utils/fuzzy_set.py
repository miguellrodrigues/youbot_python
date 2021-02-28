#  * Copyright (c) 27/02/2021 21:30
#  *
#  * Last modified 27/02/2021 21:30
#  * Miguel L. Rodrigues
#  * All rights reserved

from math import exp


def cartesian_product_pertinence(fuzzy_sets, values):
    if len(fuzzy_sets) != len(values):
        print("cartesian_product_pertinence, bad arguments")
        return None

    values = []

    for i in range(len(fuzzy_sets)):
        values.append(fuzzy_sets[i].calculate_pertinence(values[i]))

    return min(values)


def de_fuzzy(values_set, pertinence_set):
    sum_a = .0
    sum_b = .0

    for i in range(len(values_set)):
        values = values_set[i]

        for j in range(len(values)):
            value = values[j]
            pertinence = pertinence_set[i]

            sum_a += value * pertinence
            sum_b += pertinence

    return sum_a / sum_b


class FuzzySet:
    TRIANGULAR = 0
    TRAPEZOIDAL = 1
    SINUSOIDAL = 2

    def __init__(self, set_type, values):
        self.type = set_type

        self.values = values

    def calculate_pertinence(self, value):
        if self.type == 0:
            return self._calculate_triangular_pertinence(value)
        elif self.type == 1:
            return self._calculate_trapezoidal_pertinence(value)
        else:
            return self._calculate_sinusoidal_pertinence(value)

    def _calculate_triangular_pertinence(self, value):
        if value <= self.values[0]:
            return .0
        elif self.values[0] < value <= self.values[1]:
            return (value - self.values[0]) / (self.values[1] - self.values[0])
        elif self.values[1] <= value <= self.values[2]:
            return (value - self.values[2]) / (self.values[1] - self.values[2])
        else:
            return .0

    def _calculate_trapezoidal_pertinence(self, value):
        if self.values[0] <= value < self.values[1]:
            return (value - self.values[0]) / (self.values[1] - self.values[0])
        elif self.values[1] <= value <= self.values[2]:
            return 1.0
        elif self.values[2] < value <= self.values[3]:
            return (self.values[3] - value) / (self.values[3] - self.values[2])
        else:
            return .0

    def _calculate_sinusoidal_pertinence(self, value):
        # return exp(-pow(value - self.values[1], 2.0) / (self.values[0] * pow(2.0, 2.0)))
        return exp(-self.values[0] * pow(value - self.values[1], 2.0))

    def union_pertinence(self, fuzzy_set, value):
        return max(self.calculate_pertinence(value), fuzzy_set.calculate_pertinence(value))

    def intersection_pertinence(self, fuzzy_set, value):
        return min(self.calculate_pertinence(value), fuzzy_set.calculate_pertinence(value))

    def complement_pertinence(self, value):
        1 - self.calculate_pertinence(value)

    def equal(self, fuzzy_set):
        return self.calculate_pertinence(self.values[0]) == fuzzy_set.calculate_pertinence(fuzzy_set.values[0])
