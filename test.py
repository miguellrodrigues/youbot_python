#  * Copyright (c) 16/02/2021 10:55
#  *
#  * Last modified 16/02/2021 10:55
#  * Miguel L. Rodrigues
#  * All rights reserved

from math import *

from lib.utils.matrix import Matrix

test_matrix = Matrix(3, 3)

nx = -.935114
ny = .250563
nz = .250561

theta = 1.63784

# cos_alpha = nx / sqrt(pow(nx, 2) + pow(ny, 2))
# sin_alpha = ny / sqrt(pow(nx, 2) + pow(ny, 2))
#
# cos_beta = nz
# sin_beta = sqrt(pow(nx, 2) + pow(ny, 2))
#
#
# r_x = [
#     [1, 0, 0],
#     [0, cos(.0), -sin(.0)],
#     [0, sin(.0), cos(.0)]
# ]
#
# r_y = [
#        [cos(.0), 0, sin(.0)],
#        [0, 1, 0],
#        [-sin(.0), 0, cos(.0)]
# ]
#
# r_z = [
#     [cos(.0), -sin(.0), 0],
#     [sin(.0), cos(.0), 0],
#     [0, 0, 1]
# ]

cos_theta = cos(theta)
sin_theta = sin(theta)

r_n = [
    [(pow(nx, 2) * (1 - cos_theta) + cos_theta), ((nx * ny) * (1 - cos_theta) - (nz * sin_theta)), ((nx * nz) * (1 - cos_theta) + (ny * sin_theta))],
    [((nx * ny) * (1 - cos_theta) + (nz * sin_theta)), (pow(ny, 2) * (1 - cos_theta) + cos_theta), ((ny * nz) * (1 - cos_theta) - (nx * sin_theta))],
    [((nx * nz) * (1 - cos_theta) - (ny * sin_theta)), ((ny * nz) * (1 - cos_theta) + (nx * sin_theta)), (pow(nz, 2) * (1 - cos_theta) + cos_theta)]
]

test_matrix.assign(r_n)

test_matrix.print()
