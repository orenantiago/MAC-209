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
            times.append([t1, t2, t3])
        first_line = False
    return times

print(timestamps("mruv/experimento1"))
