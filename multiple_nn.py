#  * Copyright (c) 09/03/2021 14:45
#  *
#  * Last modified 09/03/2021 14:45
#  * Miguel L. Rodrigues
#  * All rights reserved

from lib.network.network import Network, load_network
from lib.utils.pid import Pid
from lib.utils.vector import Vector
from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.youBot import YouBot
from math import atan2, sin, cos


def normalize(value: float) -> float:
    return atan2(sin(value), cos(value))


cont = Controller(14, True)
youBot = YouBot(cont)

# align_network = Network([1, 8, 8, 1])

align_network = load_network("align_network.json")

angle_pid = Pid(8.0, 0.05, 6.0, 10.0, .3)

max_velocity = 6

while cont.step() != -1:
    youBot_position = youBot.get_position()
    box_position = Vector(cont.get_object_position("box"))

    youBot_rotation_angle = youBot.get_rotation_angle()

    distance = youBot_position.distance(box_position)
    theta = youBot_position.differenceAngle(box_position)

    angle_error = normalize(youBot_rotation_angle + theta)

    output = align_network.predict([angle_error])

    if angle_error > .01 or angle_error < -.01:
        speed = output.get_value(0, 0) * max_velocity

        youBot.set_wheels_speed([-speed, speed, -speed, speed])
    else:
        youBot.set_wheels_speed([.0, .0, .0, .0])

    # angle_out = angle_pid.compute(angle_error, 14/1000)
    #
    # youBot.set_wheels_speed([-angle_out, angle_out, -angle_out, angle_out])
    #
    # align_network.train([angle_error], [angle_out])

align_network.save("align_network.json")
