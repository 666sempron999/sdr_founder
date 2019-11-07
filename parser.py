# -*- coding: utf-8 -*-

import re
import os
import sys
# import commands
import subprocess

from subprocess import Popen
from config import Configurator

def ReadLog(filename):
	'''
	RUS
	Данная функция читает файл с отчётом и выделяет из него важную информацию
	filename - имя файла
	Возвращает только нужную часть лога
	ENG
	This function read a report file and extracts important information from it
	filename - name of file
	return - important part of log
	'''

	f = open(filename)

	freeqlist = list()

	for line in f.readlines():
		freeqlist.append(line[:-1])

	for i in range(0,len(freeqlist)):
		if len(freeqlist[i])==8:
			freeqlist[i] = freeqlist[i][:2] + "." + freeqlist[i][2:]
			print(freeqlist[i])

		elif len(freeqlist[i])==9:
			freeqlist[i] = freeqlist[i][:3] + "." + freeqlist[i][3:]
			print(freeqlist[i])
	
	return freeqlist
	

def ParseLog(text):
	'''
	RUS
	Данная функция выделяет из лога частоту (через freqPatern) и ширину окна для чигнала (freqWidth)
	text - весь лог
	freqPatern,freqWidth - регулярные выражения
	d - словарь(dict{freqPatern:freqWidth})
	ENG
	This function distinguish frequency from log (via freqPatern) and the width of the window for the signal (freqWidth)
	text - all log
	freqPatern,freqWidth - Regular expressionsя
	d - dict{freqPatern:freqWidth}
	'''
	
	freqPatern = re.compile(r'\d{2,3}.\d{6}\s{1}MHz')
	freqWidth = re.compile(r'\d{2,3}.\d{6}\s{1}kHz')

	freqList = freqPatern.findall(text)
	wigthList = freqWidth.findall(text)
	
	d = dict(zip(freqList, wigthList))

	return d

def ClearParametr(text):
	'''
	RUS
	Эта функция отделяет значение параметра от едицницы измерений
	text - список параметров (96.094500 MHz)
	newList - список частот
	ENG
	This function separates the value of the parameter from the unit of measurement
	Text - the list of parameters (96.094500 MHz)
	NewList - list Frequencies
	'''

	newList = []
	for i in range(0, len(text)):
		parametr = text[i].split(" ")
		newList.append(parametr[0])

	return newList

def WriteWave(freeqList):
	try:
		os.mkdir("records")
	except OSError:
		print("Удалите каталог с именем records")
		sys.exit()
		
	
	os.chdir("records/")

	for i in range(0, len(freeqList)):
		command = "rtl_fm -M wbfm -f " + str(freeqList[i]) + "M -F 8 -l 50 | sox -t raw -e signed -c 1 -b 16 -r " + Configurator.WAV_BITRATE + " - recording" + str(freeqList[i]) + ".wav"
		#rtl_fm -M wbfm -f 91.73M -F 8 -l 50 | sox -t raw -e signed -c 1 -b 16 -r 32000 - recording.wav

		#subprocess.Popen(command, shell = True)
		subprocess.call(command, shell=True)
		#result = commands.getoutput(command)
		


if __name__ == '__main__':

	freq = ReadLog("out.txt")

	"""

	l = ReadLog("out.txt")
	d = ParseLog(l)
	
	freq = d.keys()

	print(freq)
	"""

	clear = ClearParametr(freq)

	print("Обнаружено волн - " + str(len(clear)))
	WriteWave(clear)
	
	
