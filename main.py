#  * Copyright (c) 10/02/2021 22:04
#  *
#  * Last modified 10/02/2021 21:14
#  * Miguel L. Rodrigues
#  * All rights reserved

from kb import KeyboardReader
from wbc_controller.wbc_controller import Controller
from youbot_control.enum.Height import Height
from youbot_control.enum.Orientation import Orientation
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
    youBot.gripper.release()
    youBot.arm.set_height(Height.ARM_FRONT_CARDBOARD_BOX)
    passive_wait(4.0)
    youBot.gripper.grip()
    passive_wait(1.0)
    youBot.arm.set_height(Height.ARM_BACK_PLATE_LOW)
    passive_wait(3.0)
    youBot.gripper.release()
    passive_wait(1.0)
    youBot.arm.reset()
    youBot.base.strafe_left()
    passive_wait(5.0)
    youBot.base.reset()
    passive_wait(1.0)
    youBot.base.turn_left()
    passive_wait(1.0)
    youBot.base.reset()
    youBot.arm.set_height(Height.ARM_BACK_PLATE_LOW)
    passive_wait(3.0)
    youBot.gripper.grip()
    passive_wait(1.0)
    youBot.arm.set_height(Height.ARM_RESET)
    passive_wait(2.0)
    youBot.arm.set_height(Height.ARM_FRONT_PLATE)
    youBot.arm.set_orientation(Orientation.ARM_RIGHT)
    passive_wait(4.0)
    youBot.arm.set_height(Height.ARM_FRONT_FLOOR)
    passive_wait(2.0)
    youBot.gripper.release()
    passive_wait(1.0)
    youBot.arm.set_height(Height.ARM_FRONT_PLATE)
    passive_wait(2.0)
    youBot.arm.set_height(Height.ARM_RESET)
    passive_wait(2.0)
    youBot.arm.reset()
    youBot.gripper.grip()
    passive_wait(2.0)


automatic_behavior()

while cont.step() != -1:
    input_data = kb.get_input()

    if input_data == 'exit':
        kb.stop()
        break

    if input_data != last_input:
        if input_data == 'ih':
            youBot.arm.increase_height()
        elif input_data == 'dh':
            youBot.arm.decrease_height()
        elif input_data == 'io':
            youBot.arm.increase_orientation()
        elif input_data == 'do':
            youBot.arm.decrease_orientation()
        elif input_data == 'fw':
            youBot.base.forwards()
        elif input_data == 'bw':
            youBot.base.backwards()
        elif input_data == 'sl':
            youBot.base.strafe_left()
        elif input_data == 'sr':
            youBot.base.strafe_right()
        elif input_data == 'tl':
            youBot.base.turn_left()
        elif input_data == 'tr':
            youBot.base.turn_right()
        elif input_data == 'sb':
            youBot.base.reset()
        elif input_data == 'gg':
            youBot.gripper.grip()
        elif input_data == 'gr':
            youBot.gripper.release()

        last_input = input_data
