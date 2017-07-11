# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import csv

#recebe
# string name: nome que será salvo no arquivo
# delta_t: vetor de delta_t fornecido pela função accelerometer_time
# v_a: vetor de velocidades médias ou de acelerações médias, dependendo do movement
# points: vetor de instantes do cronometro para os espaços [10,20,30] ou [5,10,15,20,25,30]
#movement: string com o valor "mru" ou "mruv" que define o tipo de movimento
def plot_space(name, delta_t, v_a, points, movement):
    #se for os pontos paralelos
    x0 = np.arange(delta_t[0])
    x1 = np.arange(delta_t[1])
    x2 = np.arange(delta_t[2])
    time_avg = (delta_t[0] + delta_t[1] + delta_t[2]) / 3
    x_avg = np.arange(time_avg)
    if len(points[0]) == 3:
        points_spaces = [10,20,30]
        aux = 2
    else:
        points_spaces = [5,10,15,20,25,30]
        aux = 5

    if movement == "mruv":
        v0 = []
        v0.append((60 - v_a[0] * points[0][aux] ** 2) / (2 * points[0][aux]))
        v0.append((60 - v_a[1] * points[1][aux] ** 2) / (2 * points[1][aux]))
        v0.append((60 - v_a[2] * points[2][aux] ** 2) / (2 * points[2][aux]))

    fig = plt.figure(1)
    plt.title(name)
    #primeira corrida
    plt.subplot(221)
    if movement == "mru":
        plt.plot(x0, v_a[0] * x0, 'b', points[0], points_spaces, 'ro')
    elif movement == "mruv":
        plt.plot(x0, v0[0] * x0 + (v_a[0] * x0 * x0)/2, 'b', points[0], points_spaces, 'ro')
    plt.title('corrida 1')
    plt.ylabel('espaço (m)')

    #segunda corrida
    plt.subplot(222)
    if movement == "mru":
        plt.plot(x1, v_a[1] * x1, 'b', points[1], points_spaces, 'ro')
    elif movement == "mruv":
        plt.plot(x1, v0[1] * x1 + (v_a[1] * x1 * x1)/2, 'b', points[1], points_spaces, 'ro')
    plt.title('corrida 2')
    plt.ylabel('espaço (m)')

    #terceira corrida
    plt.subplot(223)
    if movement == "mru":
        plt.plot(x2, v_a[2] * x2, 'b', points[2], points_spaces, 'ro')
    elif movement == "mruv":
        plt.plot(x2, v0[2] * x2 + (v_a[2] * x2 * x2)/2, 'b', points[2], points_spaces, 'ro')
    plt.title('corrida 3')
    plt.ylabel('espaço (m)')
    plt.xlabel('tempo (s)')

    v_a_average = average(v_a)

    #média do corredor
    plt.subplot(224)
    if movement == "mru":
        plt.plot(x_avg, v_a_average * x_avg, 'b')
    elif movement == "mruv":
        plt.plot(x_avg, (v_a_average * x_avg * x_avg) / 2, 'b')
    plt.title('Média')
    plt.ylabel('espaço (m)')
    plt.xlabel('tempo (s)')
    plt.savefig(name)
    plt.close(fig)
    return v_a_average, time_avg
    # Recebe o parâmetro velocity (v) e plota a função de equação s(t) = v*t
    # O gráfico da função é nomeado por "name" e contém os pontos demarcados na matriz "points"


# param = velocity or acceleration
def plot_avg_space(name, delta_t, param, movement):
    if movement == "mru":
        fig = plt.figure(1)
        timevector = np.arange(delta_t)
        plt.plot(timevector, param * timevector, 'g')
        plt.title(name)
        plt.ylabel('espaço (m)')
        plt.xlabel('tempo (s)')
        plt.savefig(name)
        plt.close(fig)
    elif movement == "mruv":
        fig = plt.figure(1)
        timevector = np.arange(delta_t)
        plt.plot(timevector, param * (timevector * timevector) / 2, 'g')
        plt.title(name)
        plt.ylabel('espaço (m)')
        plt.xlabel('tempo (s)')
        plt.savefig(name)
        plt.close(fig)

def plot_velocity(name, delta_t, accelerations):
    x0 = np.arange(delta_t[0])
    x1 = np.arange(delta_t[1])
    x2 = np.arange(delta_t[2])
    time_average = (delta_t[0] + delta_t[1] + delta_t[2]) / 3
    x_avg = np.arange(time_average)

    fig = plt.figure(1)
    plt.title(name)
    #primeira corrida
    plt.subplot(221)
    plt.plot(x0, accelerations[0] * x0, 'b')
    plt.title('corrida 1')
    plt.ylabel('velocidade (m/s)')

    #segunda corrida
    plt.subplot(222)
    plt.plot(x1, accelerations[1] * x1, 'b')
    plt.title('corrida 2')
    plt.ylabel('velocidade (m/s)')

    #terceira corrida
    plt.subplot(223)
    plt.plot(x2, accelerations[2] * x2, 'b')
    plt.title('corrida 3')
    plt.ylabel('velocidade (m/s)')
    plt.xlabel('tempo (s)')

    v_a_average = average(accelerations)

    #média do corredor
    plt.subplot(224)
    plt.plot(x_avg, v_a_average * x_avg, 'b')
    plt.title('Média')
    plt.ylabel('velocidade (m/s)')
    plt.xlabel('tempo (s)')
    plt.savefig(name)
    plt.close(fig)

    return v_a_average, time_average
    # Recebee o parâmetro velocity (v) e plota a função de equação s(t) = v*t
    # O gráfico da função é nomeado por "name" e contém os pontos demarcados na matriz "points"

def plot_avg_velocity(name, delta_t, acceleration):
    fig = plt.figure(1)
    timevector = np.arange(delta_t)
    plt.plot(timevector, acceleration * timevector, 'g')
    plt.title(name)
    plt.ylabel('velocidade (m/s)')
    plt.xlabel('tempo (s)')
    plt.savefig(name)
    plt.close(fig)


def accelerometer_time(filenametoolbox):
    # Função que recebe um arquivo "filenametoolbox" contendo dados do acelerômetro
    # e retorna um deltaT (tempo de chegada - tempo de saída)
    delta_t = []
    first_line = True
    to_found = tf_found = False
    for i in range(1, 4):
        for row in csv.reader(open(filenametoolbox + str(i) + ".csv", 'rt')):
            if first_line == False:
                # Encontrando o tempo inicial
                if to_found == False:
                    tfg_to = float(row[4]) # Variável auxiliar
                    if (tfg_to < .900) or (tfg_to >= 1.100):
                        to = float(row[0])
                        to_found = True

                # Encontrando o tempo final
                elif tf_found == False:
                    tfg_tf = float(row[4]) # Variável auxiliar
                    if (tfg_tf >= .900) and (tfg_tf < 1.100):
                        tf = float(row[0])
                        tf_found = True
                else: # Caso em que > tf_found == True <
                    tfg_tf = float(row[4]) # Variável auxiliar
                    if (tfg_tf < .900) or (tfg_tf >= 1.100):
                        tf_found = False

            first_line = False

        delta_t.append(tf - to)

        first_line = True
        to_found = tf_found = False

    return delta_t

#NÃO CALCULEI AS MEDIAS DE TODAS AS PESSOAS JUNTAS
#recebe dois arquivos csv de relogio, das marcações paralelas e retorna as médias
#das marcações nos pontos 10, 20 e 30
def timestamps(filename1, filename2):
    times = []
    first_line = True
    i = 0
    for row in csv.reader(open(filename1 + '.csv', 'rt')):
        if first_line == False:
            t1 = float(row[0])
            t2 = float(row[2]) + t1
            t3 = float(row[4]) + t2
            times.append([t1, t2, t3])
        first_line = False
    first_line = True

    for row in csv.reader(open(filename2 + '.csv', 'rt')):
        if first_line == False:
            t1 = float(row[0])
            t2 = float(row[2]) + t1
            t3 = float(row[4]) + t2
            times[i][0] = (times[i][0] + t1) / 2
            times[i][1] = (times[i][1] + t2) / 2
            times[i][2] = (times[i][2] + t3) / 2
            i += 1
        first_line = False

    return times

#recebe dois arquivos csv de relogio, das marcações ALTERNADAS e retorna as médias
#das marcações nos pontos 5, 10, 15, 20, 25 e 30
def timestamps_alt(filename1, filename2):
    times = []
    space_array = [5, 10, 15, 20, 25, 30]
    first_line = True
    i = 0
    for row in csv.reader(open(filename1 + '.csv', 'rt')):
        if first_line == False:
            times.append([0,0,0,0,0,0])
            times[i][space_array.index(int(row[1]))] = float(row[0])
            times[i][space_array.index(int(row[3]))] = float(row[2])
            times[i][space_array.index(int(row[5]))] = float(row[4])
            i += 1
        first_line = False

    first_line = True
    i = 0
    for row in csv.reader(open(filename2 + '.csv', 'rt')):
        if first_line == False:
            times[i][space_array.index(int(row[1]))] = float(row[0])
            times[i][space_array.index(int(row[3]))] = float(row[2])
            times[i][space_array.index(int(row[5]))] = float(row[4])
            i += 1
        first_line = False

    #corrigindo a marcação unida dos dois relógios
    for i in range(len(times)):
        for j in range(2, 4):
            times[i][j] += times[i][j-2]
            times[i][j+2] += times[i][j]

    return times

def velocity_run(filenametoolbox):
    # Calcula um vetor com a velocidade média de cada corrida de um corredor
    velocities = []


    delta_t = accelerometer_time(filenametoolbox)

    for i in range(len(delta_t)):
        velocities.append(30/delta_t[i])

    return velocities

#def MRU_plot(velocity):

def accel_run(times):
    accelerations = [] # Vetor com as acelerações de cada corrida
    average_accel = 0 # variável auxiliar
    tf_to = 0 # tf - to

    # Matriz dos tempos
    if len(times[0]) == 3:
        delta_s = 10
    else:
        delta_s = 5

    len_spaces = len(times[0]) # Número de marcações na corrida

    for i in range(len(times)):
        len_deltav = len(times[i])-2 # Número de acelarações médias por corrida
        for j in range(2, len(times[i])):
            delta_t = times[i][j]-times[i][j-1]
            tf_to += delta_t/2
            vf = delta_s/delta_t

            delta_t = times[i][j-1]-times[i][j-2]
            tf_to += delta_t/2
            vo = delta_s/delta_t

            average_accel += (vf-vo)/tf_to
            tf_to = 0

        accelerations.append(average_accel/len_deltav)
        average_accel = 0

    return accelerations

def average(value_array):
    # Calcula a média das velocidades
    sum_values = 0
    size = len(value_array)
    for i in range(size):
        sum_values += value_array[i]

    return sum_values/size

def main():
    # Variáveis para construção dos gráficos

    delta_t = [] # delta_t de corridas de um corredor
    velocities_run = [] # Velocidade média de corridas de um corredor
    accelerations_run = [] # Aceleração média de corridas de um corredor
    velocities_runner = [] # Velocidade média de cada corredor
    accelerations_runner = [] # Aceleração média de cada corredor
    times_runner = [] # Tempo médio de corrida de cada corredor


    ### Mensagem no terminal ###
    print("Este programa gera e salva todos os gráficos de posições e velocidades médias de cada corrida e de todos os corredores.")


    ### MRU ###

    # j = 0 --> PRIMEIRA VERSÃO DO EXPERIMENTO
    # j = 1 --> SEGUNDA VERSÃO DO EXPERIMENTO
    for j in range(2):
        if j == 0:
            names = ["AllanCtePar", "RenanCtePar", "TiagoCtePar"] # Nome dos corredores - cronômetro par
        else:
            names = ["AllanCteAlt", "RenanCteAlt", "TiagoCteAlt"] # Nome dos corredores - cronômetro alternado

        # GRÁFICOS DE POSIÇÕES

        # 1. CADA CORREDOR E CADA CORRIDA

        # PARA CADA CORREDOR:
        # 3 GRÁFICOS DA POSIÇÃO MÉDIA POR CORRIDA
        # 1 GRÁFICO DA POSIÇÃO MÉDIA DO CORREDOR
        for i in range(len(names)):
            delta_t = accelerometer_time("input/" + names[i]) # Vetor de amostragem dos tempos nos gráficos
            velocities_run = velocity_run("input/" + names[i]) # Vetor de velocidades médias das corridas
            points = timestamps("input/" + names[i] + "E", "input/" + names[i] + "R") # Dados reais amostrados no cronômetro

            # Gráficos
            velocity, time = plot_space("posicao_constante_"+ names[i], delta_t, velocities_run, points, "mru")

            # Construção para o gráfico da média das posições constante dos corredores
            velocities_runner.append(velocity)
            times_runner.append(time)

        # 2. TODOS OS CORREDORES

        # Gráfico da média das posições constante dos corredores
        plot_avg_space("media_posicoes_constantes", average(times_runner), average(velocities_runner), "mru")

        velocities_runner = [] # Reutilização
        times_runner = []      # dos vetores


    ### MRUV ###

    # j = 0 --> PRIMEIRA VERSÃO DO EXPERIMENTO
    # j = 1 --> SEGUNDA VERSÃO DO EXPERIMENTO
    for j in range(2):
        if j == 0:
            names = ["AllanAcdPar", "RenanAcdPar", "TiagoAcdPar"] # Nome dos corredores - cronômetro par
        else:
            names = ["AllanAcdAlt", "RenanAcdAlt", "TiagoAcdAlt"] # Nome dos corredores - cronômetro alternado

        # GRÁFICOS DE VELOCIDADE

        # 1. CADA CORREDOR E CADA CORRIDA

        # PARA CADA CORREDOR:
        # 3 GRÁFICOS DA VELOCIDADE MÉDIA POR CORRIDA
        # 1 GRÁFICO DA VELOCIDADE MÉDIA DO CORREDOR
        for i in range(len(names)):
            delta_t = accelerometer_time("input/" + names[i]) # Vetor de amostragem dos tempos nos gráficos
            points = timestamps("input/" + names[i] + "E", "input/" + names[i] + "R") # Dados reais amostrados no cronômetro
            accelerations_run = accel_run(points) # Vetor de acelerações médias das corridas

            # Gráficos
            acceleration, time = plot_velocity("velocidade_acelerada_" + names[i], delta_t, accelerations_run)

            # Construção para o gráfico da média das velocidades dos corredores
            accelerations_runner.append(acceleration)
            times_runner.append(time)

        # 2. TODOS OS CORREDORES

        # Gráfico da média das velocidades dos corredores
        plot_avg_velocity("media_velocidades_aceleradas", average(times_runner), average(accelerations_runner))

        velocities_runner = [] # Reutilização
        times_runner = []      # dos vetores

        ### ### ###


        # GRÁFICOS DE POSIÇÕES

        # 1. CADA CORREDOR E CADA CORRIDA

        # PARA CADA CORREDOR:
        # 3 GRÁFICOS DA POSIÇÃO MÉDIA POR CORRIDA
        # 1 GRÁFICO DA POSIÇÃO MÉDIA DO CORREDOR
        for i in range(len(names)):
            delta_t = accelerometer_time("input/" + names[i]) # Vetor de amostragem dos tempos nos gráficos
            points = timestamps("input/" + names[i] + "E", "input/" + names[i] + "R") # Dados reais amostrados no cronômetro
            accelerations_run = accel_run(points)   # Vetor de acelerações médias das corridas

            # Gráficos
            acceleration, time = plot_space("posicao_acelerada_" + names[i], delta_t, accelerations_run, points, "mruv")

            # Construção para o gráfico da média das posições aceleradas dos corredores
            accelerations_runner.append(acceleration)
            times_runner.append(time)

        # 2. TODOS OS CORREDORES

        # Gráfico da média das posições aceleradas dos corredores
        plot_avg_space("media_posicoes_aceleradas", average(times_runner), average(accelerations_runner), "mruv")

        velocities_runner = [] # Reutilização
        times_runner = []      # dos vetores

    ### Mensagem no terminal ###
    print("Todos os gráficos foram salvos.")

main()
