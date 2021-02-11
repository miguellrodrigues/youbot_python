#  * Copyright (c) 10/02/2021 22:04
#  *
#  * Last modified 10/02/2021 20:44
#  * Miguel L. Rodrigues
#  * All rights reserved

import time
from threading import Thread


class KeyboardReader(Thread):
    def __init__(self):
        super().__init__()

        self.current_input = 'reset'
        self.new_input = False

        self.running = True

    def get_input(self):
        return self.current_input

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            self.current_input = '.'

            input_str = input()

            self.current_input = input_str

            time.sleep(.01)
