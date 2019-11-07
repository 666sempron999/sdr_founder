# -*- coding: utf-8 -*-

import numpy
import os
import sys
import re
import subprocess
import scipy.io.wavfile

import matplotlib as mpl

from matplotlib import pyplot, mlab
from collections import defaultdict

SAMPLE_RATE = 32000  # Hz
WINDOW_SIZE = 2048  # размер окна, в котором делается fft
WINDOW_STEP = 512   # шаг окна
WINDOW_OVERLAP = WINDOW_SIZE - WINDOW_STEP

def get_wave_data(wave_filename):
    sample_rate, wave_data = scipy.io.wavfile.read(wave_filename)
    assert sample_rate == SAMPLE_RATE, sample_rate
    if isinstance(wave_data[0], numpy.ndarray):  # стерео
        wave_data = wave_data.mean(1)
    return wave_data

def show_specgram(wave_data, name):
    fig = pyplot.figure()
    ax = fig.add_axes((0.1, 0.1, 0.8, 0.8))
    ax.specgram(wave_data,
        NFFT=WINDOW_SIZE, noverlap=WINDOW_OVERLAP, Fs=SAMPLE_RATE)
    #pyplot.show()
    pyplot.savefig(name + ".png", dpi=200)

def get_fingerprint(wave_data):
    # pxx[freq_idx][t] - мощность сигнала
    pxx, _, _ = mlab.specgram(wave_data,
        NFFT=WINDOW_SIZE, noverlap=WINDOW_OVERLAP, Fs=SAMPLE_RATE)
    band = pxx[15:250]  # наиболее интересные частоты от 60 до 1000 Hz
    return numpy.argmax(band.transpose(), 1)  # max в каждый момент времени

def compare_fingerprints(base_fp, fp, name):
    
    base_fp_hash = defaultdict(list)
    for time_index, freq_index in enumerate(base_fp):
        base_fp_hash[freq_index].append(time_index)
    matches = [t - time_index # разницы времен совпавших частот
        for time_index, freq_index in enumerate(fp)
        for t in base_fp_hash[freq_index]]

    mpl.rcParams['font.family'] = 'fantasy'
    mpl.rcParams['font.fantasy'] = 'Times New Roman', 'Ubuntu','Arial','Tahoma','Calibri'

    pyplot.clf()
    pyplot.hist(matches, 1000)

    pyplot.xlabel(u'Время')
    pyplot.ylabel(u'Коэффициент совпадения звуковой частоты')


    #pyplot.show()
    pyplot.savefig("finger_" + name + ".png", dpi=200)

if __name__ == '__main__':
    
    if len(sys.argv) < 2:

        print('python audio_analize.py pattern.wav')

    else:	

        d1 = get_wave_data(sys.argv[1])    	
        show_specgram(d1, "original")
        fp1 = get_fingerprint(d1)
        os.chdir("records/")
        fileList = os.listdir(".")

        if len(fileList) > 0:
            os.mkdir("report")
            os.chdir("..")

            subprocess.call("mv original.png records/report", shell=True)
            subprocess.call("cp scaing.png records/report", shell=True)
            subprocess.call("cp report.py records/report", shell=True)

            os.chdir("records")
			

        for i in range(0,len(fileList)):

            d2 = get_wave_data(fileList[i])
            show_specgram(d2, fileList[i])
            fp2 = get_fingerprint(d2)
            compare_fingerprints(fp1, fp2, fileList[i])
            subprocess.call("mv *.png report", shell=True)
