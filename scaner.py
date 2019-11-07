# -*- coding: utf-8 -*-

import numpy as np
import peakutils
import csv
import sys
import subprocess
import matplotlib as mpl
import matplotlib.pyplot as plt

from collections import defaultdict
from math import pi
from config import Configurator


def csv_dict_list(variables_file):
    
    reader = csv.reader(open(variables_file, 'r'))
    dict_list = []
    for line in reader:
        dict_list.append(line)
    return dict_list

def frange(start, stop, step):
    i = 0
    f = start
    while f <= stop:
        f = start + step*i
        yield f
        i += 1

command = "rtl_power -f " + Configurator.START_FREEQ + "M:" + Configurator.END_FREEQ + "M:" + Configurator.SCAN_STEP + "k -g 50 -i 10 -e " + Configurator.SCAN_TIME + " data.csv"

subprocess.call(command, shell=True)

path = "data.csv"

sums = defaultdict(float)
counts = defaultdict(int)

for line in open(path):
    line = line.strip().split(', ')
    low = int(line[2])
    high = int(line[3])
    step = float(line[4])
    weight = int(line[5])
    dbm = [float(d) for d in line[6:]]
    for f,d in zip(frange(low, high, step), dbm):
        sums[f] += d*weight
        counts[f] += weight

ave = defaultdict(float)
for f in sums:
    ave[f] = sums[f] / counts[f]


incsv = ""

for f in sorted(ave):
    incsv += (','.join([str(f), str(ave[f])]))
    incsv += "\n"

outfile = open("data.csv", 'w')

outfile.write(incsv)

outfile.close()


device_values = csv_dict_list("data.csv")



freq = list()
gain = list()
 
for i in range(0,len(device_values)):
	
	non_dot = device_values[i][0].split(".")[0]
	device_values[i][0] = int(non_dot)

	freq.append(device_values[i][0])

	left = device_values[i][1].split(".")[0]
	right = device_values[i][1].split(".")[1]

	right = right[:2]
	
	device_values[i][1] = float(left + "." + right) #for python

	gain.append(device_values[i][1])


cb = np.array(gain)
indexes = peakutils.indexes(cb, thres=0.02/max(cb), min_dist=7)

freeqlist = list()
vertical = list()

for i in range(0, len(freq)):
	vertical.append(Configurator.PICK_SCALE)

for i in range(0,len(indexes)):
	if float(gain[indexes[i]]) > Configurator.PICK_SCALE:
		freeqlist.append(freq[indexes[i]])
	


print("Detected " + str(len(freeqlist)))

f = open("out.txt", "w")

for item in freeqlist:
    f.write("%s\n" % item)

f.close()

mpl.rcParams['font.family'] = 'fantasy'
mpl.rcParams['font.fantasy'] = 'Times New Roman', 'Ubuntu','Arial','Tahoma','Calibri'

fig = plt.figure(figsize=(9, 4), dpi=80, facecolor='w', edgecolor='k')
ax1 = fig.add_subplot(111)

ax1.plot(freq,gain,'b',label=u'Результаты сканирования')

ax1.plot(freq,vertical, 'r', lw=2, label=u'Порог срабатывания')

st = u'Загрузка диапазона 88-108 МГц на момент сканирования'
sy = u'Мощность сигнала db'
sx = u'Частота Гц'

ax1.set_title(st,size=20,color='green')
ax1.set_xlabel(sx,size=14,color='green')
ax1.set_ylabel(sy,size=12, color='black')
ax1.grid(True)
ax1.legend(loc='best',frameon=False)

plt.tight_layout() # автоматическое выравнивание элементов на холсте plt

plt.savefig("scaing.png", dpi=200)
