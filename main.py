from wbc_controller.wbc_controller import Controller
from youbot_control.arm import Arm, Height, Orientation

cont = Controller(14, True)
arm = Arm(cont)

a = 0
b = 0

while cont.step() != -1:
   print(2)
