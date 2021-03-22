#  * Copyright (c) 10/03/2021 17:02
#  *
#  * Last modified 10/03/2021 17:02
#  * Miguel L. Rodrigues
#  * All rights reserved
import json

from lib.network.network import Network, cross_over
from lib.utils.numbers import normalize, random_item
from lib.utils.vector import Vector
from lib.webots_lib.wbc_controller import Controller
from lib.youbot_control.youBot import YouBot
from math import atan2, sin, cos, pi
import matplotlib.pyplot as plt
from datetime import datetime
import csv

fig = plt.figure()

ax1 = fig.add_subplot()


cont = Controller(20, True)
youBot = YouBot(cont)

networks = []

errors = []

max_per_generation = 2
generations = 200

topology = [2, 16, 16, 16, 1]

for i in range(max_per_generation):
    networks.append(Network(topology))

count = 0
current = 0

time_interval = 60
last_time = 0

max_velocity = 8

network = networks[current]

# network = load_network("network1.json")

print("Geracao: {} de {}".format(count, generations))

center = youBot.get_position()
initial_position = center

angle = .0

comp = .005

fitness_list = [.0]

target_fit = .0003

logs = []

while cont.step() != -1:
    time = cont.get_supervisor().getTime()

    youBot_position = youBot.get_position()

    youBot_rotation_angle = youBot.get_rotation_angle()

    if angle > pi or angle < -pi:
        comp *= -1

    angle += comp

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

            network.set_fitness(fitness)

            cont.set_object_position("youBot", [initial_position.x, initial_position.y, initial_position.z])

            logs.append("Individuo {} | Fitness {} | Fit Err {}".format(current, fitness, fit_err))

            print(logs[-1])

            errors.clear()

            current += 1

            if current == len(networks):
                count += 1

                networks.sort(key=lambda n: n.get_fitness())

                best_fitness = networks[0].get_fitness()

                fitness_list.append(best_fitness)

                father = networks[0]

                for i in range(max_per_generation):
                    net = Network(topology)

                    cross_over(net, father, random_item(networks))

                    net.mutate(.2)

                    networks.remove(networks[i])
                    networks.append(net)

                logs.append("Best fitness: {}".format(best_fitness))

                print(logs[-1])

                logs.append("Geracao: {} de {}".format(count, generations))

                print(logs[-1])

                current = 0

            network = networks[current]

    output = network.predict([abs(angle_error), 1.0 if angle_error > 0 else .0])

    s = max_velocity * output.get_value(0, 0)

    youBot.set_wheels_speed([-s, s, -s, s])

network.save("network1.json")

train_data = {
    "date": datetime.today().strftime('%d-%m-%Y-%H:%M:%S'),
    "topology": network.topology,
    "bias": network.bias,
    "max_generations": generations,
    "max_per_generation": max_per_generation,
    "log": logs
}

ax1.clear()

ax1.plot(range(len(fitness_list)), fitness_list)

plt.savefig("./img/img_{}.png".format(train_data['date']), dpi=600, format='png', bbox_inches='tight')
plt.show()

with open("./log/log_data_{}.json".format(train_data['date']), "w") as file:
    json.dump(train_data, file)


f = csv.writer(open("./csv/log_data_{}.csv".format(train_data['date']), "w"))

f.writerow(train_data.keys())
f.writerow(train_data.values())
