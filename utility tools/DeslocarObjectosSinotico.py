from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import *
import webbrowser
import sys
import os
import time
import pickle
import smtplib
import mimetypes
import email
import email.mime.application
from datetime import datetime

def main(args):
	app = QApplication(args)
	app.setStyle("plastique")
	form = MainWindow()
	form.resize(300,100)
	form.show()
	app.exec_()
    
class Conteudo(QWidget):
	def __init__(self, parent=None):
		super(Conteudo, self).__init__(parent)
		LabelOrigem = QLabel("Origem (.csv): ")
		LabelDestino = QLabel("Destino (.csv): ")
		LabelOrigemX = QLabel("X Origem:")
		LabelOrigemY = QLabel("Y Origem:")
		LabelDestinoX = QLabel("X Destino:")
		LabelDestinoY = QLabel("Y Destino:")
				
		self.CaminhoOrigem = QLineEdit()
		self.CaminhoDestino = QLineEdit()
		self.XOrigem = QLineEdit()
		self.YOrigem = QLineEdit()
		self.XDestino = QLineEdit()
		self.YDestino = QLineEdit()
				
		self.butao = QPushButton("Corrigir")
				
		Origem = QHBoxLayout()
		Dados = QHBoxLayout()
		Destino = QHBoxLayout()
		final = QVBoxLayout()
				
		Origem.addWidget(LabelOrigem)
		Origem.addWidget(self.CaminhoOrigem)
		Dados.addWidget(LabelOrigemX)
		Dados.addWidget(self.XOrigem)
		Dados.addWidget(LabelOrigemY)
		Dados.addWidget(self.YOrigem)
		Dados.addWidget(LabelDestinoX)
		Dados.addWidget(self.XDestino)
		Dados.addWidget(LabelDestinoY)
		Dados.addWidget(self.YDestino)
		Destino.addWidget(LabelDestino)
		Destino.addWidget(self.CaminhoDestino)
				
		final.addLayout(Origem)
		final.addLayout(Dados)
		final.addLayout(Destino)
		final.addWidget(self.butao)
		self.setLayout(final)
	
	def funcao(self):
		coordenadas_raw = []
		coordenadasX = [] #coordenadasX[0] Origem || coordenadasX[1] Destino
		coordenadasY = [] #coordenadasY[0] Origem || coordenadasY[1] Destino
		coordenadas_dif = [] #diferenca entre as coordenadas X2 - X1 || Y2 - Y1
		filename = self.CaminhoOrigem.text()
		coordenadasX.append(self.XOrigem.text())
		coordenadasY.append(self.YOrigem.text())
		coordenadasX.append(self.XDestino.text())
		coordenadasY.append(self.YDestino.text())
		newfilename = self.CaminhoDestino.text()
		if (coordenadasX[0] <= coordenadasX[1]) and (coordenadasY[0] <= coordenadasY[1]):
			coordenadas_dif.append(int(coordenadasX[0]) - int(coordenadasX[1]))
			coordenadas_dif.append(int(coordenadasY[0]) - int(coordenadasY[1]))
		else:
			pass
		conteudo_ficheiro_raw = open(filename).read()
		conteudo_ficheiro = []
		contador = 0
		for c in conteudo_ficheiro_raw.split("\n"):
			conteudo_ficheiro.append(c)
			if "Link;" in c:
				primeiraConfig = contador
			elif "OBJ;" in c:
				segundaConfig = contador
			else:
				pass
			contador += 1
		contador = 0
		for d in conteudo_ficheiro[primeiraConfig].split(";"):
			if "Xi" in d:
				Xi = contador
			elif "Yi" in d:
				Yi = contador
			elif "Xf" in d:
				Xf = contador
			elif "Yf" in d:
				Yf = contador
			else:
				pass
			contador += 1
		contador = 0
		for e in conteudo_ficheiro[segundaConfig].split(";"):
			if "X" in e:
				X = contador
			elif "Y" in e:
				Y = contador
			else:
				pass
			contador += 1
		#processa o primeiro bloco
		for f in xrange(segundaConfig - primeiraConfig -1):
			conteudo_linha = []
			for g in conteudo_ficheiro[primeiraConfig + f + 1].split(";"):
				conteudo_linha.append(g)
			int_valorXi = int(conteudo_linha[Xi])
			int_valorYi = int(conteudo_linha[Yi])
			int_valorXf = int(conteudo_linha[Xf])
			int_valorYf = int(conteudo_linha[Yf])
			nova_linha = ""
			if int_valorXi < coordenadas_dif[0] or int_valorYi < coordenadas_dif[1]:
				pass
			else:
				novo_valorXi = int_valorXi - coordenadas_dif[0]
				novo_valorYi = int_valorYi - coordenadas_dif[1]
				novo_valorXf = int_valorXf - coordenadas_dif[0]
				novo_valorYf = int_valorYf - coordenadas_dif[1]
				conteudo_linha[Xi] = str(novo_valorXi)
				conteudo_linha[Yi] = str(novo_valorYi)
				conteudo_linha[Xf] = str(novo_valorXf)
				conteudo_linha[Yf] = str(novo_valorYf)
			for k in xrange(len(conteudo_linha) - 1):
				nova_linha = nova_linha + conteudo_linha[k] + ";"
			conteudo_ficheiro[primeiraConfig + f + 1] = nova_linha
		for h in xrange(len(conteudo_ficheiro) - segundaConfig - 2):
			conteudo_linha = []
			for i in conteudo_ficheiro[segundaConfig + h + 1].split(";"):
				conteudo_linha.append(i)
			int_valorX = int(conteudo_linha[X])
			int_valorY = int(conteudo_linha[Y])
			nova_linha = ""
			if int_valorX < coordenadas_dif[0] or int_valorY < coordenadas_dif[1]:
				pass
			else:
				novo_valorX = int_valorX - coordenadas_dif[0]
				novo_valorY = int_valorY - coordenadas_dif[1]
				conteudo_linha[X] = str(novo_valorX)
				conteudo_linha[Y] = str(novo_valorY)
			for j in xrange(len(conteudo_linha) - 1):
				nova_linha = nova_linha + conteudo_linha[j] + ";"
			conteudo_ficheiro[segundaConfig + h + 1] = nova_linha
		temporario = open(newfilename,"a")
		for fim in xrange(len(conteudo_ficheiro) - 1):
			temporario.write(conteudo_ficheiro[fim])
			temporario.write("\n")
		temporario.close()


class MainWindow(QMainWindow):
	def __init__(self, parent=None):

		QMainWindow.__init__(self)
		self.mainWidget = QWidget(self)
		
		exitAction = QAction(("&Sair"), self)
		exitAction.setShortcut('ESC')
		exitAction.setStatusTip(("Sair da aplicacao"))
		exitAction.triggered.connect(qApp.quit)
     
		autorAction = QAction("&Autor", self)
		autorAction.setStatusTip(("FB do Autor"))
		autorAction.triggered.connect(self.abre_FB)

		menubar = self.menuBar()
		ExitMenu = menubar.addMenu("Sair")
		AboutMenu = menubar.addMenu("Sobre")
		AboutMenu.addAction(autorAction)
		ExitMenu.addAction(exitAction)
		
		layoutfixo = QHBoxLayout(self.mainWidget)
		self.conteudo = Conteudo()
		layoutfixo.addWidget(self.conteudo)
		
		self.conteudo.butao.clicked.connect(self.corre)
		
		self.mainWidget.setLayout(layoutfixo)
		self.setCentralWidget(self.mainWidget)
		self.setWindowTitle("CoKas v1.1 Alpha")
		self.setWindowIcon(QtGui.QIcon('brand.ico'))
		self.statusBar().showMessage(("Hello! Program is ready!"))
	
	
	def abre_FB(self):
		webbrowser.open("https://www.facebook.com/micael.martins.8100")
	
	def corre(self):
		try:
			self.conteudo.funcao()
			self.statusBar().showMessage(("Done!"))
		except IOError:
			self.statusBar().showMessage(("ERRO! Ficheiro de entrada nao encontrado"))


if __name__=="__main__":
    main(sys.argv)
