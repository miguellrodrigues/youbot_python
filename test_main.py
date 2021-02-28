#  * Copyright (c) 16/02/2021 14:03
#  *
#  * Last modified 16/02/2021 14:03
#  * Miguel L. Rodrigues
#  * All rights reserved

from math import degrees, cos, sin

from lib.network.network import Network
from lib.utils.angle import calculate_angle
from lib.utils.fuzzy_set import FuzzySet, de_fuzzy
from lib.utils.pid import Pid
from lib.utils.vector import normalize_radian, Vector
from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.youBot import YouBot

negative_error = FuzzySet(FuzzySet.TRAPEZOIDAL, [-180, -90, -5, -.0001])
center_error = FuzzySet(FuzzySet.TRIANGULAR, [-10, 0, 10])
positive_error = FuzzySet(FuzzySet.TRAPEZOIDAL, [.0001, 5, 90, 180])

low_output = FuzzySet(FuzzySet.TRIANGULAR, [-15, -30, -5])
medium_output = FuzzySet(FuzzySet.TRIANGULAR, [-30, .0001, 30])
high_output = FuzzySet(FuzzySet.TRIANGULAR, [5, 30, 15])

# if error is low, output is low
# if error is medium output is medium
# if error is high output is high

cont = Controller(14, True)
youBot = YouBot(cont)

angle_pid = Pid(8.0, 0.07, 2.0, 5.0, 1.0)

network = Network([1, 16, 32, 1])

radius = .5
ang = 1.57
comp = .01

center = youBot.get_position()

while cont.step() != -1:
    time = cont.get_supervisor().getTime()

    youBot_position = youBot.get_position()
    box_position = Vector(cont.get_object_position("box"))

    youBot_rotation = cont.get_object_rotation("youBot")
    box_rotation = cont.get_object_rotation("box")

    angle = calculate_angle(youBot_rotation)

    theta = youBot_position.differenceAngle(box_position)

    angle_error = normalize_radian(angle + theta)

    rules = [
        negative_error.calculate_pertinence(degrees(angle_error)),
        center_error.calculate_pertinence(degrees(angle_error)),
        positive_error.calculate_pertinence(degrees(angle_error))
    ]

    output = de_fuzzy([low_output.values, medium_output.values, high_output.values], [rules[0], rules[1], rules[2]])

    youBot.set_wheels_speed([-output, output, -output, output])

    # print("Output -> {} | Error -> {}".format(output, degrees(angle_error)))

    ang += comp

    if ang > 3.14:
        comp = -.01
    elif ang < -3.14:
        comp = 0.01

    center.add(Vector([cos(ang), .0, sin(ang)]))

    cont.set_object_position("box", [center.x, center.y, center.z])

    center.subtract(Vector([cos(ang), .0, sin(ang)]))


