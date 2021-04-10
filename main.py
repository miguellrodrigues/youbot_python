#  * Copyright (c) 12/02/2021 11:48
#  *
#  * Last modified 12/02/2021 11:48
#  * Miguel L. Rodrigues
#  * All rights reserved

from math import radians
from random import uniform

from lib.utils.pid import Pid
from lib.utils.vector import Vector
from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.youBot import YouBot

cont = Controller(16, True)
youBot = YouBot(cont)

angle_pid = Pid(8.0, 0.05, 6.0, 10.0, .3)
distance_pid = Pid(5.0, .01, 2.0, 5.0, .01)

start_time = .0
end_time = .0

launch_x = -.9
launch_z = -0.0562697

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
    youBot_rotation_angle = youBot.get_rotation_angle()

    box_position = Vector(cont.get_object_position("box"))

    angle_error = (youBot_rotation_angle + youBot_position.differenceAngle(box_position))

    distance_error = (box_position.distance(youBot_position) - minimum_distance)

    youBot.set_wheels_speed([.0, .0, .0, .0])

    if state == 'align' and (in_tolerance(distance_error, distance_tolerance)) and (in_tolerance(angle_error, angle_tolerance)):
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
        youBot.pickup(0)

        x_err = launch_x - youBot.get_position().x
        z_err = launch_z - youBot.get_position().z

        while (abs(x_err) > .01 or abs(z_err) > .01) and cont.step() != -1:
            u_x = x_err * 12
            u_z = z_err * 12

            youBot.set_wheels_speed([-u_z + u_x, u_z + u_x, u_z + u_x, -u_z + u_x])

            z_err = launch_z - youBot.get_position().z
            x_err = launch_x - youBot.get_position().x

        youBot.set_wheels_speed([.0, .0, .0, .0])
        youBot.passive_wait(.5)

        can_throw = True
    elif state == 'throw':
        youBot.throw()

        x = uniform(-0.509027, -0.419027)
        z = uniform(-0.296191, 0.253809)

        cont.set_object_position('box', [x, .282492, z])

        can_throw = False
