from wbc_controller.wbc_controller import Controller
from tiny_math import bound

class Gripper:
    LEFT = 0
    RIGHT = 1

    MIN_POS = .0
    MAX_POS = .025

    OFFSET_WHEN_LOCKED = .021

    def __init__(self, controller: Controller):
        self.fingers = {}
        self.controller = controller

        self.gripper_init()

    def gripper_init(self):
        self.fingers[self.LEFT] = self.controller.get_device_by_name("finger1")
        self.fingers[self.RIGHT] = self.controller.get_device_by_name("finger2")

        self.fingers[self.LEFT].setVelocity(.03)
        self.fingers[self.RIGHT].setVelocity(.03)

    def grip(self):
        self.fingers[self.LEFT].setVelocity(self.MIN_POS)
        self.fingers[self.RIGHT].setVelocity(self.MIN_POS)

    def release(self):
        self.fingers[self.LEFT].setVelocity(self.MAX_POS)
        self.fingers[self.RIGHT].setVelocity(self.MAX_POS)

    def set_gap(self, gap):
        v = bound(0.5 * (gap - self.OFFSET_WHEN_LOCKED), self.MIN_POS, self.MAX_POS)
        self.fingers[self.LEFT].setVelocity(v)
        self.fingers[self.RIGHT].setVelocity(v)