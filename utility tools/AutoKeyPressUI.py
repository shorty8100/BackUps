import pyautogui
import time
from threading import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import *
import sys



__author__ = "Micael Martins"
__copyright__ = "Copyright 2017, Itelmatis"
__credits__ = ["Micael Martins"]
__version__ = "0.1"
__maintainer__ = "Micael Martins"
__email__ = "micaelmartins@itelmatis.com"
__status__ = "Finished"
__description__ = "Prime teclas automaticamente"


KeyOne = "space"
KeyTwo = "down"


def main(args):
	app = QApplication(args)
	app.setStyle("plastique")
	form = MainWindow()
	form.resize(300,80)
	form.show()
	app.exec_()

class primindo_thread (QThread):
	posicao_rato = pyqtSignal(str)
	def __init__(self, parent=None):
		super(primindo_thread, self).__init__(parent)

	def __del__(self):
		self.wait()

	def run(self):
		time.sleep(5)
		while True:
			pyautogui.press(KeyOne)
			time.sleep(0.3)
			pyautogui.press(KeyTwo)
			self.posicao_rato.emit(str(pyautogui.position()))
			time.sleep(0.3)



class Conteudo(QWidget):
	def __init__(self, parent=None):
		super(Conteudo, self).__init__(parent)
		
		self.botao = QPushButton("Executa")
		self.botao2 = QPushButton("Parar")
		Label1 = QLabel(KeyOne + " " + "+" + " " + KeyTwo)
		Label21 = QLabel("Posicao do rato: ")
		self.Label22 = QLabel()
		Label3 = QLabel("Teclas a serem primidas: ")
		butoes = QHBoxLayout()
		labeles = QHBoxLayout()
		informacao = QHBoxLayout()
		final = QVBoxLayout()
		butoes.addWidget(self.botao)
		butoes.addWidget(self.botao2)
		labeles.addWidget(Label3)
		labeles.addWidget(Label1)
		informacao.addWidget(Label21)
		informacao.addWidget(self.Label22)
		#labeles.addWidget(Label2)
		final.addLayout(butoes)
		final.addLayout(labeles)
		final.addLayout(informacao)
		self.setLayout(final)


class MainWindow(QMainWindow):
	def __init__(self, parent=None):

		QMainWindow.__init__(self)
		self.mainWidget = QWidget(self)
		
		exitAction = QAction(("&Sair"), self)
		exitAction.setShortcut('ESC')
		exitAction.setStatusTip(("Sair da aplicacao"))
		exitAction.triggered.connect(qApp.quit)
		
		menubar = self.menuBar()
		ExitMenu = menubar.addMenu("Sair")
		ExitMenu.addAction(exitAction)
		layoutfixo = QHBoxLayout(self.mainWidget)
		self.conteudo = Conteudo()
		layoutfixo.addWidget(self.conteudo)
		self.conteudo.botao.clicked.connect(self.primindo)
		self.conteudo.botao2.clicked.connect(self.terminar)
		self.mainWidget.setLayout(layoutfixo)
		self.setCentralWidget(self.mainWidget)
		self.setGeometry(1600, 700, 600, 600)
		self.setWindowTitle("Auto KeyPress")
		self.setWindowIcon(QtGui.QIcon('brand.ico'))
		self.statusBar().showMessage(("Arrancou!"))
		#self.setWindowFlags(Qt.FramelessWindowHint) #tira a frame da janela na totalidade
	 	#self.setWindowFlags(Qt.WindowTitleHint) # remove minimizar, maximizar e desabilita o fechar
	
	def primindo(self):
		 self.processo = primindo_thread()
		 self.processo.posicao_rato.connect(self.dummy)
		 self.processo.start()
		 self.statusBar().showMessage(("Em execucao"))

	def terminar(self):
		self.processo.terminate()
		self.statusBar().showMessage(("Terminou!"))
	
	def dummy(self, texto):
		#self.merdas.valor.setText(str(texto))
		self.conteudo.Label22.setText(texto)

if __name__ == "__main__":
	main(sys.argv)
	#sys.e xit()
