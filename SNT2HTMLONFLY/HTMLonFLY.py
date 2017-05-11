# -*- coding: utf-8 -*-

import struct
import os.path
from PIL import Image
from moviepy.editor import *
import imageio
import cherrypy
import SMComm


class INICIO(object):
	@cherrypy.expose
	def index(self):
		return "<html><head></head><body>Hello world!</body></html>"


if __name__=="__main__":
	cherrypy.config.update({'server.socket_port': 80})
	cherrypy.quickstart(INICIO())
