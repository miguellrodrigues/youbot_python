#  * Copyright (c) 22/03/2021 17:55
#  *
#  * Last modified 22/03/2021 17:55
#  * Miguel L. Rodrigues
#  * All rights reserved

from datetime import datetime
from random import SystemRandom
from math import atan2, sin, cos

sr = SystemRandom()

sr.seed(datetime.timestamp(datetime.now()))


def random_double(minimum, maximum):
    return sr.uniform(minimum, maximum)


def random_int(minimum, maximum):
    return sr.randint(minimum, maximum)


def random_item(lst):
    return sr.choice(lst)


def normalize(value: float) -> float:
    return atan2(sin(value), cos(value))