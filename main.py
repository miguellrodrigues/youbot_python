from wbc_controller.wbc_controller import Controller
from youbot_control.youBot import YouBot

cont = Controller(14, True)
youBot = YouBot(cont)

while cont.step() != -1:
    youBot.base.backwards()