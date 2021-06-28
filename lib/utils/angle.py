#  * Copyright (c) 16/02/2021 13:32
#  *
#  * Last modified 16/02/2021 13:32
#  * Miguel L. Rodrigues
#  * All rights reserved

from math import radians, sin, cos, atan2
from lib.linalg.matrix import Matrix
from typing import List

phi = radians(-90)

r_x = Matrix(3, 3)

r_x.assign_matrix([
    [1, 0, 0],
    [0, cos(phi), -sin(phi)],
    [0, sin(phi), cos(phi)]
])

r_x = r_x.transpose()


def calculate_matrix_r(data: List[float]) -> Matrix:
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


def calculate_angle(rotation_matrix: Matrix) -> float:
    # matrix_r = calculate_matrix_r(process_variable)

    # matrix_r = Matrix(3, 3)
    #
    # o = controller.get_object_orientation("youBot")
    #
    # d = [[o[0] ,o[1], o[2]],
    #      [o[3], o[4], o[5]],
    #      [o[6], o[7], o[8]]]
    #
    # matrix_r.assign_matrix(d)

    result = r_x.multiply(rotation_matrix)

    angle = atan2(result.get_value(1, 0), result.get_value(0, 0))

    return angle
