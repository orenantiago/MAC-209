# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import csv

#lê o arquivo de tempos do mruv
def timestamps(filename):
    times = []
    first_line = True
    i = 0
    for row in csv.reader(open(filename + '.csv', 'rt')):
        if first_line == False:
            t1 = float(row[0])
            t2 = float(row[1])
            t3 = float(row[2])
            times.append(t1)
            times.append(t2)
            times.append(t3)
        first_line = False
    return times

#retorna a aceleração de uma descida, recebendo o vetor de tempos dela
def accel_run(times):
    tf_to = 0 # tf - to

    # Matriz dos tempos
    delta_s = 10

    delta_t = times[2] - times[1]
    tf_to += delta_t/2
    vf = delta_s/delta_t

    delta_t = times[1] - times[0]
    tf_to += delta_t/2
    vo = delta_s/delta_t
    accel = (vf-vo)/tf_to

    return accel


times = timestamps("mruv/experimento5")
acc = accel_run(times)
print(times)
print(acc)
