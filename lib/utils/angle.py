#  * Copyright (c) 16/02/2021 13:32
#  *
#  * Last modified 16/02/2021 13:32
#  * Miguel L. Rodrigues
#  * All rights reserved

from math import radians, sin, cos, atan2

from lib.utils.matrix import Matrix

phi = radians(-90)

r_x = Matrix(3, 3)

r_x.assign_matrix([
    [1, 0, 0],
    [0, cos(phi), -sin(phi)],
    [0, sin(phi), cos(phi)]
])


def calculate_matrix_r(data):
    matrix_r = Matrix(3, 3)

    cos_theta = cos(data[3])
    sin_theta = sin(data[3])

    matrix_r.assign_matrix([
        [(pow(data[0], 2) * (1 - cos_theta) + cos_theta),
         ((data[0] * data[1]) * (1 - cos_theta) - (data[2] * sin_theta)),
         ((data[0] * data[2]) * (1 - cos_theta) + (data[1] * sin_theta))],
        [((data[0] * data[1]) * (1 - cos_theta) + (data[2] * sin_theta)),
         (pow(data[1], 2) * (1 - cos_theta) + cos_theta),
         ((data[1] * data[2]) * (1 - cos_theta) - (data[0] * sin_theta))],
        [((data[0] * data[2]) * (1 - cos_theta) - (data[1] * sin_theta)),
         ((data[1] * data[2]) * (1 - cos_theta) + (data[0] * sin_theta)),
         (pow(data[2], 2) * (1 - cos_theta) + cos_theta)]
    ])

    return matrix_r


def calculate_angle(process_variable):
    matrix_r = calculate_matrix_r(process_variable)

    result = r_x.transpose().multiply(matrix_r)

    angle = atan2(result.get_value(1, 0), result.get_value(0, 0))

    return angle
