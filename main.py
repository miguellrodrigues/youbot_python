#  * Copyright (c) 12/02/2021 11:48
#  *
#  * Last modified 12/02/2021 11:48
#  * Miguel L. Rodrigues
#  * All rights reserved

from lib.utils.vector import Vector, normalize_radian
from lib.webots_lib.wbc_controller import Controller

from lib.youbot_control.youBot import YouBot
from math import pi

cont = Controller(14, True)
youBot = YouBot(cont)

while cont.step() != -1:
    youBot_position = youBot.get_position()
    youBot_rotation_angle = youBot.get_rotation_angle()

    box_position = Vector(cont.get_object_position('box'))

    theta = youBot_position.angle(box_position)

    angle_error = normalize_radian((youBot_rotation_angle - theta + (pi / 2.0)))

    if angle_error > 0:
        youBot.strafe_left()
    elif angle_error < 0:
        youBot.strafe_right()
    else:
        youBot.base_reset()

