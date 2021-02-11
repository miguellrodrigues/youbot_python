#  * Copyright (c) 10/02/2021 22:04
#  *
#  * Last modified 10/02/2021 20:11
#  * Miguel L. Rodrigues
#  * All rights reserved

from webots_lib.wbc_controller import Controller


class Base:
    SPEED = 4.0
    # DISTANCE_TOLERANCE = .001
    # ANGLE_TOLERANCE = .001

    # K1 = 3.0
    # K2 = 1.0
    # K3 = 1.0

    def __init__(self, controller: Controller):
        self.controller = controller

        self.wheels = []
        # self.gps = None
        # self.compass = None

        self.init()

    def init(self):
        for i in range(4):
            self.wheels.append(self.controller.get_device_by_name("wheel{}".format(i + 1)))

    def set_wheel_speed(self, index, speed):
        self.wheels[index].setPosition(float('inf'))
        self.wheels[index].setVelocity(speed)

    def set_wheels_speed(self, speed):
        for i in range(len(self.wheels)):
            self.set_wheel_speed(i, speed[i])

    def reset(self):
        self.set_wheels_speed([.0, .0, .0, .0])

    def forwards(self):
        self.set_wheels_speed([self.SPEED, self.SPEED, self.SPEED, self.SPEED])

    def backwards(self):
        self.set_wheels_speed([-self.SPEED, -self.SPEED, -self.SPEED, -self.SPEED])

    def turn_left(self):
        self.set_wheels_speed([-self.SPEED, self.SPEED, -self.SPEED, self.SPEED])

    def turn_right(self):
        self.set_wheels_speed([self.SPEED, -self.SPEED, self.SPEED, -self.SPEED])

    def strafe_left(self):
        self.set_wheels_speed([self.SPEED, -self.SPEED, -self.SPEED, self.SPEED])

    def strafe_right(self):
        self.set_wheels_speed([-self.SPEED, self.SPEED, self.SPEED, -self.SPEED])
