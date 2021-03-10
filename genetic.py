#  * Copyright (c) 10/03/2021 17:02
#  *
#  * Last modified 10/03/2021 17:02
#  * Miguel L. Rodrigues
#  * All rights reserved

from lib.network.network import Network, load_network
from lib.utils.vector import Vector
from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.youBot import YouBot
from math import atan2, sin, cos
import matplotlib.pyplot as plt

fig = plt.figure()

ax1 = fig.add_subplot()


def normalize(value: float) -> float:
    return atan2(sin(value), cos(value))


cont = Controller(14, True)
youBot = YouBot(cont)

networks = []

errors = []

max_per_generation = 10
generations = 1000

for i in range(max_per_generation):
    networks.append(Network([1, 8, 16, 16, 8, 1]))

count = 0
current = 0
xx = [0]

time_interval = 10
last_time = 0

max_velocity = 64

network = networks[current]

# network = load_network("network1.json")

print("Geracao: {} de {}".format(count, generations))

center = youBot.get_position()
initial_position = center

angle = .0

comp = .01

fitness_list = [.0]

target_fit = .0001

while cont.step() != -1:
    time = cont.get_supervisor().getTime()

    youBot_position = youBot.get_position()

    youBot_rotation_angle = youBot.get_rotation_angle()

    angle += comp

    if angle > 3.14:
        comp = -.01

    if angle < -3.14:
        comp = .01

    x = 0.8 * cos(angle)
    z = 0.8 * sin(angle)

    center.add(Vector([x, .0, z]))

    cont.set_object_position("box", [center.x, center.y, center.z])

    theta = youBot_position.differenceAngle(center)

    center.subtract(Vector([x, .0, z]))

    angle_error = normalize(youBot_rotation_angle + theta)

    errors.append(angle_error)

    if (time > last_time + 1) and (time % time_interval == 0):
        last_time = time

        if count < generations:
            sum_errors = .0

            for error in errors:
                sum_errors += abs(error)

            fitness = (sum_errors / len(errors)) + initial_position.distance(youBot.get_position())

            fit_err = 0.5 * pow(target_fit - fitness, 2.0)

            if fit_err <= target_fit:
                break

            network.set_fitness(fitness)

            fitness_list.append(fitness)

            cont.set_object_position("youBot", [initial_position.x, initial_position.y, initial_position.z])

            print("Individuo {} | Fitness {} | Fit Err {}".format(current, fitness, fit_err))

            errors.clear()

            current += 1

            xx.append(xx[-1] + 1.0)

            if current == len(networks):
                count += 1

                networks.sort(key=lambda n: n.get_fitness())

                best_fitness = networks[0].get_fitness()

                father = networks[0]
                mother = networks[1]

                networks.clear()

                for i in range(max_per_generation):
                    net = Network([1, 8, 16, 16, 8, 1])

                    net.cross_over(father, mother)

                    net.mutate(.3)

                    networks.append(net)

                print("Best fitness: {}".format(best_fitness))

                print("Geracao: {} de {}".format(count, generations))

                current = 0

            network = networks[current]

    output = network.predict([angle_error])

    speed = output.get_value(0, 0) * max_velocity

    youBot.set_wheels_speed([speed, -speed, speed, -speed])


network.save("network1.json")

ax1.clear()

ax1.plot(xx, fitness_list)

plt.show()