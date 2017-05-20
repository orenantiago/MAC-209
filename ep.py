# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import csv


#lê o o numero do arquivo de de tempos do mruv

def timestamps(filenumber):
    times = []
    first_line = True
    for i in range(1,5):
        for row in csv.reader(open("mruv/experimento" + str(filenumber) + '.csv', 'rt')):
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

def eulerPosition(y0, v0, dt):
    return y0 + v0 * dt

#retorna v0 + g * seno_da_inclinação_da_rampa
#def eulerVelocity(v0, dt):
#    return v0 + 9.8 * 0.0784591 * dt
def eulerVelocity(v0, acc, dt):
    if v0 == 0:
        return v0 + 9.8 * 0.0784591 * dt
    else:
        return v0 + (9.8 * 0.0784591 - 0.0295/v0) * dt


def euler(acc, dt):
    t0 = 0
    y = []
    v = []
    t = []
    y.append(0)
    v.append(0)
    t.append(t0)
    i = 0

    while(y[i] < 30):
        t0 += dt
        y.append(eulerPosition(y[i], v[i], dt))
        v.append(eulerVelocity(v[i], acc, dt))
        t.append(t0)
        i += 1

    return y, v, t

def eulerCromer (acc, dt):
    t0 = 0
    i = 0
    v = []
    y = []
    t = []
    y.append(0)
    v.append(0)
    t.append(t0)

    while(y[i] < 30):
        t0 += dt
        v.append(eulerVelocity(v[i], acc, dt))
        y.append(eulerPosition(y[i], v[i + 1], dt))
        t.append(t0)
        i += 1

    return y, v, t


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

space = [10,20,30]
times = timestamps(5)
acc = accel_run(times)
y,v,t = euler(acc, 0.05)
y1,v1,t1 = eulerCromer(acc, 0.05)
plt.plot(times, space, "bo", t, y, "r", t1, y1, 'g')
plt.show()
#print(times)
#print(acc)
