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
