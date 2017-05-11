# -*- encoding: utf8 -*-

import SMonitor
import os.path
import ctypes
import struct
import time
from flask import *
from threading import *
from datetime import datetime
import json
import ast

__author__ = "Micael Martins"
__copyright__ = "Copyright 2016, Itelmatis"
__credits__ = ["Rui Palma, Ivo Vargas"]
__version__ = "1.0"
__maintainer__ = "Micael Martins"
__email__ = "micaelmartins@itelmatis.com"
__status__ = "Under Development"

debug_on = False

webserver = Flask(__name__)


@webserver.route("/")
def smonitor():
	try:
		return render_template("smonitor_data.html")
	except Exception, e:
		return str(e)


#@webserver.route("/dados/<SMfiltro>", methods=["POST","GET"])
@webserver.route("/dados/<SMfiltro>", methods=["POST"])
def resposta_javascript(SMfiltro):
	if SMfiltro == "all":
		return string_to_send
	sending = ast.literal_eval(string_to_send)
	filtered_string_to_send = ""
	temp_filter = []
	for f in SMfiltro.split(","):
		temp_filter.append(f)
	contador = 0
	for i in sending["DADOS"]:
		if i["indice"] in temp_filter:
			filtered_string_to_send += str(i)
			if contador < (len(temp_filter)) -1:
				filtered_string_to_send += ","
			contador += 1
	filtered_string_to_send = "{\"DADOS\":[" + str(filtered_string_to_send) + "]," + "\"DATAHORA\":" + str(sending["DATAHORA"]) + "," + "\"STATUS\":" + str(sending["STATUS"]) + "}"
	if debug_on:
		print filtered_string_to_send.replace("'", "\"")
	return filtered_string_to_send.replace("'", "\"")


@webserver.route("/dados/envia", methods=["POST"])
def javascript_SMonitor():
	indice = request.form.get("indice")
	valor = request.form.get("valor")
	#print str(Tags)
	#smonitor.Pull()
	Tags[int(indice)].value = float(valor)
	if smonitor.Push():
		print "push com sucesso"
	else:
		print "push fudeuuuu"
	if debug_on:
		print "recebido: " + str(indice) + " " + str(valor)
	return ('', 202)


def smonitor_to_json(self , data, timestamp):
	self.dados = data
	self.datahora = timestamp
	temp_data = "\"DADOS\":["
	temp_timestamp = ""
	SM_status = ""
	try:
		SMconnected = smonitor.Pull()
		valores_nao_nulos = 0
		for tag in smonitor.Tags:
			if tag.name != "-----------------FREE-----------------":
				valores_nao_nulos += 1
		contador = 1
		for tag in smonitor.Tags:
			if tag.name != "-----------------FREE-----------------":
				temp_data += "{" + "\"nome\"" + ":" "\"" + tag.name + "\"" + ","
				temp_data += "\"valor\"" + ":" "\"" + str(round((tag.value),3)) + "\"" + ","
				temp_data += "\"indice\"" + ":" "\"" + str(tag.index) + "\"" + "}"
				if contador != valores_nao_nulos:
					temp_data += ","
				else:
					temp_data += "],"
				contador += 1
		
		temp_timestamp = "\"DATAHORA\":" + "{" + "\"data\":" + "\"" + time.strftime("%d-%m-%Y") + "\"" + "," + "\"hora\"" + ":" "\"" + time.strftime("%H:%M:%S") + "\"" + "},"
		if SMconnected:
			processo.data = temp_data
			processo.timestamp = temp_timestamp
			SM_status = "\"STATUS\":" + "{" + "\"ligacao\":\"Ligado\"}"
		else:
			SM_status = "\"STATUS\":" + "{" + "\"ligacao\":\"Desligado\"}"
		
		values = "{" + processo.data + processo.timestamp + SM_status + "}"
		if debug_on:
			print values
		return values
	except Exception, e:
		print str(e)
		return False


class smonitor_thread (Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
		global string_to_send
		self.data = ""
		self.timestamp = ""
		while True:
			string_to_send = smonitor_to_json(self, self.data, self.timestamp)
			time.sleep(2)


if __name__ == '__main__':
	Tags = []
	smonitor = SMonitor.SMClient(Tags, r"C:\Users\Micael\Desktop\SMonitor Server\server.prt")
	processo = smonitor_thread()
	processo.start()
	time.sleep(2)
	webserver.run(debug=debug_on, host='0.0.0.0', port=80, threaded=True, use_reloader=False)
	
