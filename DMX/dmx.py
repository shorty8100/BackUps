# -*- coding: utf-8 -*-

import sys, socket, math, time
from ctypes import *
import SMComm
import os.path

__author__ = "Micael Martins"
__copyright__ = "Copyright 2017, Itelmatis"
__credits__ = ["Micael Martins"]
__version__ = "v1.0 - Python2.7"
__maintainer__ = "Micael Martins"
__email__ = "MicaelMartins@itelmatis.com"
__status__ = "Under Development"

hostIP = "10.7.191.194"
QuantidadeLampadas = 100
CanaisPorLampada = 3
DelayDoCiclo = 0.1

MapaCores = {
			"Desligado": {"R": 0, "G": 0, "B": 0 },
			"Vermelho": {"R": 255, "G": 0, "B": 0 },
			"Laranja": {"R": 255, "G": 127, "B": 0 },
			"Amarelo": {"R": 255, "G": 255, "B": 0 },
			"Verde Lima": {"R": 127, "G": 255, "B": 0 },
			"Verde": {"R": 0, "G": 255, "B": 0 },
			"Verde Azul": {"R": 0, "G": 255, "B": 127 },
			"Ciano": {"R": 0, "G": 255, "B": 255 },
			"Azul Claro": {"R": 0, "G": 127, "B": 255 },
			"Azul": {"R": 0, "G": 0, "B": 255 },
			"Violeta": {"R": 127, "G": 0, "B": 255 },
			"Magenta": {"R": 255, "G": 0, "B": 255 },
			"Rosa": {"R": 255, "G": 0, "B": 127 },
			"Branco": {"R": 255, "G": 255, "B": 255 }
			}

relacaoCores = ["Desligado", "Vermelho", "Laranja",
				"Amarelo", "Verde Lima", "Verde",
				"Verde Azul", "Ciano", "Azul Claro",
				"Azul", "Violeta", "Magenta", "Rosa",
				"Branco"]

class ArtNetDMXOut(LittleEndianStructure):
	PORT = 0x1936
	_fields_ = [("id", c_char * 8),
				("opcode", c_ushort),
				("protverh", c_ubyte),
				("protver", c_ubyte),
				("sequence", c_ubyte),
				("physical", c_ubyte),
				("universe", c_ushort),
				("lengthhi", c_ubyte),
				("length", c_ubyte),
				("payload", c_ubyte * 512)]

	def __init__(self):
		self.id = b"Art-Net"
		self.opcode = 0x5000
		self.protver = 14
		self.universe = 0
		self.lengthhi = 2

def main():
	diretoriaPRT = "C:\\S-Monitor\\DMX"
	Tags = []
	Lampadas = {}
	try:
		if not os.path.exists(diretoriaPRT):
			os.makedirs(diretoriaPRT)
		if('smonitor' not in locals()):
			for ID in range(1, QuantidadeLampadas * CanaisPorLampada, CanaisPorLampada):
				nome = "LampadaAddress " + str(ID)
				Tags.append(SMComm.Tag(nome, 0))
				Lampadas[nome] = 0
			smonitor = SMComm.SMServer(Tags, diretoriaPRT + "\\DMX.prt")
	except:
		pass
	ENTTEC = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	packet = ArtNetDMXOut()
	while True:
		try:
			TagsUpdated = smonitor.Pull()
			while(len(TagsUpdated) > 0):
				Tag = TagsUpdated.pop()
				Lampadas[Tag.name] = int(Tag.value)
			contador = 0
			for ID in range(1, QuantidadeLampadas * CanaisPorLampada, CanaisPorLampada):
					nome = "LampadaAddress " + str(ID)
					if Lampadas[nome] > (len(relacaoCores) - 1):
						Lampadas[nome] = (len(relacaoCores) - 1)
					if Lampadas[nome] < 0:
						Lampadas[nome] = 0
					packet.payload[contador] = MapaCores[relacaoCores[Lampadas[nome]]]["R"]
					packet.payload[contador + 1] = MapaCores[relacaoCores[Lampadas[nome]]]["G"]
					packet.payload[contador + 2] = MapaCores[relacaoCores[Lampadas[nome]]]["B"]
					contador += CanaisPorLampada
			ENTTEC.sendto(packet, (hostIP, ArtNetDMXOut.PORT))
			smonitor.Push()
		except:
			pass
		time.sleep(DelayDoCiclo)


if __name__ == "__main__":
	main()
