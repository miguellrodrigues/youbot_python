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

    angle_error = normalize_radian(youBot_rotation_angle + theta)

    can_pick = box_position.isInSphere(youBot_position, 0.5716721982903271)

    print(angle_error)

    if angle_error > 0:
        youBot.strafe_right()
    else:
        youBot.strafe_left()


