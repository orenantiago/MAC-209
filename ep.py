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

#def eulerPosition(y0, v0, dt):#
#    return y0 + v0 * dt

#retorna v0 + g * seno_da_inclinação_da_rampa
#def dVelocity(v0, dt):
#    return v0 + 9.8 * 0.0784591 * dt

def dVelocity(v0):
    #a função retorna a aceleração do momento,
    #utilizando g = 9.8, seno da inclinação = 0.0784591 e a força de resistencia = 0.0295/v0

    if v0 == 0:
        return  9.8 * 0.0784591
    else:
        return  9.8 * 0.0784591 - 0.0295/v0


def euler(dt):
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
        y.append(y[i] + v[i] * dt)
        v.append(v[i] + dVelocity(v[i]) * dt)
        t.append(t0)
        i += 1

    return y, v, t

def eulerCromer (dt):
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
        v.append(v[i] + dt * dVelocity(v[i]))
        y.append(y[i] + v[i + 1] * dt)
        t.append(t0)
        i += 1

    return y, v, t

def eulerRichardson(dt):
    v = []
    y = []
    t = []
    i = 0
    t0 = 0
    dtmid = dt / 2
    v.append(0)
    y.append(0)
    t.append(t0)

    while y[i] < 30:
        t0 += dt
        vmid = v[i] + dtmid * dVelocity(v[i])
        ymid = y[i] + dtmid * v[i]
        v.append(v[i] + dt * dVelocity(v[i]))
        y.append(y[i] + dt * vmid)
        t.append(t0)
        i += 1

    return y, v, t

import csv

def pendulum_times(filenumber):
    # Função que recebe um arquivo "filenametoolbox" contendo dados do acelerômetro
    # e retorna os tempos nos pontos altos e baixos da trajetória do pêndulo.
    times = []
    points = []
    first_line = True
    time_10s = False
    start = False

    tmp_point = 1
    point_up = 2
    point_down = -1
    time_up = time_down = 0

    for row in csv.reader(open("pendulo/experimento" + str(filenumber) + ".csv", 'rt')):
        # Firulas/gambiarras iniciais
        if first_line == True:
            first_line = False
        elif time_10s == False:
            if float(row[0]) >= 10.0 and float(row[4]) < 1:
                time_10s = True
                point = 0

        # Análise dos dados propriamente dita
        if time_10s == True:
            # Força g
            g_force = float(row[4])

            if g_force < 1:
                point = 1
                if (tmp_point != point):
                    times.append(time_up)
                    points.append(point_up)
                    point_up = 2
            else:
                point = 0
                if (tmp_point != point):
                    times.append(time_down)
                    points.append(point_down)
                    point_down = -1

            if point == 1:
                if g_force < point_up:

                    time_up = float(row[0])
                    point_up = float(row[4])
            else:
                if g_force > point_down:
                    point_down = g_force
                    time_down= float(row[0])
                    point_down = float(row[4])

            tmp_point = point

    times.pop(0)
    points.pop(0)
    aux = times[0]
    for i in range(len(times)):
        times[i] -= aux
    return times, points

def pendulum_times_experimental(filenumber):
    # Função que recebe um arquivo "filenametoolbox" contendo dados do acelerômetro
    # e retorna os tempos nos pontos altos e baixos da trajetória do pêndulo.
    times = []
    points = []
    first_line = True
    weight = 9.8 * 0.27

    for row in csv.reader(open("pendulo/experimento" + str(filenumber) + ".csv", 'rt')):
        # Firulas/gambiarras iniciais
        if first_line == True:
            first_line = False
        else:
            times.append(float(row[0]))
            point = math.degrees(math.asin(float(row[4])/weight))
            points.append(point)
    return times, points

#space = [10,20,30]
#times, points = pendulum_times(2)
#times = timestamps(5)
#acc = accel_run(times)
#y,v,t = euler(0.05)
#y1,v1,t1 = eulerCromer(0.05)
#y2, v2, t2 = eulerRichardson(0.05)
#plt.plot(times, points, "b")
#plt.show()
#print(times)
#print(acc)
