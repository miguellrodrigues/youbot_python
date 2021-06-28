import json

from lib.utils.numbers import random_double, random_int
from math import pi


def randomize(x, min, max):
    return x + random_double(min, max)


def _map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


with open("output_dataset.json", "r") as file:
    data = json.load(file)

errors = data['errors']
sig = data['sig']
outputs = data['out']

_errors = []
_sig = []
_outputs = []

mx = 1024

classes = [.0, 1.0]
values_classes = [[], []]

lines = []

for i in range(len(classes)):
    c = 0

    for j in range(len(outputs)):
        if c >= mx / 4:
            c = 0
            break

        if outputs[j] == classes[i]:
            pos = random_int(0, len(errors) - 1)

            line = {
                'error': _map(errors[pos], -pi, pi, .0, 1.0),
                'sig': sig[pos],
                'out': outputs[pos]
            }

            lines.append(line)

            modified_line = {
                'error': randomize(line['error'], -.05, .05),
                'sig': randomize(line['sig'], -.05, .05),
                'out': line['out']
            }

            lines.append(modified_line)

            c += 1


lines.sort(key=lambda x: x['out'] == 0)

for i in range(len(lines)):
    _errors.append(lines[i]['error'])
    _sig.append(lines[i]['sig'])
    _outputs.append(lines[i]['out'])

data = {
    "errors": _errors,
    "sig": _sig,
    "out": _outputs
}

with open("data-{}.json".format(mx), "w") as sfile:
    json.dump(data, sfile)
