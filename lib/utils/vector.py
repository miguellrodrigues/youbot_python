#  * Copyright (c) 12/02/2021 11:45
#  *
#  * Last modified 12/02/2021 11:45
#  * Miguel L. Rodrigues
#  * All rights reserved

from math import pi, atan2, sin, cos


def normalize_radian(radian):
    return atan2(sin(radian), cos(radian))


class Vector:
    def __init__(self, args):
        self.x = args[0]
        self.y = args[1]
        self.z = args[2]

    def distance(self, vector):
        return hypot(self.x - vector.x, self.z - vector.z)

    def angle(self, vector):
        return atan2(vector.z - self.z, vector.x - self.x)

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z

    def subtract(self, vector):
        self.x -= vector.x
        self.y -= vector.y
        self.z -= vector.z

    def multiply(self, vector):
        self.x *= vector.x
        self.y *= vector.y
        self.z *= vector.z

    def scalar(self, x):
        self.x *= x
        self.y *= x
        self.z *= x

    def clone(self):
        return Vector([self.x, self.y, self.z])
