#  * Copyright (c) 16/02/2021 14:03
#  *
#  * Last modified 16/02/2021 14:03
#  * Miguel L. Rodrigues
#  * All rights reserved
from lib.network.network import Network
from lib.utils.angle import calculate_angle
from lib.utils.matrix import array_to_matrix
from lib.utils.pid import Pid
from lib.utils.vector import normalize_radian, Vector
from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.youBot import YouBot


cont = Controller(14, True)
youBot = YouBot(cont)

angle_pid = Pid(8.0, 0.07, 2.0, 5.0, 1.0)

network = Network([1, 16, 32, 1])

while cont.step() != -1:
    time = cont.get_supervisor().getTime()

    youBot_position = youBot.get_position()
    box_position = Vector(cont.get_object_position("box"))

    youBot_rotation = cont.get_object_rotation("youBot")
    box_rotation = cont.get_object_rotation("box")

    angle = calculate_angle(youBot_rotation)

    theta = youBot_position.differenceAngle(box_position)

    angle_error = normalize_radian(angle + theta)

    if 0 < time < 5:
        # angle_error = normalize_radian(box_rotation[3] - angle)

        out = angle_pid.compute(angle_error, .05)

        youBot.set_wheels_speed([-out, out, -out, out])

        network.train(array_to_matrix([angle_error]), array_to_matrix([out]))
    else:
        out = network.predict(array_to_matrix([angle_error])).get_value(0, 0)

        print(out)

        x = out * 6

        youBot.set_wheels_speed([-x, x, -x, x])

