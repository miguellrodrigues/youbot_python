#  * Copyright (c) 10/03/2021 21:41
#  *
#  * Last modified 10/03/2021 21:41
#  * Miguel L. Rodrigues
#  * All rights reserved

from lib.network.network import load_network
from lib.utils.vector import Vector
from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.youBot import YouBot
from math import atan2, sin, cos
import matplotlib.pyplot as plt


def normalize(value: float) -> float:
    return atan2(sin(value), cos(value))


cont = Controller(14, True)
youBot = YouBot(cont)

network = load_network("net.json")

max_velocity = 10

while cont.step() != -1:
    time = cont.get_supervisor().getTime()

    youBot_position = youBot.get_position()

    youBot_rotation_angle = youBot.get_rotation_angle()
    angle_error = normalize(youBot_rotation_angle + youBot_position.differenceAngle(Vector(cont.get_object_position("box"))))

    print(angle_error)

    output = network.predict([angle_error])

    speed = output.get_value(0, 0) * max_velocity

    youBot.set_wheels_speed([speed, -speed, speed, -speed])

