#  * Copyright (c) 12/02/2021 11:48
#  *
#  * Last modified 12/02/2021 11:48
#  * Miguel L. Rodrigues
#  * All rights reserved

from math import radians

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

radius = 0.5741111029669102

minimum_distance = 0.5441111029669102

while True:
    start_time = cont.get_supervisor().getTime()

    youBot_position = youBot.get_position()
    youBot_rotation_angle = normalize_radian(youBot.get_rotation_angle())

    box_position = Vector(cont.get_object_position("box"))

    theta = youBot_position.differenceAngle(box_position)

    angle_error = normalize_radian(youBot_rotation_angle + theta)

    can_pick = box_position.isInSphere(youBot_position, 0.5741111029669102) and box_position.distance(
        youBot_position) <= minimum_distance

    youBot.set_wheels_speed([.0, .0, .0, .0])

    if state == 'align' and ((angle_error < angle_tolerance) and (angle_error > -angle_tolerance)):
        state = 'walk'
    elif state == 'walk' and ((angle_error > angle_tolerance) or (angle_error < -angle_tolerance)):
        state = 'align'
    elif state == 'walk' and can_pick:
        state = 'pick'
    elif state == 'pick' and not can_pick:
        state = 'align'

    if state == 'walk':
        distance_error = (box_position.distance(youBot_position) - minimum_distance)

        out = distance_pid.compute(distance_error, start_time - end_time)

        youBot.set_wheels_speed([out, out, out, out])

        youBot.passive_wait(1.0)

        end_time = cont.get_supervisor().getTime()
    elif state == 'align':
        out = angle_pid.compute(angle_error, start_time - end_time)

        youBot.set_wheels_speed([-out, out, out, -out])

        youBot.passive_wait(1.0)

        end_time = cont.get_supervisor().getTime()
    elif state == 'pick':
        youBot.grip_release()
        youBot.passive_wait(0.8)
        youBot.set_arm_height(Height.ARM_FRONT_TABLE_BOX)
        youBot.passive_wait(2.0)
        youBot.grip()
        youBot.passive_wait(.8)

        state = 'throw'
    elif state == 'throw':
        youBot.throw()
        state = 'align'

    print(state)
