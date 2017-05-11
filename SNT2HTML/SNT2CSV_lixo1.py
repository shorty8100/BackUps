# -*- coding: utf-8 -*-

import struct
import sys

#print (conteudo)
#print (conteudo[0:1])
#print (struct.unpack("c", conteudo[0:1])[0].decode("utf-8"))
#print (struct.unpack("c" * 500, conteudo[1:501]))

with open("MenuPrincipal.snt","rb") as ficheiro:
	conteudo = ficheiro.read()

FileContent = []
temporario = ""
emptyCounter = 0

print(struct.unpack("c" * (len(conteudo)), conteudo))
#while(1):
#	pass

for byte in struct.unpack("c" * (len(conteudo)), conteudo):
	if byte is b"\x00":
		emptyCounter += 1
	elif byte is not b"\x00" and emptyCounter < 2:
		temporario += byte.decode("iso-8859-1")
	elif byte.decode("iso-8859-1") is "#":
		temporario += byte.decode("iso-8859-1")
		emptyCounter = 0
	elif byte is not b"\x00" and emptyCounter > 2:
		pass
	else:
		pass

#print (temporario)

for a in temporario.split("#"):
	print(a)
