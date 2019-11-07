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
			<title>
				
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
	<img src='scaing.png' width="1120">
	<h4>"""
	message += "Îò÷¸ò ñôîðìèðîâàí (" + time + ")"
	message += """</h4>

	<table border="1">
	<tr>
		<th>
			×àñòîòà
		</th>
		<th>
			Îðèãèíàë
		</th>
		<th>
			Çàïèñü
		</th>
		<th>
			Êîððåëÿöèÿ
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
			<img class="block" src=""" +  keys[i]+ """ width="320" height="240">
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
	
	files = os.listdir(".")#ïîëó÷åíèå ñïèñêà ôàéëîâ â òåêóùåé äèðåêòîðèè
	
	files.remove("report.pyc")
	files.remove("original.png")#óäàëåíèå ôàéëîâ, êîòîðûå íå ó÷àñòâóþò â ôîðìèðîâàíèè îò÷¸òà
	files.remove("scaing.png")
	files.sort()
	
	keys = files[0:((len(files))/2)]# Çäåñü èìåíà ôàéëîâ ñ êîðåëÿöèÿìè
	objects = files[((len(files))/2):len(files)]#Çäåñü èìåíà ôàéëîâ ñ çàïèñÿìè

	createHTML(keys, objects)


	