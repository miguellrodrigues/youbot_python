#  * Copyright (c) 10/02/2021 22:04
#  *
#  * Last modified 10/02/2021 20:21
#  * Miguel L. Rodrigues
#  * All rights reserved

from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.tiny_math import bound


class Gripper:
    LEFT = 0
    RIGHT = 1

    MIN_POS = .0
    MAX_POS = .025

    OFFSET_WHEN_LOCKED = .021

    def __init__(self, controller: Controller):
        self.fingers = {}
        self.controller = controller

        self.init()

    def init(self):
        self.fingers[self.LEFT] = self.controller.get_device_by_name("finger1")
        self.fingers[self.RIGHT] = self.controller.get_device_by_name("finger2")

        self.fingers[self.LEFT].setVelocity(0.03)
        self.fingers[self.RIGHT].setVelocity(0.03)

    def grip(self):
        self.fingers[self.LEFT].setPosition(self.MIN_POS)
        self.fingers[self.RIGHT].setPosition(self.MIN_POS)

    def release(self):
        self.fingers[self.LEFT].setPosition(self.MAX_POS)
        self.fingers[self.RIGHT].setPosition(self.MAX_POS)

    def set_gap(self, gap: float):
        v = bound(0.5 * (gap - self.OFFSET_WHEN_LOCKED), self.MIN_POS, self.MAX_POS)

        self.fingers[self.LEFT].setPosition(v)
        self.fingers[self.RIGHT].setPosition(v)
