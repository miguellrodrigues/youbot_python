#  * Copyright (c) 04/03/2021 14:50
#  *
#  * Last modified 04/03/2021 14:50
#  * Miguel L. Rodrigues
#  * All rights reserved

from lib.utils.pid import Pid
from lib.utils.vector import Vector
from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.youBot import YouBot
from math import *

cont = Controller(14, True)
youBot = YouBot(cont)

upper_length = .155
lower_length = .216

hyp = sqrt(lower_length ** 2 + upper_length ** 2)

print(hyp)

# base x = -1.15326
# base y = 0.21498
# base z = 0.0988456

# ybx = -1.20686
# yby = 0.101928
# ybz = 0.08605

# x = -1.15326 - (-1.20686)
# y = 0.21498 - 0.101928
# z = 0.0988456 - 0.08605

# d = 0.5906511712734462

distance_pid = Pid(2.0, .005, 1.0, 8.0, .5)

while cont.step() != -1:
    youBot_position = youBot.get_position()
    box_position = Vector(cont.get_object_position("box"))

    base_position = youBot_position.clone().add(Vector([0.05360000000000009, 0.113052, 0.012795600000000004]))

    youBot.set_wheels_speed([.0, .0, .0, .0])

    z = .125
    x = box_position.y - .25

    theta = atan2(z, x)

    # z2 = x / cos(theta)
    z2 = .26585898517823314
    x1 = sqrt(x ** 2 + z ** 2)

    alpha = -asin(z / x1)

    cos_a = (pow(upper_length, 2.0) + pow(z2, 2.0) - pow(lower_length, 2.0)) / (2 * upper_length * z2)
    cos_b = (pow(z2, 2.0) + pow(lower_length, 2.0) - pow(upper_length, 2.0)) / (2 * lower_length * z2)

    angle_a = acos(cos_a)
    angle_b = acos(cos_b)

    elbow_angle = -pi + (angle_a + angle_b)

    youBot._arm.ik(0.1, 0.1, 0.0)

    # youBot.set_heights([1, 2, 3], [-angle_a, -1.57 - elbow_angle, -(pi / 2.0) - alpha])

