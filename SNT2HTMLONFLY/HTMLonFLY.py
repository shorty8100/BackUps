# -*- coding: utf-8 -*-

import struct
import os.path
from PIL import Image
from moviepy.editor import *
import imageio
import cherrypy
import SMComm

PortaServidor = 80
SinoticoPrincipal = "Files\Main\MenuPrincipal.snt"
SMonitorFolder = "C:\\S-Monitor\\"

class INICIO(object):
	@cherrypy.expose
	def index(self):
		tempHTML = "<html><head></head><body>Hello world!</body></html>"
		return tempHTML


if __name__=="__main__":
	cherrypy.config.update({'server.socket_port': PortaServidor })
	cherrypy.quickstart(INICIO())
