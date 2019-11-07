# -*- coding: utf-8 -*-

import os
from datetime import datetime

def createHTML(keys, objects):
	f = open("report.html","w")
	time = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
	message = """
	<!DOCTYPE html>
		<html>
		<head>
			<meta charset="utf-8">
			<title>
				Результаты сканирования
			</title>
			

			<style type="text/css">
				.block{
					    width:320px;
					    height:240px;
					    
					    display: block;
					    opacity: 1;
					    -webkit-transform: scale(1,1);
					    -webkit-transition-timing-function: ease-out;
					    -webkit-transition-duration: 220ms;
					    -moz-transform: scale(1,1);
					    -moz-transition-timing-function: ease-out;
					    -moz-transition-duration: 220ms;
					}
					.block:hover {
					    -webkit-transform: scale(2.5,2.5);
					    -webkit-transition-timing-function: ease-out;
					    -webkit-transition-duration: 220ms;
					    -moz-transform: scale(2.5,2.5);
					    -moz-transition-timing-function: ease-out;
					    -moz-transition-duration: 220ms;
					    z-index:99999999; 
					}
			</style>

		</head>
	<body>
	<img src='scaning.png' width="1120">
	<h4>"""
	message += "Время формирования отчёта - (" + time + ")"
	message += """</h4>

	<table border="1">
	<tr>
		<th>
			Частота
		</th>
		<th>
			Спектрограмма модельнго сигнала
		</th>
		<th>
			Спектрограмма записанного сигнала
		</th>
		<th>
			Диограмма совпадния
		</th>
	</tr>

	<tr>
	"""
	

	for i in range(len(keys)):
		freeq = keys[i].split(".")
		freeq = freeq[0] + "." + freeq[1]
		freeq = freeq.replace("finger_recording", "")
		message += """
		<td>
		""" + freeq + """
		</td>
		<td>
			<img src="original.png" width="320" height="240">
		</td>
		<td>
			<img src=""" + objects[i] + """ width="320" height="240">
		</td>
		<td>
			<img class="block" src=""" + keys[i] + """ width="320" height="240">
		</td>
	</tr>
	"""
	

	message += """
	</table>

	</body>
	</html>
	"""
	f.write(message)
	f.close()
	

if __name__ == '__main__':
	
	files = os.listdir(".")

	files.remove("original.png")
	files.remove("scaning.png")
	files.sort()
	
	keys = files[0:(len(files)//2)]
	objects = files[(len(files)//2):len(files)]
	createHTML(keys, objects)
