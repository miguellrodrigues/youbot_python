#  * Copyright (c) 16/02/2021 10:36
#  *
#  * Last modified 16/02/2021 10:36
#  * Miguel L. Rodrigues
#  * All rights reserved
from lib.utils.numbers import random_double


def array_to_matrix(array):
    matrix = Matrix(len(array), 1)

    for i in range(len(array)):
        matrix.set_value(i, 0, array[i])

    return matrix


def list_to_matrix(lst, rows, cols):
    matrix = Matrix(rows, cols)

    count = 0

    for i in range(rows):
        for j in range(cols):
            matrix.set_value(i, j, lst[count])
            count += 1

    return matrix


class Matrix:
    def __init__(self, rows, cols, is_random=False):
        self.rows = rows
        self.cols = cols

        self.data = [[0.0] * cols for _i in range(rows)]

        if is_random:
            for i in range(rows):
                for j in range(cols):
                    self.data[i][j] = random_double(-.501, .501)
        else:
            for i in range(rows):
                for j in range(cols):
                    self.data[i][j] = .0

    def set_value(self, row, column, value):
        self.data[row][column] = value

    def get_value(self, row, column):
        return self.data[row][column]

    def map(self, function):
        for i in range(self.rows):
            for j in range(self.cols):
                self.set_value(i, j, function(self.data[i][j]))

    def transpose(self):
        matrix = Matrix(self.cols, self.rows)

        for i in range(self.rows):
            for j in range(self.cols):
                matrix.set_value(j, i, self.get_value(i, j))

        return matrix

    def hadamard(self, mx):
        matrix = Matrix(mx.rows, mx.cols)

        for i in range(mx.rows):
            for j in range(mx.cols):
                matrix.set_value(i, j, self.get_value(i, j) * mx.get_value(i, j))

        return matrix

    def multiply(self, mx):
        matrix = Matrix(self.rows, mx.cols)

        for i in range(self.rows):
            for j in range(mx.cols):
                aux = .0

                for k in range(mx.rows):
                    aux += self.get_value(i, k) * mx.get_value(k, j)

                matrix.set_value(i, j, aux)

        return matrix

    def add(self, mx):
        matrix = Matrix(self.rows, self.cols)

        for i in range(self.rows):
            for j in range(self.cols):
                matrix.set_value(i, j, self.get_value(i, j) + mx.get_value(i, j))

        return matrix

    def subtract(self, mx):
        matrix = Matrix(self.rows, self.cols)

        for i in range(self.rows):
            for j in range(self.cols):
                matrix.set_value(i, j, self.get_value(i, j) - mx.get_value(i, j))

        return matrix

    def scalar(self, value):
        for i in range(self.rows):
            for j in range(self.cols):
                self.set_value(i, j, self.get_value(i, j) * value)

    def divide(self, value):
        for i in range(self.rows):
            for j in range(self.cols):
                self.set_value(i, j, self.get_value(i, j) / value)

    def matrix_to_array(self):
        array = []

        for i in range(self.rows):
            array[i] = self.get_value(i, 0)

        return array

    def assign_matrix(self, matrix_array):
        rows = len(matrix_array)
        cols = len(matrix_array[0])

        if rows != self.rows or cols != self.cols:
            print('bad argument')
            return

        for i in range(rows):
            for j in range(cols):
                self.set_value(i, j, matrix_array[i][j])

    def print(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(str(self.get_value(i, j)) + ' ', end='')

                if j == self.cols - 1:
                    print('')

    def copy(self, matrix):
        for i in range(matrix.rows):
            for j in range(matrix.cols):
                self.set_value(i, j, matrix.get_value(i, j))

    def to_list(self):
        values = []

        for i in range(self.rows):
            for j in range(self.cols):
                values.append(self.get_value(i, j))

        return values

    def assign_array(self, lst):
        count = 0

        for i in range(self.rows):
            for j in range(self.cols):
                self.set_value(i, j, lst[count])
                count += 1
