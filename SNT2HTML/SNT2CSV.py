# -*- coding: utf-8 -*-

import struct
import os.path
from PIL import Image
from moviepy.editor import *

__author__ = "Micael Martins"
__copyright__ = "Copyright 2017, Itelmatis"
__credits__ = ["Rui Palma"]
__version__ = "0.1"
__maintainer__ = "Micael Martins"
__email__ = "MicaelMartins@itelmatis.com"
__status__ = "Under Development"

class Objeto:
	def __init__(self):
		self.Tipo = 0
		self.Nome = ""
		self.Variavel = 0
		self.IndexObjecto = 0
		self.Digital = False
		self.x = 0
		self.y = 0
		self.TextoOn = ""
		self.TextoOff = ""
		self.Largura = 0
		self.Altura = 0
		self.ImagemBotao = ""
		self.ImagemPosicaoBotao = 0
		self.Ficheiro = ""
		self.TipoDeAnimacao = 0
		self.VariavelMin = 0
		self.VariavelMax = 100
		self.SeparadorDeMilhares = False
		self.Texto = ""
		self.Contorno = 0
		self.TipoDeLetraNome = ""
		self.TipoDeLetraTamanho = 9
		self.TipoDeLetraCor = 0
		self.TipoDeLetraBold = False
		self.TipoDeLetraItalico = False
		self.TipoDeLetraSublinhado = False
		self.CorDoFundo = 0
		self.Enable = True
		self.SomOn = ""
		self.SomOff = ""
		self.CasaDecimal = True

class Sinoptico:
	def __init__(self):
		self.offset = 0
		self.ImagemFundo = ""
		self.x = 0
		self.y = 0
		self.Nome = ""
		self.Ficheiro = ""
		self.QuantidadeTipo = []
		self.LinkXi = []
		self.LinkYi = []
		self.LinkXf = []
		self.LinkYf = []
		self.LinkFicheiro = []
		self.GraficoEm3D = False
		self.GraficoVariaveis = []
		self.GraficoCores = []
		self.GraficoZoom = 0
		self.GraficoSeguirRegistos = False
		self.GraficoOrtogonal = False
		self.GraficoRotacaoH = 0
		self.GraficoRotacaoV = 0
		self.GraficoProfundidade = 0
		self.GraficoLargura = 0
		self.GraficoAltura = 0
		self.GraficoTop = 0
		self.GraficoLeft = 0
		self.GraficoVisivel = False
		self.GraficoMaximizado = False
		self.Sinoptico = ""
		self.LinkImagem = []
		self.GraficoVerBarra = False
		self.VariavelDeAcesso = 0
		self.FicheiroGrafico = ""
		self.Versao = ""
		self.objeto = []

	def carregarSNT(self,nomeFicheiro, idioma = "01"):
		caminho , self.nomeFicheiro = os.path.split(nomeFicheiro)
		nome , extensao = self.nomeFicheiro.split(".")
		try:
			ficheiro = open(nomeFicheiro,"rb")
			self.conteudo = ficheiro.read()
			ficheiro.close()
			idiomas = nome + " " + idioma + ".csv"
			if os.path.isfile(caminho + "/" + idiomas):
				ficheiro_idiomas = open(caminho + "/" + idiomas,"r")
				self.conteudoIdiomas = ficheiro_idiomas.read()
				ficheiro_idiomas.close()
				self.load_snt()
			else:
				print ("Ficheiro não existe!")
		except:
			print("Falhou o carregamento do ficheiro")

	def load_snt(self):
		try:
			self.Nome = str(struct.unpack_from("100s", self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1"))
			self.offset = 100
			self.Versao = str(struct.unpack_from("10s", self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1"))
			self.offset += 10
			self.ImagemFundo = str(struct.unpack_from("500s", self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1"))
			self.offset += 500
			self.x = struct.unpack_from("i", self.conteudo, self.offset)[0]
			self.offset += 4
			self.y = struct.unpack_from("i", self.conteudo, self.offset)[0]
			self.offset += 4
			self.Nome = str(struct.unpack_from("100s", self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1"))
			self.offset += 100
			self.Ficheiro = str(struct.unpack_from("500s", self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1"))
			self.offset += 500
			self.QuantidadeTipo.append(struct.unpack_from("i", self.conteudo, self.offset)[0])
			self.offset += 4
			self.QuantidadeTipo.append(struct.unpack_from("i", self.conteudo, self.offset)[0])
			self.offset += 4
			self.QuantidadeTipo.append(struct.unpack_from("i", self.conteudo, self.offset)[0])
			self.offset += 4
			self.QuantidadeTipo.append(struct.unpack_from("i", self.conteudo, self.offset)[0])
			self.offset += 4
			for var in range(0, 100):
				self.LinkXi.append(struct.unpack_from("i", self.conteudo, self.offset)[0])
				self.offset += 4
			for var in range(0, 100):
				self.LinkYi.append(struct.unpack_from("i", self.conteudo, self.offset)[0])
				self.offset += 4
			for var in range(0, 100):
				self.LinkXf.append(struct.unpack_from("i", self.conteudo, self.offset)[0])
				self.offset += 4
			for var in range(0, 100):
				self.LinkYf.append(struct.unpack_from("i", self.conteudo, self.offset)[0])
				self.offset += 4
			for var in range(0, 100):
				self.LinkFicheiro.append(str(struct.unpack_from("300s", self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1")))
				self.offset += 300
			self.GraficoEm3D = struct.unpack_from("B", self.conteudo, self.offset)[0]
			self.offset += 4 # ???????
			for var in range(0, 5):
				self.GraficoVariaveis.append(struct.unpack_from("i", self.conteudo, self.offset)[0])
				self.offset += 4
			for var in range(0, 5):
				self.GraficoCores.append(struct.unpack_from("i", self.conteudo, self.offset)[0])
				self.offset += 4
			self.GraficoZoom = struct.unpack_from("i", self.conteudo, self.offset)[0]
			self.offset += 4
			self.GraficoSeguirRegistos = struct.unpack_from("B", self.conteudo, self.offset)[0]
			self.offset += 1# ???????
			self.GraficoOrtogonal = struct.unpack_from("B", self.conteudo, self.offset)[0]
			self.offset += 3# ???????
			self.GraficoRotacaoH = struct.unpack_from('i', self.conteudo, self.offset)[0]
			self.offset += 4
			self.GraficoRotacaoV = struct.unpack_from('i', self.conteudo, self.offset)[0]
			self.offset += 4
			self.GraficoProfundidade = struct.unpack_from('i', self.conteudo, self.offset)[0]
			self.offset += 4
			self.GraficoLargura = struct.unpack_from('i', self.conteudo, self.offset)[0]
			self.offset += 4
			self.GraficoAltura = struct.unpack_from('i', self.conteudo, self.offset)[0]
			self.offset += 4
			self.GraficoTop = struct.unpack_from('i', self.conteudo, self.offset)[0]
			self.offset += 4
			self.GraficoLeft = struct.unpack_from('i', self.conteudo, self.offset)[0]
			self.offset += 4
			self.GraficoVisivel = struct.unpack_from('B', self.conteudo, self.offset)[0]
			self.offset += 1
			self.GraficoMaximizado = struct.unpack_from('B', self.conteudo, self.offset)[0]
			self.offset += 1
			self.Sinoptico = str(struct.unpack_from("500s", self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1"))
			self.offset += 500
			for var in range(0, 100):
				self.LinkImagem.append(str(struct.unpack_from("300s", self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1")))
				self.offset += 300
			self.GraficoVerBarra = struct.unpack_from('B', self.conteudo, self.offset)[0]
			self.offset += 2 # ???????
			self.VariavelDeAcesso = struct.unpack_from('i', self.conteudo, self.offset)[0]
			self.offset += 4
			self.FicheiroGrafico = str(struct.unpack_from("300s", self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1"))
			self.offset += 300
			self.total_de_objetos = self.QuantidadeTipo[0] + self.QuantidadeTipo[1] + self.QuantidadeTipo[2] + self.QuantidadeTipo[3]
			for var in range(0, self.total_de_objetos):
				objet = Objeto()
				objet.Tipo = struct.unpack_from('i', self.conteudo, self.offset)[0]
				self.offset += 4
				objet.Nome = str(struct.unpack_from('51s', self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1"))
				self.offset += 52
				objet.Variavel = struct.unpack_from('i', self.conteudo, self.offset)[0]
				self.offset += 4
				objet.IndexObjecto = struct.unpack_from('i', self.conteudo, self.offset)[0]
				self.offset += 4
				objet.Digital = struct.unpack_from('B', self.conteudo, self.offset)[0]
				self.offset += 4 # ???????
				objet.x = struct.unpack_from('i', self.conteudo, self.offset)[0]
				self.offset += 4
				objet.y = struct.unpack_from('i', self.conteudo, self.offset)[0]
				self.offset += 4
				objet.TextoOn = str(struct.unpack_from('51s', self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1"))
				self.offset += 51
				objet.TextoOff = str(struct.unpack_from('51s', self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1"))
				self.offset += 51
				self.offset += 2 # ???????
				objet.Largura = struct.unpack_from('i', self.conteudo, self.offset)[0]
				self.offset += 4
				objet.Altura = struct.unpack_from('i', self.conteudo, self.offset)[0]
				self.offset += 4
				objet.ImagemBotao = str(struct.unpack_from('500s', self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1"))
				self.offset += 500
				objet.ImagemPosicaoBotao = struct.unpack_from('i', self.conteudo, self.offset)[0]
				self.offset += 4
				objet.Ficheiro = str(struct.unpack_from('500s', self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1"))
				self.offset += 500
				objet.TipoDeAnimacao = struct.unpack_from('i', self.conteudo, self.offset)[0]
				self.offset += 4
				objet.VariavelMin = struct.unpack_from('i', self.conteudo, self.offset)[0]
				self.offset += 4
				objet.VariavelMax = struct.unpack_from('i', self.conteudo, self.offset)[0]
				self.offset += 4
				objet.SeparadorDeMilhares = struct.unpack_from('B', self.conteudo, self.offset)[0]
				self.offset += 1
				objet.Texto = str(struct.unpack_from('101s', self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1"))
				self.offset += 103 # ???????
				objet.Contorno = struct.unpack_from('i', self.conteudo, self.offset)[0]
				self.offset += 4
				objet.TipoDeLetraNome = str(struct.unpack_from('200s', self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1"))
				self.offset += 200
				objet.TipoDeLetraTamanho = struct.unpack_from('i', self.conteudo, self.offset)[0]
				self.offset += 4
				objet.TipoDeLetraCor = struct.unpack_from('i', self.conteudo, self.offset)[0]
				self.offset += 4
				objet.TipoDeLetraBold = struct.unpack_from('B', self.conteudo, self.offset)[0]
				self.offset += 1
				objet.TipoDeLetraItalico = struct.unpack_from('B', self.conteudo, self.offset)[0]
				self.offset += 1
				objet.TipoDeLetraSublinhado = struct.unpack_from('B', self.conteudo, self.offset)[0]
				self.offset += 2 # ???????
				objet.CorDoFundo = struct.unpack_from('i', self.conteudo, self.offset)[0]
				self.offset += 4
				objet.Enable = struct.unpack_from('B', self.conteudo, self.offset)[0]
				self.offset += 1
				objet.SomOn = str(struct.unpack_from('500s', self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1"))
				self.offset += 500
				objet.SomOff = str(struct.unpack_from('500s', self.conteudo, self.offset)[0].split(b'\0',1)[0].decode("iso-8859-1"))
				self.offset += 500
				objet.CasaDecimal = struct.unpack_from('B', self.conteudo, self.offset)[0]
				self.offset += 3 # ???????
				self.objeto.append(objet)
			self.load_idiom()
		except:
			print("Falhou o Parse do Ficheiro")

	def load_idiom(self):
		self.util = {}
		for linhas in self.conteudoIdiomas.split("\n"):
			try:
				index , texto, lixo = linhas.split(";")
				self.util[index] = texto
				#print (index , texto, lixo)
			except:
				#print ("Erro no fim do ficheiro de idiomas")
				pass #crach no fim porque existe "\n" no fim do ficheiro que não contém nenhum tipo de informação -> try resolve o crach
		try:
			self.ImagemFundo = self.util[self.ImagemFundo]
			self.Nome = self.util[self.Nome]
			self.Ficheiro = self.util[self.Ficheiro]
			for var in range(0, 100):
				self.LinkFicheiro[var] = self.util[self.LinkFicheiro[var]]
			self.Sinoptico = self.util[self.Sinoptico]
			for var in range(0, 100):
				self.LinkImagem[var] = self.util[self.LinkImagem[var]]
			self.FicheiroGrafico = self.util[self.FicheiroGrafico]
			for var in range(0, self.total_de_objetos):
				self.objeto[var].Nome = self.util[self.objeto[var].Nome]
				self.objeto[var].TextoOn = self.util[self.objeto[var].TextoOn]
				self.objeto[var].TextoOff = self.util[self.objeto[var].TextoOff]
				self.objeto[var].ImagemBotao = self.util[self.objeto[var].ImagemBotao]
				self.objeto[var].Ficheiro = self.util[self.objeto[var].Ficheiro]
				self.objeto[var].Texto = self.util[self.objeto[var].Texto]
				self.objeto[var].TipoDeLetraNome = self.util[self.objeto[var].TipoDeLetraNome]
				self.objeto[var].SomOn = self.util[self.objeto[var].SomOn]
				self.objeto[var].SomOff = self.util[self.objeto[var].SomOff]
		except:
			print("Falhou a incorporação do ficheiro de idiomas")

	def SAVEasCSV(self):
		directoria = "exportados"
		nomeCSV = directoria + "/" + self.nomeFicheiro + ".csv"
		if not os.path.exists(directoria):
			os.makedirs(directoria)
		tempCSV = ""
		tempCSV += "Name;" + self.Nome + "\n"
		tempCSV += "Versao;" + self.Versao + "\n"
		tempCSV += "BackGround;" + self.ImagemFundo + "\n"
		tempCSV += "X;" + str(self.x) + "\n"
		tempCSV += "Y;" + str(self.y) + "\n"
		tempCSV += "Name;" + self.Nome + "\n"
		tempCSV += "File;" + self.Ficheiro + "\n"
		tempCSV += "Chart W;" + str(self.GraficoLargura) + "\n"
		tempCSV += "Chart H;" + str(self.GraficoAltura) + "\n"
		tempCSV += "Chart Top;" + str(self.GraficoTop) + "\n"
		tempCSV += "Chart Left;" + str(self.GraficoLeft) + "\n"
		tempCSV += "Chart Visible;" + str(self.GraficoVisivel) + "\n"
		tempCSV += "Chart Maximized;" + str(self.GraficoMaximizado) + "\n"
		tempCSV += "Chart File;" + self.FicheiroGrafico + "\n"
		tempCSV += "Sinoptic;" + self.Sinoptico + "\n"
		tempCSV += "Access VAR;" + str(self.VariavelDeAcesso) + "\n"
		tempCSV += "Link;Xi;Yi;Xf;Yf;Dest;Image;" + "\n"
		for var in range(0, 100):
			tempCSV += str(var) + ";"
			tempCSV += str(self.LinkXi[var]) + ";"
			tempCSV += str(self.LinkYi[var]) + ";"
			tempCSV += str(self.LinkXf[var]) + ";"
			tempCSV += str(self.LinkYf[var]) + ";"
			tempCSV += self.LinkFicheiro[var] + ";"
			tempCSV += self.LinkImagem[var] + ";" + "\n"
		tempCSV += "OBJ;Type;Name;VAR;Index;Digital;X;Y;ON Text;OFF Text;Width;Height;Button Image;"
		tempCSV += "Button Image Position;File;Animation Type;Animation Min;Animation Max;Thousands Separator;"
		tempCSV += "Text;Text Border Line;Text Font Name;Text Font Size;Text Font Color;Text Font Bold;Text Font Italic;"
		tempCSV += "Text Font Underlined;Text Background Color;Text Enable/Disable;ON Sound;OFF Sound;Decimal;" + "\n"
		for var in range(0, self.total_de_objetos):
			tempCSV += str(var) + ";"
			tempCSV += str(self.objeto[var].Tipo) + ";"
			tempCSV += self.objeto[var].Nome + ";"
			tempCSV += str(self.objeto[var].Variavel) + ";"
			tempCSV += str(self.objeto[var].IndexObjecto) + ";"
			tempCSV += str(self.objeto[var].Digital) + ";"
			tempCSV += str(self.objeto[var].x) + ";"
			tempCSV += str(self.objeto[var].y) + ";"
			tempCSV += self.objeto[var].TextoOn + ";"
			tempCSV += self.objeto[var].TextoOff + ";"
			tempCSV += str(self.objeto[var].Largura) + ";"
			tempCSV += str(self.objeto[var].Altura) + ";"
			tempCSV += self.objeto[var].ImagemBotao + ";"
			tempCSV += str(self.objeto[var].ImagemPosicaoBotao) + ";"
			tempCSV += self.objeto[var].Ficheiro + ";"
			tempCSV += str(self.objeto[var].TipoDeAnimacao) + ";"
			tempCSV += str(self.objeto[var].VariavelMin) + ";"
			tempCSV += str(self.objeto[var].VariavelMax) + ";"
			tempCSV += str(self.objeto[var].SeparadorDeMilhares) + ";"
			tempCSV += self.objeto[var].Texto + ";"
			tempCSV += str(self.objeto[var].Contorno) + ";"
			tempCSV += self.objeto[var].TipoDeLetraNome + ";"
			tempCSV += str(self.objeto[var].TipoDeLetraTamanho) + ";"
			tempCSV += str(self.objeto[var].TipoDeLetraCor) + ";"
			tempCSV += str(self.objeto[var].TipoDeLetraBold) + ";"
			tempCSV += str(self.objeto[var].TipoDeLetraItalico) + ";"
			tempCSV += str(self.objeto[var].TipoDeLetraSublinhado) + ";"
			tempCSV += str(self.objeto[var].CorDoFundo) + ";"
			tempCSV += str(self.objeto[var].Enable) + ";"
			tempCSV += self.objeto[var].SomOn + ";"
			tempCSV += self.objeto[var].SomOff + ";"
			tempCSV += str(self.objeto[var].CasaDecimal) + ";" + "\n"
		conteudoCSV = open(nomeCSV,"w")
		conteudoCSV.write(tempCSV)
		conteudoCSV.close()

	def SAVEasSNT(self, idioma = "01"):
		tempSNT = bytearray()
		tempIdioma = ""
		index = 0
		tempIndex = "#"
		directoria = "exportados"
		nomeCSV = directoria + "/" + self.nomeFicheiro.split(".", 1)[0] + " " + idioma + ".csv"
		nomeSNT = directoria + "/" + self.nomeFicheiro
		if not os.path.exists(directoria):
			os.makedirs(directoria)
		tempSNT.extend(struct.pack("100s", bytearray(tempIndex + str(index), "iso-8859-1")))
		tempIdioma += tempIndex + str(index) + ";" + self.Nome + ";\n"
		index += 1
		tempSNT.extend(struct.pack("10s", bytearray(self.Versao, "iso-8859-1")))
		tempSNT.extend(struct.pack("500s", bytearray(tempIndex + str(index), "iso-8859-1")))
		tempIdioma += tempIndex + str(index) + ";" + self.ImagemFundo + ";\n"
		index += 1
		tempSNT.extend(struct.pack("i", self.x))
		tempSNT.extend(struct.pack("i", self.y))
		tempSNT.extend(struct.pack("100s", bytearray(tempIndex + str(index), "iso-8859-1")))
		tempIdioma += tempIndex + str(index) + ";" + self.Nome + ";\n"
		index += 1
		tempSNT.extend(struct.pack("500s", bytearray(tempIndex + str(index), "iso-8859-1")))
		tempIdioma += tempIndex + str(index) + ";" + self.Ficheiro + ";\n"
		index += 1
		QuantidadeTipo=[0]*4
		total_de_objs=0
		for obj in self.objeto:
			QuantidadeTipo[obj.Tipo] += 1
			total_de_objs += 1
		tempSNT.extend(struct.pack("4i", *QuantidadeTipo))
		tempSNT.extend(struct.pack("100i", *self.LinkXi))
		tempSNT.extend(struct.pack("100i", *self.LinkYi))
		tempSNT.extend(struct.pack("100i", *self.LinkXf))
		tempSNT.extend(struct.pack("100i", *self.LinkYf))
		for var in range(0,100):
			tempSNT.extend(struct.pack("300s", bytearray(tempIndex + str(index), "iso-8859-1")))
			tempIdioma += tempIndex + str(index) + ";" + self.LinkFicheiro[var] + ";\n"
			index += 1
		tempSNT.extend(struct.pack("B", self.GraficoEm3D))
		tempSNT.extend(struct.pack("3B", *[0x00]*3))
		tempSNT.extend(struct.pack("5i", *self.GraficoVariaveis))
		tempSNT.extend(struct.pack("5i", *self.GraficoCores))
		tempSNT.extend(struct.pack("i", self.GraficoZoom))
		tempSNT.extend(struct.pack("B", self.GraficoSeguirRegistos))
		tempSNT.extend(struct.pack("B", self.GraficoOrtogonal))
		tempSNT.extend(struct.pack("2B", *[0x00]*2))
		tempSNT.extend(struct.pack("i", self.GraficoRotacaoH))
		tempSNT.extend(struct.pack("i", self.GraficoRotacaoV))
		tempSNT.extend(struct.pack("i", self.GraficoProfundidade))
		tempSNT.extend(struct.pack("i", self.GraficoLargura))
		tempSNT.extend(struct.pack("i", self.GraficoAltura))
		tempSNT.extend(struct.pack("i", self.GraficoTop))
		tempSNT.extend(struct.pack("i", self.GraficoLeft))
		tempSNT.extend(struct.pack("B", self.GraficoVisivel))
		tempSNT.extend(struct.pack("B", 0x00))
		tempSNT.extend(struct.pack("500s", bytearray(tempIndex + str(index), "iso-8859-1")))
		tempIdioma += tempIndex + str(index) + ";" + self.Sinoptico + ";\n"
		index += 1
		for var in range(0,100):
			tempSNT.extend(struct.pack("300s", bytearray(tempIndex + str(index), "iso-8859-1")))
			tempIdioma += tempIndex + str(index) + ";" + self.LinkImagem[var] + ";\n"
			index += 1
		tempSNT.extend(struct.pack("B", self.GraficoVerBarra))
		tempSNT.extend(struct.pack("B", 0x00))
		tempSNT.extend(struct.pack("i", self.VariavelDeAcesso))
		tempSNT.extend(struct.pack("300s", bytearray(tempIndex + str(index), "iso-8859-1")))
		tempIdioma += tempIndex + str(index) + ";" + self.FicheiroGrafico + ";\n"
		index += 1
		for obj in self.objeto:
			tempSNT.extend(struct.pack("i", obj.Tipo))
			tempSNT.extend(struct.pack("52s", bytearray(tempIndex + str(index), "iso-8859-1")))
			tempIdioma += tempIndex + str(index) + ";" + obj.Nome + ";\n"
			index += 1
			tempSNT.extend(struct.pack("i", obj.Variavel))
			tempSNT.extend(struct.pack("i", obj.IndexObjecto))
			tempSNT.extend(struct.pack("i", obj.Digital))
			tempSNT.extend(struct.pack("i", obj.x))
			tempSNT.extend(struct.pack("i", obj.y))
			tempSNT.extend(struct.pack("52s", bytearray(tempIndex + str(index), "iso-8859-1")))
			tempIdioma += tempIndex + str(index) + ";" + obj.TextoOn + ";\n"
			index += 1
			tempSNT.extend(struct.pack("52s", bytearray(tempIndex + str(index), "iso-8859-1")))
			tempIdioma += tempIndex + str(index) + ";" + obj.TextoOff + ";\n"
			index += 1
			tempSNT.extend(struct.pack("2B", *[0x00]*2))
			tempSNT.extend(struct.pack("i", obj.Largura))
			tempSNT.extend(struct.pack("i", obj.Altura))
			tempSNT.extend(struct.pack("500s", bytearray(tempIndex + str(index), "iso-8859-1")))
			tempIdioma += tempIndex + str(index) + ";" + obj.ImagemBotao + ";\n"
			index += 1
			tempSNT.extend(struct.pack("i", obj.ImagemPosicaoBotao))
			tempSNT.extend(struct.pack("500s", bytearray(tempIndex + str(index), "iso-8859-1")))
			tempIdioma += tempIndex + str(index) + ";" + obj.Ficheiro + ";\n"
			index += 1
			tempSNT.extend(struct.pack("i", obj.TipoDeAnimacao))
			tempSNT.extend(struct.pack("i", obj.VariavelMin))
			tempSNT.extend(struct.pack("i", obj.VariavelMax))
			tempSNT.extend(struct.pack("B", obj.SeparadorDeMilhares))
			tempSNT.extend(struct.pack("101s", bytearray(tempIndex + str(index), "iso-8859-1")))
			tempIdioma += tempIndex + str(index) + ";" + obj.Texto + ";\n"
			index += 1
			tempSNT.extend(struct.pack("2B", *[0x00]*2))
			tempSNT.extend(struct.pack("i", obj.Contorno))
			tempSNT.extend(struct.pack("200s", bytearray(tempIndex + str(index), "iso-8859-1")))
			tempIdioma += tempIndex + str(index) + ";" + obj.TipoDeLetraNome + ";\n"
			index += 1
			tempSNT.extend(struct.pack("i", obj.TipoDeLetraTamanho))
			tempSNT.extend(struct.pack("i", obj.TipoDeLetraCor))
			tempSNT.extend(struct.pack("B", obj.TipoDeLetraBold))
			tempSNT.extend(struct.pack("B", obj.TipoDeLetraItalico))
			tempSNT.extend(struct.pack("B", obj.TipoDeLetraSublinhado))
			tempSNT.extend(struct.pack("B", 0x00))
			tempSNT.extend(struct.pack("i", obj.CorDoFundo))
			tempSNT.extend(struct.pack("B", obj.Enable))
			tempSNT.extend(struct.pack("500s", bytearray(tempIndex + str(index), "iso-8859-1")))
			tempIdioma += tempIndex + str(index) + ";" + obj.SomOn + ";\n"
			index += 1
			tempSNT.extend(struct.pack("500s", bytearray(tempIndex + str(index), "iso-8859-1")))
			tempIdioma += tempIndex + str(index) + ";" + obj.SomOff + ";\n"
			index += 1
			tempSNT.extend(struct.pack("B", obj.CasaDecimal))
			tempSNT.extend(struct.pack("2B", *[0x00]*2))
		try:
			conteudoSNT = open(nomeSNT,"wb")
			conteudoSNT.write(tempSNT)
			conteudoSNT.close()
		except:
			print("Falhou escrita do SNT")
		try:
			conteudoIdioma = open(nomeCSV,"w")
			conteudoIdioma.write(tempIdioma)
			conteudoIdioma.close()
		except:
			print("Falhou escrita de idioma")

if __name__=="__main__":

	sino = Sinoptico()
	sino.carregarSNT(r"C:\S-Monitor\Files\Main\MenuPrincipal.snt") # Ou sino.abrir("C:\S-Monitor\Files\Main\MenuPrincipal.snt", "01")
	sino.SAVEasCSV()
	sino.SAVEasSNT() # ou sino.SAVEasSNT("01")

