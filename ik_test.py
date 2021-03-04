#  * Copyright (c) 04/03/2021 14:50
#  *
#  * Last modified 04/03/2021 14:50
#  * Miguel L. Rodrigues
#  * All rights reserved

from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.youBot import YouBot
from math import *

cont = Controller(14, True)
youBot = YouBot(cont)


upper_length = .216
lower_length = .155

hyp = sqrt(lower_length ** 2 + upper_length ** 2)

z = 0.01
x = 0.09


while cont.step() != -1:
    time = cont.get_supervisor().getTime()

    theta = atan2(z, x)

    z2 = x / cos(theta)

    cos_a = (pow(upper_length, 2.0) + pow(z2, 2.0) - pow(lower_length, 2.0)) / (2 * upper_length * z2)
    cos_b = (pow(z2, 2.0) + pow(lower_length, 2.0) - pow(upper_length, 2.0)) / (2 * lower_length * z2)

    angle_a = acos(cos_a)
    angle_b = acos(cos_b)

    elbow_angle = (pi - (angle_a + angle_b))

    youBot.set_heights([1, 2, 3], [-angle_a, radians(-90) + elbow_angle, radians(0)])
