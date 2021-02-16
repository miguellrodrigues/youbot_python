#  * Copyright (c) 10/02/2021 22:04
#  *
#  * Last modified 10/02/2021 21:14
#  * Miguel L. Rodrigues
#  * All rights reserved

from keyboard_reader import KeyboardReader

from lib.webots_lib.wbc_controller import Controller

from lib.youbot_control.youBot import YouBot

kb = KeyboardReader()

kb.start()

cont = Controller(14, True)
youBot = YouBot(cont)

input_data = kb.get_input()
last_input = '.'

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
