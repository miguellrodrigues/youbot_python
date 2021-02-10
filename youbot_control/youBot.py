from wbc_controller.wbc_controller import Controller

from youbot_control.arm import Arm
from youbot_control.gripper import Gripper
from youbot_control.base import Base


class YouBot:
    def __init__(self, controller: Controller):
        self.controller = controller

        self.arm = Arm(controller)
        self.gripper = Gripper(controller)
        self.base = Base(controller)
