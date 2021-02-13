#  * Copyright (c) 12/02/2021 11:48
#  *
#  * Last modified 12/02/2021 11:48
#  * Miguel L. Rodrigues
#  * All rights reserved

from lib.utils.vector import Vector, normalize_radian
from lib.webots_lib.wbc_controller import Controller

from lib.youbot_control.youBot import YouBot

cont = Controller(14, True)
youBot = YouBot(cont)

while cont.step() != -1:
    youBot_position = youBot.get_position()
    youBot_rotation_angle = normalize_radian(youBot.get_rotation_angle())

    box_position = Vector(cont.get_object_position("box"))

    theta = youBot_position.differenceAngle(box_position)

    angle_error = normalize_radian(theta - youBot_rotation_angle)


