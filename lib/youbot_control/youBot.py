#  * Copyright (c) 10/02/2021 22:04
#  *
#  * Last modified 10/02/2021 20:14
#  * Miguel L. Rodrigues
#  * All rights reserved
from lib.utils.angle import calculate_angle
from lib.utils.matrix import Matrix
from lib.utils.vector import Vector, normalize_radian
from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.arm import Arm
from lib.youbot_control.base import Base
from lib.youbot_control.enum import Height
from lib.youbot_control.gripper import Gripper


class YouBot:
    def __init__(self, controller: Controller):
        self.controller = controller

        self._arm = Arm(controller)
        self._gripper = Gripper(controller)
        self._base = Base(controller)

        self.node_def = self.controller.get_supervisor().getName()

        self.rotation_matrix = Matrix(3, 3, False)

    def passive_wait(self, seconds):
        start_time = self.controller.get_supervisor().getTime()

        while start_time + seconds > self.controller.get_supervisor().getTime():
            self.controller.step()

    def get_rotation_angle(self):
        self.rotation_matrix.assign_array(self.controller.get_object_orientation(self.node_def))

        return calculate_angle(self.rotation_matrix)

    def get_position(self):
        return Vector(self.controller.get_object_position(self.node_def))

    def get_height(self):
        return self._arm.current_height

    def get_orientation(self):
        return self._arm.current_orientation

    def arm_reset(self):
        self._arm.reset()

    def set_arm_height(self, height):
        self._arm.set_height(height)

    def set_arm_height_and_gripper_orientation(self, height, gripper_orientation):
        self._arm.set_height(height)
        self.set_gripper_orientation(gripper_orientation)

    def increase_arm_height(self):
        self._arm.increase_height()

    def decrease_arm_height(self):
        self._arm.decrease_height()

    def set_arm_orientation(self, orientation):
        self._arm.set_orientation(orientation)

    def increase_arm_orientation(self):
        self._arm.increase_orientation()

    def decrease_arm_orientation(self):
        self._arm.decrease_orientation()

    def grip(self):
        self._gripper.grip()

    def grip_release(self):
        self._gripper.release()

    def set_wheels_speed(self, speed):
        self._base.set_wheels_speed(speed)

    def forwards(self):
        self._base.forwards()

    def backwards(self):
        self._base.backwards()

    def turn_left(self):
        self._base.turn_left()

    def turn_right(self):
        self._base.turn_right()

    def strafe_left(self):
        self._base.strafe_left()

    def strafe_right(self):
        self._base.strafe_right()

    def base_reset(self):
        self._base.reset()

    def set_gripper_orientation(self, value):
        self._arm.set_sub_rotation(self._arm.ARM5, value)

    def set_height(self, arm, value):
        self._arm.set_arms_position([arm], [value])

    def set_heights(self, arms, values):
        self._arm.set_arms_position(arms, values)

    def throw(self):
        self.set_arm_height(Height.ARM_LAUNCH)

        self.passive_wait(.58)
        self.grip_release()
        self.passive_wait(.2)

        self.arm_reset()
        self.passive_wait(2.0)
        self.grip()

    def pickup(self, r):
        self.grip_release()
        self.passive_wait(1.0)
        self.set_arm_height_and_gripper_orientation(Height.ARM_FRONT_TABLE_BOX, r)
        self.passive_wait(2.2)
        self.grip()
        self.passive_wait(.4)
        self.set_arm_height(Height.ARM_PREPARE_LAUNCH)
        self.passive_wait(1.2)

    def getOrientation(self):
        return self.controller.get_object_orientation(self.node_def)

