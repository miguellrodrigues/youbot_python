#  * Copyright (c) 12/02/2021 11:48
#  *
#  * Last modified 12/02/2021 11:48
#  * Miguel L. Rodrigues
#  * All rights reserved

from math import radians, pi
from random import uniform

from lib.utils.pid import Pid
from lib.utils.vector import Vector, normalize_radian
from lib.webots_lib.wbc_controller import Controller
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
    youBot_rotation_angle = normalize_radian(youBot.get_rotation_angle())

    box_position = Vector(cont.get_object_position("box"))

    theta = youBot_position.differenceAngle(box_position)

    angle_error = normalize_radian(youBot_rotation_angle + theta)

    distance_error = (box_position.distance(youBot_position) - minimum_distance)

    youBot.set_wheels_speed([.0, .0, .0, .0])

    if state == 'align' and (in_tolerance(distance_error, distance_tolerance)) and (
            in_tolerance(angle_error, angle_tolerance)):
        state = 'pick'
    elif state == 'pick' and can_throw:
        state = 'throw'
    elif state == 'throw' and not can_throw:
        state = 'align'

    if state == 'align':
        angle_out = angle_pid.compute(angle_error, start_time - end_time)
        distance_out = distance_pid.compute(distance_error, start_time - end_time)

        out_plus = angle_out + distance_out
        out_minus = angle_out - distance_out

        youBot.set_wheels_speed([-out_minus, out_plus, out_plus, -out_minus])

        end_time = cont.get_supervisor().getTime()
    elif state == 'pick':
        orientation = .0

        box_rotation = cont.get_object_rotation("box")[3]

        rest = (box_rotation % (pi / 4))

        if rest > pi / 4.0:
            orientation = -((pi / 2.0) - rest)
        else:
            orientation = rest

        youBot.pickup(orientation)

        can_throw = True
    elif state == 'throw':
        youBot.throw()

        x = uniform(0.432629, 0.572629)
        z = uniform(-0.187101, 0.302899)

        cont.set_object_position('box', [x, .262492, z])
        cont.set_object_rotation('box', [.01, .01, .01, uniform(-pi, pi)])

        can_throw = False
