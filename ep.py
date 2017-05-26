# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import csv
import math


#lê o o numero do arquivo de de tempos do mruv

def MruvTimesSpaces(filenumber):
    times = []
    spaces = [10, 20, 30]
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
        return times, spaces

#retorna a aceleração de uma descida, recebendo o vetor de tempos dela
def accelRun(times):
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
#def accMruv(v0, dt):
#    return v0 + 9.8 * 0.0784591 * dt

def accMruv(v0):
    #a função retorna a aceleração do momento,
    #utilizando g = 9.8, seno da inclinação = 0.0784591 e a força de resistencia = 0.0295/v0

    if v0 == 0:
        return  9.8 * 0.0784591
    else:
        return  9.8 * 0.0784591 - 0.0295/v0

#implementar aceleração do pendulo para algoritmos numéricos
#def accPendulum():
def accPendulum(teta, v0):
    return (- 9.8 * teta) / 0.85 - 1.04*(teta)**2

def euler(y0, dt, movement):
    t0 = 0
    y = []
    v = []
    t = []
    y.append(y0)
    v.append(0)
    t.append(t0)
    i = 0
    if(movement == "mruv"):
        while(y[i] <= 30):
            t0 += dt
            y.append(y[i] + v[i] * dt)
            v.append(v[i] + accMruv(v[i]) * dt)
            t.append(t0)
            i += 1
    else:
        while(t[i] < 120):
            t0 += dt
            y.append(y[i] + v[i] * dt)
            v.append(v[i] + accPendulum(y[i], v[i]) * dt)
            t.append(t0)
            i += 1

    return y, v, t

def eulerCromer (y0, dt, movement):
    t0 = 0
    i = 0
    v = []
    y = []
    t = []
    y.append(y0)
    v.append(0)
    t.append(t0)

    if(movement == "mruv"):
        while(y[i] <= 30):
            t0 += dt
            v.append(v[i] + dt * accMruv(v[i]))
            y.append(y[i] + v[i + 1] * dt)
            t.append(t0)
            i += 1
    else:
        while(t[i] < 120):
            t0 += dt
            v.append(v[i] + dt * accPendulum(y[i], v[i]))
            y.append(y[i] + v[i + 1] * dt)
            t.append(t0)
            i += 1

    return y, v, t

def eulerRichardson(y0, dt, movement):
    v = []
    y = []
    t = []
    i = 0
    t0 = 0
    dtmid = dt / 2
    v.append(0)
    y.append(y0)
    t.append(t0)

    while t[i] < 130:
        t0 += dt
        if movement == "mruv":
            vmid = v[i] + dtmid * accMruv(v[i])
            v.append(v[i] + dt * accMruv(v[i]))
        else:
            vmid = v[i] + dtmid * accPendulum(y[i], v[i])
            v.append(v[i] + dt * accPendulum(y[i], v[i]))
        ymid = y[i] + dtmid * v[i]
        y.append(y[i] + dt * vmid)
        t.append(t0)
        i += 1

    return y, v, t

def degtorad(deg):
    #transforma graus em radianos
    return (2*math.pi*deg/360)

def pendulumTimes(filenumber):
    # Função que recebe um arquivo "filenametoolbox" contendo dados do acelerômetro
    # e retorna os tempos nos pontos altos e baixos da trajetória do pêndulo.
    times = []
    points = []
    first_line = True
    before10s = True
    timesnew = []
    pointsnew = []
    for row in csv.reader(open("pendulo/experimento" + str(filenumber) + ".csv", 'rt')):
        # Firulas/gambiarras iniciais
        if first_line == True:
            first_line = False
        elif before10s == True:
            if float(row[0]) >= 10.0:
                before10s = False
        elif float(row[0]) <= 130.0:
            times.append(float(row[0]))
            point = float(row[4])
            points.append(point)
        else:
            break
    aux = times[0]
    for i in range(len(times)):
        times[i] -= aux
    dt = 0.55
    diff = 0
    downFound = False
    upFound = True
    searches = 0
    i = 0
    j = 0
    while i < len(times) and j < len(times):

        j = i + 1
        while diff <= dt and j < len(times):
            if points[i] > points[j]:
                i = j
                diff = 0
            else:
                diff = times[j] - times[i]
                j += 1
        timesnew.append(times[i])
        pointsnew.append(points[i])
        diff = 0

        j = i + 1
        while diff <= dt and j < len(times):
            if points[i] < points[j]:
                i = j
                diff = 0
            else:
                diff = times[j] - times[i]
                j += 1

        timesnew.append(times[i])
        pointsnew.append(points[i])
        diff = 0

    angles = []
    times = []

    osc = 0

    for i in range(0,len(pointsnew),2):
        ang = (math.pi / 6) * (pointsnew[i+1]-pointsnew[i])/(pointsnew[1]-pointsnew[0])
        if (ang > degtorad(4.5)):
            angles.append(((-1)**(osc))*ang)
            times.append(timesnew[i])
            angles.append(0)
            times.append(timesnew[i+1])
            osc+=1

    y,v,t = eulerCromer(math.pi/6, 0.05, "pendulo")
    plt.plot(times, angles,"bo",t,y,"r")
    plt.ylabel('angulo (°)')
    plt.xlabel('tempo (s)')
    plt.show()

    return timesnew, pointsnew

def main():
    dt = float(input("Informe dt:\n"))
    print("Analisando experimento da rampa...")
    corridas = []
    acelCorridas = []
    for i in range(1, 6):
        tempo, espaco = MruvTimesSpaces(i)
        acelCorrida = accelRun(tempo)
        eulerS, eulerV, eulerT = euler(0, dt, "mruv")
        cromerS, cromerV, cromerT = eulerCromer(0, dt, "mruv")
        fig = plt.figure(1)

        plt.subplot(221)
        plt.title("x(t)")
        plt.plot(tempo, espaco, 'o', label='Oficial')
        plt.plot(eulerT, eulerS, label='Euler')
        plt.plot(cromerT, cromerS, label='Euler-Cromer')
        plt.ylabel('Espaço (m)')
        plt.xlabel('Tempo (s)')
        plt.legend()

        plt.subplot(222)
        plt.title("v(t)")
        plt.plot(eulerT, eulerV, label='Euler')
        plt.plot(cromerT, cromerV, label='Euler-Cromer')
        plt.ylabel('Velocidade (m/s)')
        plt.xlabel('Tempo(s)')
        plt.legend()

        plt.savefig('corrida' + str(i))
        plt.close(fig)
    print("finalizado.")
if __name__ == '__main__':
    main()
