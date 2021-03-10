#  * Copyright (c) 10/03/2021 17:02
#  *
#  * Last modified 10/03/2021 17:02
#  * Miguel L. Rodrigues
#  * All rights reserved
from typing import cast

from lib.network.network import Network
from lib.utils.vector import Vector
from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.youBot import YouBot
from math import atan2, sin, cos


def normalize(value: float) -> float:
    return atan2(sin(value), cos(value))


cont = Controller(14, True)
youBot = YouBot(cont)

networks = []
errors = []

max_per_generation = 2
generations = 50

for i in range(max_per_generation):
    networks.append(Network([1, 8, 8, 1]))

count = 0
current = 0

time_interval = 15
last_time = 0

max_velocity = 16

network = networks[current]

print("Geracao: {} de {}".format(count, generations))

while cont.step() != -1:
    time = cont.get_supervisor().getTime()

    youBot_position = youBot.get_position()
    box_position = Vector(cont.get_object_position("box"))

    youBot_rotation_angle = youBot.get_rotation_angle()

    theta = youBot_position.differenceAngle(box_position)

    angle_error = normalize(youBot_rotation_angle + theta)

    errors.append(angle_error)

    if (time > last_time + 1) and (time % time_interval == 0):
        last_time = time

        if count < generations:
            fitness = sum(errors) / len(errors)

            network.set_fitness(fitness)

            print("Individuo {} | Fitness {}".format(current, fitness))

            errors = []

            current += 1

            if current == len(networks):
                count += 1

                networks.sort(key=lambda x: x.get_fitness())

                best_fitness = networks[0].get_fitness()

                temp_networks = []

                father = cast(Network, networks[0])
                mother = cast(Network, networks[1])

                for i in range(max_per_generation):
                    net = Network([1, 8, 8, 1])

                    temp_networks.append(net)

                networks.clear()

                for i in range(len(temp_networks)):
                    net = temp_networks[i]

                    net.cross_over(father, mother)

                    net.mutate(.3)

                    networks.append(net)

                temp_networks.clear()

                print("Best fitness: {}".format(best_fitness))

                print("Geracao: {} de {}".format(count, generations))

                current = 0

            network = networks[current]

    output = network.predict([angle_error])

    speed = output.get_value(0, 0) * max_velocity

    youBot.set_wheels_speed([speed, -speed, speed, -speed])

network.save("network.json")
