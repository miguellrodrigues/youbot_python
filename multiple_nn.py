#  * Copyright (c) 09/03/2021 14:45
#  *
#  * Last modified 09/03/2021 14:45
#  * Miguel L. Rodrigues
#  * All rights reserved

from lib.network.network import Network, load_network
from lib.utils.pid import Pid
from lib.utils.vector import Vector
from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.youBot import YouBot
from math import *

cont = Controller(14, True)
youBot = YouBot(cont)

align_network = Network([1, 16, 32, 1])

while cont.step() != -1:
    pass
