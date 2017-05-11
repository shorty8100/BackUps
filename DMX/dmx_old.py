# -*- coding: utf-8 -*-

import sys, socket, math, time
from ctypes import *
import SMComm
import os.path

__author__ = "Micael Martins"
__copyright__ = "Copyright 2017, Itelmatis"
__credits__ = ["Micael Martins"]
__version__ = "v0.1 - Python2.7"
__maintainer__ = "Micael Martins"
__email__ = "MicaelMartins@itelmatis.com"
__status__ = "Under Development"

hostIP = "10.7.191.194"
QuantidadeLampadas = 100

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

class Lampada:
	def __init__(self, Cor):
		self.R = MapaCores[Cor]["R"]
		self.G = MapaCores[Cor]["G"]
		self.B = MapaCores[Cor]["B"]

def main():
	diretoriaPRT = "C:\\S-Monitor\\DMX"
	Tags = []
	Lampadas = []
	relacaoCores = []

	try:
		ficheiro = open(r"C:\S-Monitor\Lamp Quarto 101 Cor.var","w")
		contador = 0
		for var in MapaCores:
			if contador == 0:
				ficheiro.write(str(round(contador,1)).replace(".", ",") + "=" + "Desligado" + "\n")
				relacaoCores.append("Desligado")
				contador += 1
			if var != "Desligado":
				ficheiro.write(str(round(contador,1)).replace(".", ",") + "=" + var + "\n")
				relacaoCores.append(var)
				contador += 1
		ficheiro.close()
	except:
		pass

	try:
		if not os.path.exists(diretoriaPRT):
			os.makedirs(diretoriaPRT)
		if('smonitor' not in locals()):
			for ID in range(0, QuantidadeLampadas):
				nome = "Lampada ID " + str(ID)
				Tags.append(SMComm.Tag(nome, 0))
			smonitor = SMComm.SMServer(Tags, diretoriaPRT + "\\DMX.prt")
	except:
		pass

	for index in range(0, QuantidadeLampadas):
		Lampadas.append(Lampada("Ciano"))

	ENTTEC = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	packet = ArtNetDMXOut()

	while True:
		contador = 0
		for var in range(0, QuantidadeLampadas - 3, 3):
			packet.payload[var] = Lampadas[contador].R
			contador += 1
			packet.payload[var + 1] = Lampadas[contador].G
			contador += 1
			packet.payload[var + 2] = Lampadas[contador].B
			contador += 1
		ENTTEC.sendto(packet, (hostIP, ArtNetDMXOut.PORT))
		print "enviou"
		time.sleep(0.1)


if __name__ == "__main__":
	main()
