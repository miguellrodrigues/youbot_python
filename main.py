#  * Copyright (c) 10/02/2021 22:04
#  *
#  * Last modified 10/02/2021 21:14
#  * Miguel L. Rodrigues
#  * All rights reserved

from keyboard_reader import KeyboardReader

from webots_lib.wbc_controller import Controller
from youbot_control.enum import Height, Orientation

from youbot_control.youBot import YouBot

kb = KeyboardReader()

kb.start()

cont = Controller(14, True)
youBot = YouBot(cont)

input_data = kb.get_input()
last_input = '.'


def passive_wait(sec):
    start_time = cont.get_supervisor().getTime()

    while start_time + sec > cont.get_supervisor().getTime():
        cont.step()


passive_wait(2.0)


def automatic_behavior():
    passive_wait(2.0)
    youBot.grip_release()
    youBot.set_arm_height(Height.ARM_FRONT_CARDBOARD_BOX)
    passive_wait(4.0)
    youBot.grip()
    passive_wait(1.0)
    youBot.set_arm_height(Height.ARM_BACK_PLATE_LOW)
    passive_wait(3.0)
    youBot.grip_release()
    passive_wait(1.0)
    youBot.arm_reset()
    youBot.strafe_left()
    passive_wait(5.0)
    youBot.base_reset()
    passive_wait(1.0)
    youBot.turn_left()
    passive_wait(1.0)
    youBot.base_reset()
    youBot.set_arm_height(Height.ARM_BACK_PLATE_LOW)
    passive_wait(3.0)
    youBot.grip()
    passive_wait(1.0)
    youBot.set_arm_height(Height.ARM_RESET)
    passive_wait(2.0)
    youBot.set_arm_height(Height.ARM_FRONT_PLATE)
    youBot.set_arm_orientation(Orientation.ARM_RIGHT)
    passive_wait(4.0)
    youBot.set_arm_height(Height.ARM_FRONT_FLOOR)
    passive_wait(2.0)
    youBot.grip_release()
    passive_wait(1.0)
    youBot.set_arm_height(Height.ARM_FRONT_PLATE)
    passive_wait(2.0)
    youBot.set_arm_height(Height.ARM_RESET)
    passive_wait(2.0)
    youBot.arm_reset()
    youBot.grip()
    passive_wait(2.0)


automatic_behavior()

while cont.step() != -1:
    input_data = kb.get_input()

    if input_data == 'exit':
        kb.stop()
        break

    if input_data != last_input:
        if input_data == 'ih':
            youBot.increase_arm_height()
        elif input_data == 'dh':
            youBot.decrease_arm_height()
        elif input_data == 'io':
            youBot.increase_arm_orientation()
        elif input_data == 'do':
            youBot.decrease_arm_orientation()
        elif input_data == 'fw':
            youBot.forwards()
        elif input_data == 'bw':
            youBot.backwards()
        elif input_data == 'sl':
            youBot.strafe_left()
        elif input_data == 'sr':
            youBot.strafe_right()
        elif input_data == 'tl':
            youBot.turn_left()
        elif input_data == 'tr':
            youBot.turn_right()
        elif input_data == 'sb':
            youBot.base_reset()
        elif input_data == 'gg':
            youBot.grip()
        elif input_data == 'gr':
            youBot.grip_release()

        last_input = input_data
