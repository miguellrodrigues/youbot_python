#  * Copyright (c) 16/02/2021 14:03
#  *
#  * Last modified 16/02/2021 14:03
#  * Miguel L. Rodrigues
#  * All rights reserved

# from math import degrees, cos, sin
from math import degrees, pi, radians, cos, sin

from lib.utils.angle import calculate_angle
from lib.utils.fuzzy_set import FuzzySet, de_fuzzy
from lib.utils.pid import Pid
from lib.utils.vector import normalize_radian, Vector
from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.youBot import YouBot

kp_high_negative_error = FuzzySet(FuzzySet.TRAPEZOIDAL, [-pi, -pi / 2, -pi / 4, radians(-25)])
kp_low_negative_error = FuzzySet(FuzzySet.TRIANGULAR, [radians(-25), radians(-10), radians(-1)])
kp_center_error = FuzzySet(FuzzySet.SINUSOIDAL, [.01, radians(.01)])
kp_low_positive_error = FuzzySet(FuzzySet.TRIANGULAR, [radians(1), radians(10), radians(25)])
kp_high_positive_error = FuzzySet(FuzzySet.TRAPEZOIDAL, [radians(25), pi / 4, pi / 2, pi])

kp_very_low_output = FuzzySet(FuzzySet.TRIANGULAR, [4.4, 12.8, 8.6])
kp_low_output = FuzzySet(FuzzySet.TRIANGULAR, [4.2, 8.4, 4.6])
kp_normal_output = FuzzySet(FuzzySet.TRIANGULAR, [1.2, 6.1, 1.2])
kp_high_output = FuzzySet(FuzzySet.TRIANGULAR, [4.2, 8.4, 4.6])
kp_very_high_output = FuzzySet(FuzzySet.TRIANGULAR, [4.4, 12.8, 8.6])

# if error is low, output is low
# if error is medium output is medium
# if error is high output is high

cont = Controller(14, True)
youBot = YouBot(cont)

radius = .5
ang = 1.57
comp = .01

center = youBot.get_position()

angle_pid = Pid(.1, 0.05, 1.0, 16.0, .001)

error = .0
old_error = .0

while cont.step() != -1:
    youBot_position = youBot.get_position()
    box_position = Vector(cont.get_object_position("box"))

    youBot_rotation = cont.get_object_rotation("youBot")
    box_rotation = cont.get_object_rotation("box")

    angle = calculate_angle(youBot_rotation)

    theta = youBot_position.differenceAngle(box_position)

    angle_error = normalize_radian(angle + theta)

    kp_rules = [
        kp_high_negative_error.calculate_pertinence(angle_error),
        kp_low_negative_error.calculate_pertinence(angle_error),
        kp_center_error.calculate_pertinence(angle_error),
        kp_low_positive_error.calculate_pertinence(angle_error),
        kp_high_positive_error.calculate_pertinence(angle_error)
    ]

    kp_output = de_fuzzy([
        kp_very_low_output.values,
        kp_low_output.values,
        kp_normal_output.values,
        kp_high_output.values,
        kp_very_high_output.values
    ], [
        kp_rules[0],
        kp_rules[1],
        kp_rules[2],
        kp_rules[3],
        kp_rules[4],
    ])

    angle_pid.update_weights([kp_output, .001, .2])

    out = angle_pid.compute(angle_error, .05)

    youBot.set_wheels_speed([-out, out, -out, out])

    print("Output -> {} | Error -> {}".format(kp_output, (angle_error)))

    # ang += comp
    #
    # if ang > 3.14:
    #     comp = -.001
    # elif ang < -3.14:
    #     comp = .001
    #
    # center.add(Vector([cos(ang), .0, sin(ang)]))
    #
    # cont.set_object_position("box", [center.x, center.y, center.z])
    #
    # center.subtract(Vector([cos(ang), .0, sin(ang)]))
