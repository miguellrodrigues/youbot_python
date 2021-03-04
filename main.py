#  * Copyright (c) 12/02/2021 11:48
#  *
#  * Last modified 12/02/2021 11:48
#  * Miguel L. Rodrigues
#  * All rights reserved

from math import radians, pi, sqrt, asin
from random import uniform

from lib.utils.angle import calculate_angle
from lib.utils.pid import Pid
from lib.utils.vector import Vector, normalize_radian
from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.enum import Height
from lib.youbot_control.youBot import YouBot

cont = Controller(14, True)
youBot = YouBot(cont)

angle_pid = Pid(8.0, 0.05, 6.0, 10.0, .3)
distance_pid = Pid(5.0, .01, 2.0, 5.0, .01)

start_time = .0
end_time = .0

state = 'align'

angle_tolerance = radians(.8)

minimum_distance = 0.5441111029669102

distance_tolerance = 0.0025

can_throw = False


def in_tolerance(value, tolerance):
    return -tolerance < value < tolerance


while cont.step() != -1:
    start_time = cont.get_supervisor().getTime()

    youBot_position = youBot.get_position()
    youBot_rotation_angle = calculate_angle(youBot.getOrientation())

    box_position = Vector(cont.get_object_position("box"))

    angle_error = (youBot_rotation_angle + youBot_position.differenceAngle(box_position))

    distance_error = (box_position.distance(youBot_position) - minimum_distance)

    youBot.set_wheels_speed([.0, .0, .0, .0])

    if state == 'align' and (in_tolerance(distance_error, distance_tolerance)) and (in_tolerance(angle_error, angle_tolerance)):
        state = 'align_base'

        angle_pid.update_weights([4.0, 0.005, 2.0])
    elif state == 'pick' and can_throw:
        state = 'throw'
    elif state == 'throw' and not can_throw:
        state = 'align'

    if state == 'align':
        angle_out = angle_pid.compute(angle_error, start_time - end_time)
        distance_out = distance_pid.compute(distance_error, start_time - end_time)

        out_plus = angle_out + distance_out
        out_minus = angle_out - distance_out

        youBot.set_wheels_speed([-out_minus, out_plus, out_minus, -out_plus])

        end_time = cont.get_supervisor().getTime()
    elif state == 'align_base':
        dif = box_position.subtract(youBot_position)

        x1 = sqrt(dif.x * dif.x + dif.z * dif.z)

        alpha = -asin(dif.z / x1)

        rest = cont.get_object_rotation("box")[3] % (pi / 4.0)

        if rest > (pi / 4.0):
            theta = -((pi / 2.0) - rest)
        else:
            theta = -rest
        
        angle_error = alpha + (theta - youBot_rotation_angle)

        youBot._arm.set_arms_position([0], [alpha])

        angle_out = angle_pid.compute(angle_error, start_time - end_time)

        youBot.set_wheels_speed([angle_out, -angle_out, angle_out, -angle_out])

        print(angle_error)

        if angle_error < 0.01:
            youBot.set_arm_height(Height.ARM_FRONT_CARDBOARD_BOX)
    elif state == 'pick':
        youBot.pickup()

        can_throw = True
    elif state == 'throw':
        youBot.throw()

        x = uniform(-.559, -.459)
        z = uniform(.246, -.254)

        cont.set_object_position('box', [x, .262492, z])

        can_throw = False
