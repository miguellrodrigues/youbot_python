#  * Copyright (c) 14/02/2021 18:06
#  *
#  * Last modified 14/02/2021 18:06
#  * Miguel L. Rodrigues
#  * All rights reserved

class Pid:
    def __init__(self, kp, ki, kd, saturation, max_error):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.accumulator = .0
        self.error = .0
        self.old_error = .0

        self.saturation = saturation
        self.max_error = max_error

        self.out = .0

    def compute(self, error, time):
        self.old_error = error
        self.error = error

        if -self.saturation < self.out < self.saturation:
            if -self.max_error < error < self.max_error:
                self.accumulator += ((error + self.old_error) / 2.0) * time

        proportional = self.kp * error
        integral = self.ki * self.accumulator
        derivative = ((error + self.old_error) / 2.0) * time

        out = proportional + integral + derivative

        self.out = out

        return out