# -*- coding: utf-8 -*-

import signal
import time
import os
import sys
import subprocess
import psutil

from config import Configurator
from subprocess import check_output

def get_pid(name):
	return list(map(int, check_output(["pidof", name]).split()))

def magic(name):
	for proc in psutil.process_iter():
		if proc.name() == name:
			return "ok"


number = len(open('out.txt', "r").readlines())


for i in range(0, number):

	try:
		pid = get_pid("rtl_fm")
	except subprocess.CalledProcessError:
		while magic("rtl_fm") != "ok":
			print("Основной процесс parser.py не запущен. Идентификация.....")
			time.sleep(0.5)
		
		pid = get_pid("rtl_fm")
	
	if pid is not None:
		time.sleep(Configurator.RECORD_TIME)
		print("Процесс {} вернул результат в файл на {} итерации".format(str(pid[0]), i+1))
		os.kill(pid[0], signal.SIGKILL)
		
	else:
		pass
