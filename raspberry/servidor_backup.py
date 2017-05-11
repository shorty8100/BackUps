# -*- encoding: utf8 -*-

import SMonitor
import os.path
import ctypes
import struct
import time
from flask import *
from threading import *
from Queue import *

__author__ = "Micael Martins"
__copyright__ = "Copyright 2016, Itelmatis"
__credits__ = ["Rui Palma, Ivo Vargas"]
__version__ = "0.1"
__maintainer__ = "Micael Martins"
__email__ = "micaelmartins@itelmatis.com"
__status__ = "Development"


webserver = Flask(__name__)


@webserver.route("/")
def smonitor():
	try:
		return render_template("smonitor_data3.html")
	except Exception, e:
		return str(e)


@webserver.route("/dados", methods=["POST"])
def smonitor_to_json():
		try:
			Tags = []
			smonitor = SMonitor.SMClient(Tags, "C:\\S-Monitor\\S-Monitor.prt")
			enviar = "["
			smonitor.Pull()
			valores_nao_nulos = 0
			for tag in smonitor.Tags:
				if tag.name != "-----------------FREE-----------------":
					valores_nao_nulos += 1
			contador = 1
			for tag in smonitor.Tags:
				if tag.name != "-----------------FREE-----------------":
					enviar = enviar + "{" + "\"nome\"" + ":" "\"" + tag.name + "\"" + ","
					enviar = enviar + "\"valor\"" + ":" "\"" + str(tag.value) + "\"" + ","
					enviar = enviar + "\"indice\"" + ":" "\"" + str(tag.index) + "\"" + "}"
					if contador != valores_nao_nulos:
						enviar = enviar + ","
					else:
						enviar = enviar + "]"
					contador += 1
			return enviar
		except Exception, e:
			return str(e)


if __name__ == '__main__':
	webserver.run(debug=False, host='0.0.0.0', port=80, use_reloader=False)

