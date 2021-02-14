#  * Copyright (c) 10/02/2021 22:04
#  *
#  * Last modified 10/02/2021 21:08
#  * Miguel L. Rodrigues
#  * All rights reserved

from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.enum import Height, Orientation

from math import pi, sqrt, asin, acos, atan


class Arm:
    ARM1 = 0
    ARM2 = 1
    ARM3 = 2
    ARM4 = 3
    ARM5 = 4

    def __init__(self, controller: Controller):
        self.controller = controller
        self.elements = {}

        self.current_height = None
        self.current_orientation = None

        self.init()

    def init(self):
        self.elements[self.ARM1] = self.controller.get_device_by_name("arm1")
        self.elements[self.ARM2] = self.controller.get_device_by_name("arm2")
        self.elements[self.ARM3] = self.controller.get_device_by_name("arm3")
        self.elements[self.ARM4] = self.controller.get_device_by_name("arm4")
        self.elements[self.ARM5] = self.controller.get_device_by_name("arm5")

        self.controller.set_motor_velocity(self.ARM2, 0.5)

        self.set_height(Height.ARM_FRONT_TABLE_BOX)
        self.set_orientation(Orientation.ARM_FRONT)

    def set_arms_position(self, arms, positions):
        for i in range(len(arms)):
            self.elements[arms[i]].setPosition(positions[i])

    def _change(self, positions):
        self.set_arms_position([self.ARM2, self.ARM3, self.ARM4, self.ARM5], positions)

    def reset(self):
        self.set_arms_position([self.ARM1, self.ARM2, self.ARM3, self.ARM4, self.ARM5], [.0, 1.57, -2.635, 1.78, .0])

    def set_height(self, height: Height):
        if height == Height.ARM_FRONT_FLOOR:
            self._change([-.97, -1.55, -.61, .0])
        elif height == Height.ARM_FRONT_PLATE:
            self._change([-.62, -.98, -1.53, .0])
        elif height == Height.ARM_FRONT_CARDBOARD_BOX:
            self._change([.0, -.77, -1.21, .0])
        elif height == Height.ARM_FRONT_TABLE_BOX:
            self._change([-.7, -.35, -1.4, 0.0])
        elif height == Height.ARM_PREPARE_LAUNCH:
            self._change([1.0, .72, .3, .0])
        elif height == Height.ARM_LAUNCH:
            self._change([-.5, -.5, -.3, .0])
        elif height == Height.ARM_RESET:
            self._change([1.57, -2.635, 1.78, .0])
        elif height == Height.ARM_BACK_PLATE_HIGH:
            self._change([.678, .682, 1.74, .0])
        elif height == Height.ARM_BACK_PLATE_LOW:
            self._change([.92, .42, 1.78, .0])
        elif height == Height.ARM_HANOI_PREPARE:
            self._change([-.4, -1.2, -(pi / 2.0), (pi / 2.0)])
        else:
            print("invalid height argument")
            return

        self.current_height = height

    def increase_height(self):
        self.current_height += 1

        if self.current_height >= Height.ARM_MAX_HEIGHT:
            self.current_height = Height.ARM_MAX_HEIGHT - 1

        self.set_height(self.current_height)

    def decrease_height(self):
        self.current_height -= 1

        if self.current_height < 0:
            self.current_height = Height.ARM_FRONT_FLOOR

        self.set_height(self.current_height)

    def set_orientation(self, orientation: Orientation):
        if orientation == Orientation.ARM_BACK_LEFT:
            self.elements[self.ARM1].setPosition(-2.949)
        elif orientation == Orientation.ARM_LEFT:
            self.elements[self.ARM1].setPosition(-(pi / 2.0))
        elif orientation == Orientation.ARM_FRONT_LEFT:
            self.elements[self.ARM1].setPosition(-.2)
        elif orientation == Orientation.ARM_FRONT:
            self.elements[self.ARM1].setPosition(.0)
        elif orientation == Orientation.ARM_FRONT_RIGHT:
            self.elements[self.ARM1].setPosition(.2)
        elif orientation == Orientation.ARM_RIGHT:
            self.elements[self.ARM1].setPosition((pi / 2.0))
        elif orientation == Orientation.ARM_BACK_RIGHT:
            self.elements[self.ARM1].setPosition(2.949)
        else:
            print("invalid orientation argument")
            return

        self.current_orientation = orientation

    def increase_orientation(self):
        self.current_orientation += 1

        if self.current_orientation >= Orientation.ARM_MAX_SIDE:
            self.current_orientation = Orientation.ARM_MAX_SIDE - 1

        self.set_orientation(self.current_orientation)

    def decrease_orientation(self):
        self.current_orientation -= 1

        if self.current_orientation < 0:
            self.current_orientation = Orientation.ARM_BACK_LEFT

        self.set_orientation(self.current_orientation)

    def set_sub_rotation(self, arm, radian):
        self.elements[arm].setPosition(radian)

    def get_sub_length(self, arm):
        if arm == self.ARM1:
            return .253
        elif arm == self.ARM2:
            return .155
        elif arm == self.ARM3:
            return .135
        elif arm == self.ARM4:
            return .081
        elif arm == self.ARM5:
            return .105

        return .0

    def ik(self, x, y, z):
        x1 = sqrt(x * x + z * z)
        y1 = y + self.get_sub_length(self.ARM4) + self.get_sub_length(self.ARM5) - self.get_sub_length(self.ARM1)

        a = self.get_sub_length(self.ARM2)
        b = self.get_sub_length(self.ARM3)
        c = sqrt(x1 * x1 + y1 * y1)

        alpha = -asin(z / x1)
        beta = -((pi / 2.0) - acos((a * a + c * c - b * b) / (2.0 * a * c)) - atan(y1 / x1))
        gamma = -(pi - acos((a * a + b * b - c * c) / (2.0 * a * b)))
        delta = -(pi + (beta + gamma))
        epsilon = (pi / 2.0) + alpha

        self.set_arms_position([self.ARM1, self.ARM2, self.ARM3, self.ARM4, self.ARM5], [alpha, beta, gamma, delta, epsilon])
