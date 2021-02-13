#  * Copyright (c) 12/02/2021 11:45
#  *
#  * Last modified 12/02/2021 11:45
#  * Miguel L. Rodrigues
#  * All rights reserved

from math import atan2, sin, cos, hypot, sqrt, acos


def normalize_radian(radian):
    return atan2(sin(radian), cos(radian))


class Vector:
    def __init__(self, args):
        self.x = float(args[0])
        self.y = float(args[1])
        self.z = float(args[2])

    def __str__(self):
        return str(self.x) + ":" + str(self.y) + ":" + str(self.z)

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z

        return self

    def subtract(self, vector):
        self.x -= vector.x
        self.y -= vector.y
        self.z -= vector.z

        return self

    def multiply(self, vector):
        self.x *= vector.x
        self.y *= vector.y
        self.z *= vector.z

        return self

    def divide(self, vector):
        self.x /= vector.x
        self.y /= vector.y
        self.z /= vector.z

        return self

    def length(self):
        return sqrt(self.lengthSquared())

    def lengthSquared(self):
        return (self.x ** 2) + (self.y ** 2) + (self.z ** 2)

    def distance(self, vector):
        return hypot(self.x - vector.x, self.z - vector.z)

    def distanceSquared(self, vector):
        return self.distance(vector) ** 2

    def angle(self, other):
        dot = self.dot(other) / (self.length() * other.length())
        return acos(dot)

    def differenceAngle(self, other):
        return atan2(other.z - self.z, other.x - self.x)

    def midPoint(self, other):
        self.x = (self.x + other.x) / 2.0
        self.y = (self.y + other.y) / 2.0
        self.z = (self.z + other.z) / 2.0

        return self

    def getMidPoint(self, other):
        x = (self.x + other.x) / 2.0
        y = (self.y + other.y) / 2.0
        z = (self.z + other.z) / 2.0

        return Vector([x, y, z])

    def scalar(self, number):
        self.x *= number
        self.y *= number
        self.z *= number

        return self

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def crossProduct(self, other):
        x = self.y * other.z - other.y * self.z
        y = self.z * other.x - other.z * self.x
        z = self.x * other.y - other.x * self.y

        self.x = x
        self.y = y
        self.z = z

        return self

    def getCrossProduct(self, other):
        x = self.y * other.z - other.y * self.z
        y = self.z * other.x - other.z * self.x
        z = self.x * other.y - other.x * self.y

        return Vector([x, y, z])

    def normalize(self):
        length = self.length()

        self.x /= length
        self.y /= length
        self.z /= length

        return self

    def zero(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        return self

    def isInAABB(self, minimum, maximum):
        return self.x >= minimum.x & self.x <= maximum.x & self.y >= minimum.y & self.y <= maximum.y & self.z >= minimum.z & self.z <= maximum.z

    def isInSphere(self, origin, radius):
        return (origin.x - self.x) ** 2 + (origin.y - self.y) ** 2 + (origin.z - self.z) ** 2 <= radius ** 2

    def setX(self, x):
        self.x = x
        return self

    def setY(self, y):
        self.y = y
        return self

    def setZ(self, z):
        self.z = z
        return self

    def clone(self):
        return Vector([self.x, self.y, self.z])
