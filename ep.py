# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import csv

#lê o o numero do arquivo de de tempos do mruv
def timestamps(filenumber):
    times = []
    first_line = True
    for i in range(1,5):
        for row in csv.reader(open(experimento + str(filenumber) + '.csv', 'rt')):
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

def pendulum_times(filenametoolbox):
    # Função que recebe um arquivo "filenametoolbox" contendo dados do acelerômetro
    # e retorna os tempos nos pontos altos e baixos da trajetória do pêndulo.
    times = []
    first_line = True
    time_10s = False
    point_up = 2
    point_down = -1
    time_up = time_down = 0

    for row in csv.reader(open(filenametoolbox + str(i) + ".csv", 'rt')):
        # Firulas/gambiarras iniciais
        if first_line == True:
            first_line = False
        elif time_10s == False:
            if float(row[0]) >= 10.0:
                time_10s = True

        # Análise dos dados propriamente dita
        if time_10s == True:
            # Força g
            g_force = float(row[4])

            # Encontrando o tempo do ponto alto
            if g_force < 1 and g_force < point_up:
                point_up = g_force

            # Encontrando o tempo do ponto baixo
            elif g_force >= 1 and g_force >= point_down:
                point_down = g_force



    return times

times = timestamps("mruv/experimento5")
acc = accel_run(times)
print(times)
print(acc)
