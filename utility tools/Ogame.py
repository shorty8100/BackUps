import pyautogui
import time
from threading import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import *
import sys
import datetime
from datetime import date


__author__ = "Micael Martins"
__copyright__ = "Copyright 2017"
__credits__ = ["Micael Martins"]
__version__ = "0.1"
__maintainer__ = "Micael Martins"
__email__ = "micaelmartins.sh@gmail.com"
__status__ = "Finished"
__description__ = "Prime teclas automaticamente"


Planetas = {
	'Planeta1':{'X' : 1100, 'Y' : 225},
	'Planeta2':{'X' : 1100, 'Y' : 335},
	'Planeta3':{'X' : 1100, 'Y' : 435},
	'Planeta4':{'X' : 1100, 'Y' : 525},
	'Planeta5':{'X' : 1100, 'Y' : 620}}

Confirmacao = {'OK':{'X' : 925, 'Y' : 255}}

Menus = {
	'Resumo':{'X' : 245, 'Y' : 195},
	'Recursos':{'X' : 245, 'Y' : 223},
	'Instalacoes':{'X' : 245, 'Y' : 250},
	'Mercador':{'X' : 245, 'Y' : 280},
	'Pesquisas':{'X' : 245, 'Y' : 310},
	'Hangar':{'X' : 245, 'Y' : 340},
	'Defesas':{'X' : 245, 'Y' : 370},
	'Frota':{'X' : 245, 'Y' : 400},
	'Galaxia':{'X' : 245, 'Y' : 430},
	'Alianca':{'X' : 245, 'Y' : 455}}


SubMenus = {
	'Metal':{'X' : 415, 'Y' : 580},
	'Cristal':{'X' : 525, 'Y' : 580},
	'Deuterio':{'X' : 620, 'Y' : 580},
	'Planta':{'X' : 735, 'Y' : 580},
	'Robots':{'X' : 415, 'Y' : 580},
	'Hangar':{'X' : 525, 'Y' : 580},
	'Laboratorio':{'X' : 620, 'Y' : 580},
	'Deposito':{'X' : 735, 'Y' : 580},
	'Silo':{'X' : 835, 'Y' : 580},
	'Nanites':{'X' : 945, 'Y' : 580},
	'Energia':{'X' : 400, 'Y' : 500},
	'Laser':{'X' : 480, 'Y' : 500},
	'Ioes':{'X' : 560, 'Y' : 500},
	'HiperEspaco':{'X' : 635, 'Y' : 500},
	'Plasma':{'X' : 720, 'Y' : 500},
	'MCombustao':{'X' : 820, 'Y' : 500},
	'MImpulsao':{'X' : 885, 'Y' : 500},
	'MHiperEspaco':{'X' : 965, 'Y' : 500},
	'Espionagem':{'X' : 400, 'Y' : 500},
	'Computadores':{'X' : 480, 'Y' : 500},
	'Astrofisica':{'X' : 560, 'Y' : 500},
	'Rede':{'X' : 635, 'Y' : 500},
	'Gravitacao':{'X' : 720, 'Y' : 500},
	'Armas':{'X' : 820, 'Y' : 500},
	'Escudos':{'X' : 885, 'Y' : 500},
	'Blindagem':{'X' : 965, 'Y' : 500}}


def main(args):
	app = QApplication(args)
	app.setStyle("plastique")
	form = MainWindow()
	form.resize(700, 300)
	form.show()
	app.exec_()


class accoes (QThread):
	tempo_restante = pyqtSignal(str)

	def __init__(self, ID, Planeta, Menu, SubMenu, Data, Hora, parent=None):
		super(accoes, self).__init__(parent)
		self.ID = ID
		self.Planeta = Planeta
		self.Menu = Menu
		self.SubMenu = SubMenu
		self.ANO, self.MES, self.DIA = Data.split("-")
		self.HORA, self.MINUTO = Hora.split(":")
		self.TempoEntreClicks = 5
		self.JaCorreu = 0
		#print "Processo:", self.ID, "a correr", "\n"

	def __del__(self):
		self.wait()

	def run(self):
		while True:
			delta = datetime.datetime(int(self.ANO), int(self.MES), int(self.DIA), int(self.HORA), int(self.MINUTO)) - datetime.datetime.now()
			#print "Faltam ", delta.seconds/3600, "h",delta.seconds/60,"m para o processo:",self.ID, "\n"
			time.sleep(1)
			self.tempo_restante.emit(str(delta.seconds / 60) + " minutos")
			if (delta.seconds / 60) == 0 and self.JaCorreu == 0:
				pyautogui.click(x=Planetas[self.Planeta]["X"], y=Planetas[self.Planeta]["Y"])
				#print self.Planeta
				time.sleep(self.TempoEntreClicks)
				pyautogui.click(x=Menus[self.Menu]["X"], y=Menus[self.Menu]["Y"])
				#print self.Menu
				time.sleep(self.TempoEntreClicks)
				pyautogui.click(x=SubMenus[self.SubMenu]["X"], y=SubMenus[self.SubMenu]["Y"])
				#print self.SubMenu
				time.sleep(self.TempoEntreClicks)
				pyautogui.click(x=Confirmacao["OK"]["X"], y=Confirmacao["OK"]["Y"])
				time.sleep(self.TempoEntreClicks)
				self.JaCorreu = 1
				#print "Fim"
				#self.terminate()
				#terminate()


class Conteudo(QWidget):
	def __init__(self, parent=None):
		super(Conteudo, self).__init__(parent)

		#self.botao = QPushButton("Executa")
		self.botao2 = QPushButton("Fechar")
		self.adicionar1 = QPushButton("Iniciar")
		self.adicionar2 = QPushButton("Iniciar")
		self.adicionar3 = QPushButton("Iniciar")
		self.adicionar4 = QPushButton("Iniciar")
		self.adicionar5 = QPushButton("Iniciar")
		self.adicionar6 = QPushButton("Iniciar")
		self.remover1 = QPushButton("Parar")
		self.remover2 = QPushButton("Parar")
		self.remover3 = QPushButton("Parar")
		self.remover4 = QPushButton("Parar")
		self.remover5 = QPushButton("Parar")
		self.remover6 = QPushButton("Parar")
		self.restante1 = QLabel("*** minutos")
		self.restante2 = QLabel("*** minutos")
		self.restante3 = QLabel("*** minutos")
		self.restante4 = QLabel("*** minutos")
		self.restante5 = QLabel("*** minutos")
		self.restante6 = QLabel("*** minutos")
		Label1 = QLabel("")
		self.LabelInformativa = QLabel()
		self.quantidade = QComboBox()
		self.Planeta1 = QComboBox()
		self.Planeta2 = QComboBox()
		self.Planeta3 = QComboBox()
		self.Planeta4 = QComboBox()
		self.Planeta5 = QComboBox()
		self.Planeta6 = QComboBox()
		self.Menu1 = QComboBox()
		self.Menu2 = QComboBox()
		self.Menu3 = QComboBox()
		self.Menu4 = QComboBox()
		self.Menu5 = QComboBox()
		self.Menu6 = QComboBox()
		self.SubMenu1 = QComboBox()
		self.SubMenu2 = QComboBox()
		self.SubMenu3 = QComboBox()
		self.SubMenu4 = QComboBox()
		self.SubMenu5 = QComboBox()
		self.SubMenu6 = QComboBox()
		self.data1 = QLineEdit(str(date.today()))
		self.data2 = QLineEdit(str(date.today()))
		self.data3 = QLineEdit(str(date.today()))
		self.data4 = QLineEdit(str(date.today()))
		self.data5 = QLineEdit(str(date.today()))
		self.data6 = QLineEdit(str(date.today()))
		self.horas1 = QLineEdit("HH:MM")
		self.horas2 = QLineEdit("HH:MM")
		self.horas3 = QLineEdit("HH:MM")
		self.horas4 = QLineEdit("HH:MM")
		self.horas5 = QLineEdit("HH:MM")
		self.horas6 = QLineEdit("HH:MM")

		Comando1 = QHBoxLayout()
		Comando2 = QHBoxLayout()
		Comando3 = QHBoxLayout()
		Comando4 = QHBoxLayout()
		Comando5 = QHBoxLayout()
		Comando6 = QHBoxLayout()
		butoes = QHBoxLayout()
		labeles = QHBoxLayout()
		informacao = QHBoxLayout()
		final = QVBoxLayout()

		Comando1.addWidget(self.Planeta1)
		Comando1.addWidget(self.Menu1)
		Comando1.addWidget(self.SubMenu1)
		Comando1.addStretch(1)
		Comando1.addWidget(self.data1)
		Comando1.addStretch(1)
		Comando1.addWidget(self.horas1)
		Comando1.addStretch(1)
		Comando1.addWidget(self.adicionar1)
		Comando1.addStretch(1)
		Comando1.addWidget(self.remover1)
		Comando1.addStretch(1)
		Comando1.addWidget(self.restante1)

		Comando2.addWidget(self.Planeta2)
		Comando2.addWidget(self.Menu2)
		Comando2.addWidget(self.SubMenu2)
		Comando2.addStretch(1)
		Comando2.addWidget(self.data2)
		Comando2.addStretch(1)
		Comando2.addWidget(self.horas2)
		Comando2.addStretch(1)
		Comando2.addWidget(self.adicionar2)
		Comando2.addStretch(1)
		Comando2.addWidget(self.remover2)
		Comando2.addStretch(1)
		Comando2.addWidget(self.restante2)
		Comando3.addWidget(self.Planeta3)
		Comando3.addWidget(self.Menu3)
		Comando3.addWidget(self.SubMenu3)
		Comando3.addStretch(1)
		Comando3.addWidget(self.data3)
		Comando3.addStretch(1)
		Comando3.addWidget(self.horas3)
		Comando3.addStretch(1)
		Comando3.addWidget(self.adicionar3)
		Comando3.addStretch(1)
		Comando3.addWidget(self.remover3)
		Comando3.addStretch(1)
		Comando3.addWidget(self.restante3)
		Comando4.addWidget(self.Planeta4)
		Comando4.addWidget(self.Menu4)
		Comando4.addWidget(self.SubMenu4)
		Comando4.addStretch(1)
		Comando4.addWidget(self.data4)
		Comando4.addStretch(1)
		Comando4.addWidget(self.horas4)
		Comando4.addStretch(1)
		Comando4.addWidget(self.adicionar4)
		Comando4.addStretch(1)
		Comando4.addWidget(self.remover4)
		Comando4.addStretch(1)
		Comando4.addWidget(self.restante4)
		Comando5.addWidget(self.Planeta5)
		Comando5.addWidget(self.Menu5)
		Comando5.addWidget(self.SubMenu5)
		Comando5.addStretch(1)
		Comando5.addWidget(self.data5)
		Comando5.addStretch(1)
		Comando5.addWidget(self.horas5)
		Comando5.addStretch(1)
		Comando5.addWidget(self.adicionar5)
		Comando5.addStretch(1)
		Comando5.addWidget(self.remover5)
		Comando5.addStretch(1)
		Comando5.addWidget(self.restante5)
		Comando6.addWidget(self.Planeta6)
		Comando6.addWidget(self.Menu6)
		Comando6.addWidget(self.SubMenu6)
		Comando6.addStretch(1)
		Comando6.addWidget(self.data6)
		Comando6.addStretch(1)
		Comando6.addWidget(self.horas6)
		Comando6.addStretch(1)
		Comando6.addWidget(self.adicionar6)
		Comando6.addStretch(1)
		Comando6.addWidget(self.remover6)
		Comando6.addStretch(1)
		Comando6.addWidget(self.restante6)

		#butoes.addWidget(self.botao)
		butoes.addWidget(self.botao2)
		informacao.addWidget(Label1)
		informacao.addWidget(self.LabelInformativa)
		final.addLayout(Comando1)
		final.addLayout(Comando2)
		final.addLayout(Comando3)
		final.addLayout(Comando4)
		final.addLayout(Comando5)
		final.addLayout(Comando6)
		final.addLayout(butoes)
		final.addLayout(labeles)
		final.addLayout(informacao)
		self.setLayout(final)
		self.load()

	def load(self):
		listaplanetas = []
		listamenus = []
		listasubmenus = []
		for aaa in Planetas:
			listaplanetas.append(aaa)
		self.Planeta1.addItems(listaplanetas)
		self.Planeta2.addItems(listaplanetas)
		self.Planeta3.addItems(listaplanetas)
		self.Planeta4.addItems(listaplanetas)
		self.Planeta5.addItems(listaplanetas)
		self.Planeta6.addItems(listaplanetas)
		for bbb in Menus:
			listamenus.append(bbb)
		self.Menu1.addItems(listamenus)
		self.Menu2.addItems(listamenus)
		self.Menu3.addItems(listamenus)
		self.Menu4.addItems(listamenus)
		self.Menu5.addItems(listamenus)
		self.Menu6.addItems(listamenus)
		for ccc in SubMenus:
			listasubmenus.append(ccc)
		self.SubMenu1.addItems(listasubmenus)
		self.SubMenu2.addItems(listasubmenus)
		self.SubMenu3.addItems(listasubmenus)
		self.SubMenu4.addItems(listasubmenus)
		self.SubMenu5.addItems(listasubmenus)
		self.SubMenu6.addItems(listasubmenus)
		self.remover1.setEnabled(False)
		self.remover2.setEnabled(False)
		self.remover3.setEnabled(False)
		self.remover4.setEnabled(False)
		self.remover5.setEnabled(False)
		self.remover6.setEnabled(False)


class MainWindow(QMainWindow):
	def __init__(self, parent=None):

		QMainWindow.__init__(self)
		self.mainWidget = QWidget(self)

		exitAction = QAction(("&Sair"), self)
		#exitAction.setShortcut('ESC')
		exitAction.setStatusTip(("Sair da aplicacao"))
		exitAction.triggered.connect(qApp.quit)

		#menubar = self.menuBar()
		layoutfixo = QHBoxLayout(self.mainWidget)
		self.conteudo = Conteudo()
		layoutfixo.addWidget(self.conteudo)
		self.conteudo.adicionar1.clicked.connect(self.click1)
		self.conteudo.remover1.clicked.connect(self.End1)
		self.conteudo.adicionar2.clicked.connect(self.click2)
		self.conteudo.remover2.clicked.connect(self.End2)
		self.conteudo.adicionar3.clicked.connect(self.click3)
		self.conteudo.remover3.clicked.connect(self.End3)
		self.conteudo.adicionar4.clicked.connect(self.click4)
		self.conteudo.remover4.clicked.connect(self.End4)
		self.conteudo.adicionar5.clicked.connect(self.click5)
		self.conteudo.remover5.clicked.connect(self.End5)
		self.conteudo.adicionar6.clicked.connect(self.click6)
		self.conteudo.remover6.clicked.connect(self.End6)
		self.conteudo.botao2.clicked.connect(self.terminar)
		#self.conteudo.atualizar.clicked.connect(self.clicka)
		self.mainWidget.setLayout(layoutfixo)
		self.setCentralWidget(self.mainWidget)
		#self.setGeometry(500, 500, 600, 600)
		self.setWindowTitle("OGame BOT v0.1 Beta for ELEMENTS by ShOrTy")
		self.setWindowIcon(QtGui.QIcon('brand.ico'))
		self.statusBar().showMessage(("Arrancou!"))
		#self.setWindowFlags(Qt.FramelessWindowHint) #tira a frame da janela na totalidade
		#self.setWindowFlags(Qt.WindowTitleHint) # remove minimizar, maximizar e desabilita o fechar

	def click1(self):
		self.processo1 = accoes(0, self.conteudo.Planeta1.currentText(), self.conteudo.Menu1.currentText(), self.conteudo.SubMenu1.currentText(), self.conteudo.data1.text(), self.conteudo.horas1.text())
		self.processo1.tempo_restante.connect(self.info1)
		self.processo1.start()
		self.conteudo.adicionar1.setEnabled(False)
		self.conteudo.remover1.setEnabled(True)
		self.statusBar().showMessage(("Em execucao accao 1"))

	def End1(self):
		self.processo1.terminate()
		self.conteudo.adicionar1.setEnabled(True)
		self.conteudo.remover1.setEnabled(False)
		self.statusBar().showMessage(("Terminou accao 1"))

	def info1(self, texto):
		#self.merdas.valor.setText(str(texto))
		self.conteudo.restante1.setText(texto)

	def click2(self):
		self.processo2 = accoes(0, self.conteudo.Planeta2.currentText(), self.conteudo.Menu2.currentText(), self.conteudo.SubMenu2.currentText(), self.conteudo.data2.text(), self.conteudo.horas2.text())
		self.processo2.tempo_restante.connect(self.info2)
		self.processo2.start()
		self.conteudo.adicionar2.setEnabled(False)
		self.conteudo.remover2.setEnabled(True)
		self.statusBar().showMessage(("Em execucao accao 2"))

	def End2(self):
		self.processo2.terminate()
		self.conteudo.adicionar2.setEnabled(True)
		self.conteudo.remover2.setEnabled(False)
		self.statusBar().showMessage(("Terminou accao 2"))

	def info2(self, texto):
		#self.merdas.valor.setText(str(texto))
		self.conteudo.restante2.setText(texto)

	def click3(self):
		self.processo3 = accoes(0, self.conteudo.Planeta3.currentText(), self.conteudo.Menu3.currentText(), self.conteudo.SubMenu3.currentText(), self.conteudo.data3.text(), self.conteudo.horas3.text())
		self.processo3.tempo_restante.connect(self.info3)
		self.processo3.start()
		self.conteudo.adicionar3.setEnabled(False)
		self.conteudo.remover3.setEnabled(True)
		self.statusBar().showMessage(("Em execucao accao 3"))

	def End3(self):
		self.processo3.terminate()
		self.conteudo.adicionar3.setEnabled(True)
		self.conteudo.remover3.setEnabled(False)
		self.statusBar().showMessage(("Terminou accao 3"))

	def info3(self, texto):
		#self.merdas.valor.setText(str(texto))
		self.conteudo.restante3.setText(texto)

	def click4(self):
		self.processo4 = accoes(0, self.conteudo.Planeta4.currentText(), self.conteudo.Menu4.currentText(), self.conteudo.SubMenu4.currentText(), self.conteudo.data4.text(), self.conteudo.horas4.text())
		self.processo4.tempo_restante.connect(self.info4)
		self.processo4.start()
		self.conteudo.adicionar4.setEnabled(False)
		self.conteudo.remover4.setEnabled(True)
		self.statusBar().showMessage(("Em execucao accao 4"))

	def End4(self):
		self.processo4.terminate()
		self.conteudo.adicionar4.setEnabled(True)
		self.conteudo.remover4.setEnabled(False)
		self.statusBar().showMessage(("Terminou accao 4"))

	def info4(self, texto):
		#self.merdas.valor.setText(str(texto))
		self.conteudo.restante4.setText(texto)

	def click5(self):
		self.processo5 = accoes(0, self.conteudo.Planeta5.currentText(), self.conteudo.Menu5.currentText(), self.conteudo.SubMenu5.currentText(), self.conteudo.data5.text(), self.conteudo.horas5.text())
		self.processo5.tempo_restante.connect(self.info5)
		self.processo5.start()
		self.conteudo.adicionar5.setEnabled(False)
		self.conteudo.remover5.setEnabled(True)
		self.statusBar().showMessage(("Em execucao accao 5"))

	def End5(self):
		self.processo5.terminate()
		self.conteudo.adicionar5.setEnabled(True)
		self.conteudo.remover5.setEnabled(False)
		self.statusBar().showMessage(("Terminou accao 5"))

	def info5(self, texto):
		#self.merdas.valor.setText(str(texto))
		self.conteudo.restante5.setText(texto)

	def click6(self):
		self.processo6 = accoes(0, self.conteudo.Planeta6.currentText(), self.conteudo.Menu6.currentText(), self.conteudo.SubMenu6.currentText(), self.conteudo.data6.text(), self.conteudo.horas6.text())
		self.processo6.tempo_restante.connect(self.info6)
		self.processo6.start()
		self.conteudo.adicionar6.setEnabled(False)
		self.conteudo.remover6.setEnabled(True)
		self.statusBar().showMessage(("Em execucao accao 6"))

	def End6(self):
		self.processo6.terminate()
		self.conteudo.adicionar6.setEnabled(True)
		self.conteudo.remover6.setEnabled(False)
		self.statusBar().showMessage(("Terminou accao 6"))

	def info6(self, texto):
		#self.merdas.valor.setText(str(texto))
		self.conteudo.restante6.setText(texto)


	def terminar(self):
		try:
			self.processo1.terminate()
			self.processo2.terminate()
			self.processo3.terminate()
			self.processo4.terminate()
			self.processo5.terminate()
			self.processo6.terminate()
		except:
			pass
		qApp.quit()



if __name__ == "__main__":
	main(sys.argv)