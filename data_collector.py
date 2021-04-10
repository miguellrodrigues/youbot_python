#  * Copyright (c) 30/03/2021 18:26
#  *
#  * Last modified 30/03/2021 18:26
#  * Miguel L. Rodrigues
#  * All rights reserved

from lib.utils.numbers import normalize
from lib.utils.vector import Vector
from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.youBot import YouBot
from math import sin, cos, pi
import json


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


cont = Controller(64, True)
youBot = YouBot(cont)

data = {
    "errors": [],
    "sig": [],
    "out": []
}

center = youBot.get_position()
initial_position = center

angle = .0
comp = .005

while cont.step() != -1:
    time = cont.get_supervisor().getTime()

    youBot_position = youBot.get_position()

    youBot_rotation_angle = youBot.get_rotation_angle()

    if angle > pi or angle < -pi:
        comp *= -1

    angle += comp

    x = 0.8 * cos(angle)
    z = 0.8 * sin(angle)

    center.add(Vector([x, .0, z]))

    # cont.set_object_position("box", [center.x, center.y, center.z])

    theta = youBot_position.differenceAngle(Vector(cont.get_object_position("box")))

    center.subtract(Vector([x, .0, z]))

    angle_error = normalize(youBot_rotation_angle + theta)

    if angle_error > 0:
        out = .0
        youBot.set_wheels_speed([-1, 1, -1, 1])
    else:
        youBot.set_wheels_speed([1, -1, 1, -1])
        out = 1.0

    data['errors'].append(angle_error)
    data['sig'].append(1.0 if angle_error > 0 else .0)
    data['out'].append(out)


with open("output_dataset.json", "w") as file:
    json.dump(data, file)