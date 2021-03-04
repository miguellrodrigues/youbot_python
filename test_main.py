#  * Copyright (c) 16/02/2021 14:03
#  *
#  * Last modified 16/02/2021 14:03
#  * Miguel L. Rodrigues
#  * All rights reserved

from math import pi, radians

from lib.utils.angle import calculate_angle
from lib.utils.fuzzy_set import FuzzySet, de_fuzzy
from lib.utils.pid import Pid
from lib.utils.vector import normalize_radian, Vector
from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.youBot import YouBot

high_negative_error = FuzzySet(FuzzySet.TRAPEZOIDAL, [-pi, -pi / 2, -pi / 4, radians(-25)])
low_negative_error = FuzzySet(FuzzySet.TRIANGULAR, [radians(-25), radians(-10), radians(-1)])
center_error = FuzzySet(FuzzySet.SINUSOIDAL, [.01, radians(.01)])
low_positive_error = FuzzySet(FuzzySet.TRIANGULAR, [radians(1), radians(10), radians(25)])
high_positive_error = FuzzySet(FuzzySet.TRAPEZOIDAL, [radians(25), pi / 4, pi / 2, pi])

kp_very_low_output = FuzzySet(FuzzySet.TRIANGULAR, [7.4, 11.6, 15.8])
kp_low_output = FuzzySet(FuzzySet.TRIANGULAR, [7.2, 8.6, 11.4])
kp_normal_output = FuzzySet(FuzzySet.TRIANGULAR, [2.0, 7.1, 11.0])
kp_high_output = FuzzySet(FuzzySet.TRIANGULAR, [5.2, 5.6, 9.4])
kp_very_high_output = FuzzySet(FuzzySet.TRIANGULAR, [5.4, 9.6, 14.8])

ki_very_low_error = FuzzySet(FuzzySet.TRIANGULAR, [-1300, -1050, -800])
ki_low_error = FuzzySet(FuzzySet.TRIANGULAR, [-1300, -800, 50])
ki_medium_error = FuzzySet(FuzzySet.TRIANGULAR, [-800, 50, -700])
ki_high_error = FuzzySet(FuzzySet.TRIANGULAR, [50, 700, 1200])


ki_very_low_output = FuzzySet(FuzzySet.TRIANGULAR, [-.001, .005, .001])
ki_low_output = FuzzySet(FuzzySet.TRIANGULAR, [-.004, .008, .004])
ki_medium_output = FuzzySet(FuzzySet.TRIANGULAR, [-.001, .0005, .001])
ki_high_output = FuzzySet(FuzzySet.TRIANGULAR, [-.004, .008, .004])

# if error is low, output is low
# if error is medium output is medium
# if error is high output is high

cont = Controller(14, True)
youBot = YouBot(cont)

radius = .5
ang = 1.57
comp = .001

angle_pid = Pid(.1, 0.05, 1.0, 32.0, .01)

error = .0
old_error = .0

while cont.step() != -1:
    center = youBot.get_position()
    
    youBot_position = youBot.get_position()
    box_position = Vector(cont.get_object_position("box"))

    youBot_rotation = cont.get_object_rotation("youBot")
    box_rotation = cont.get_object_rotation("box")

    angle = calculate_angle(cont, youBot_rotation)

    theta = youBot_position.differenceAngle(box_position)

    angle_error = normalize_radian(angle + theta)

    old_error = error
    error = angle_error

    derived_error = (error + old_error) / .0014

    rules = [
        high_negative_error.calculate_pertinence(angle_error),
        low_negative_error.calculate_pertinence(angle_error),
        center_error.calculate_pertinence(angle_error),
        low_positive_error.calculate_pertinence(angle_error),
        high_positive_error.calculate_pertinence(angle_error)
    ]

    derived_rules = [
        ki_very_low_error.complement_pertinence(derived_error),
        ki_low_error.calculate_pertinence(derived_error),
        ki_medium_error.calculate_pertinence(derived_error),
        ki_high_error.calculate_pertinence(derived_error)
    ]

    kp_output = de_fuzzy([
        kp_very_low_output.values,
        kp_low_output.values,
        kp_normal_output.values,
        kp_high_output.values,
        kp_very_high_output.values
    ], [
        rules[0],
        rules[1],
        rules[2],
        rules[3],
        rules[4]
    ])
    
    ki_output = de_fuzzy([
        ki_very_low_output.values,
        ki_low_output.values,
        ki_medium_output.values,
        ki_high_output.values,
    ], [
        derived_rules[0],
        derived_rules[1],
        derived_rules[2],
        derived_rules[3]
    ])

    angle_pid.update_weights([kp_output, ki_output, .2])

    out = angle_pid.compute(angle_error, .0014)

    youBot.set_wheels_speed([-out, out, -out, out])

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



