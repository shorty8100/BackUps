# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import *
import sys
import os
import time
import smtplib #,email,email.encoders,email.mime.text,email.mime.base
import email.mime.application
from datetime import datetime
from time import sleep
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
#from email.base64MIME import encode as encode_base64


__author__ = "Micael Martins"
__copyright__ = "Copyright 2016, Itelmatis"
__credits__ = ["Micael Martins"]
__version__ = "1.0"
__maintainer__ = "Micael Martins"
__email__ = "micaelmartins@itelmatis.com"
__status__ = "Feito"


def main(args):
	app = QApplication(args)
	app.setStyle("plastique")
	form = MainWindow()
	form.resize(300,300)
	form.show()
	app.exec_()
	

class Conteudo(QWidget):
	def __init__(self, parent=None):
		super(Conteudo, self).__init__(parent)
		
		self.botao = QPushButton("Enviar")
		self.relatorio = QTextEdit()
		#self.relatorio.setReadOnly(True)
		
		final = QVBoxLayout()
		final.addWidget(self.relatorio)
		final.addWidget(self.botao)
		
		self.setLayout(final)
	
	def enviar_dados(self):
		de = base64.b64decode("bWljYWVsbWFydGluc0BpdGVsbWF0aXMuY29t")
		pw = base64.b64decode("bWljYWVsaXRlbG1hdGlz")
		#recipients = ["sh.shorty@gmail.com" , "micaelmartins.sh@gmail.com"]
		#recipients = ["soniapeleira@itelmatis.com", "marcosfigueirinha@itelmatis.com", "micael.itelmatis@gmail.com"]
		recipients = ["micael.itelmatis@gmail.com", "marcosfigueirinha@itelmatis.com"]
		lixo1 , de1 , lixo2 = str(de).split("'")
		lixo1 , pw1 , lixo2 = str(pw).split("'")
		#fp = open('itelmatis.jpg', 'rb')
		#msgImage = MIMEImage(fp.read())
		#fp.close()
		# Define the image's ID as referenced above
		#msgImage.add_header('Content-ID', '<image1>')
		msg = MIMEMultipart()
		msg.set_charset('utf-8')
		msg['Subject'] = "Relatório Trabalho Diário"#.encode('utf8')#.decode('utf8')
		msg['From'] = de1
		msg['To'] = ", ".join(recipients)
		data = "Data: " + time.strftime("%d-%m-%Y") + "\n\n"
		obra = data + self.relatorio.toPlainText() + "\n\n" + "Cumprimentos,\nMicael Martins"
		body = MIMEText(obra.encode('utf-8'), _charset='utf-8')
		msg.attach(body)
		#envia a imagem em anexo, sendo a ideia enviar como assinatura
		#msg.attach(msgImage)
		server = smtplib.SMTP('mail.itelmatis.com', 25)
		server.set_debuglevel(0)
		server.login(de1, pw1)
		server.sendmail(de1, recipients, msg.as_string())
		server.quit()



class MainWindow(QMainWindow):
	def __init__(self, parent=None):

		QMainWindow.__init__(self)
		self.mainWidget = QWidget(self)
		
		exitAction = QAction(("&Sair"), self)
		#exitAction.setShortcut('ESC')
		exitAction.setStatusTip(("Sair da aplicacao"))
		exitAction.triggered.connect(qApp.quit)
		
		menubar = self.menuBar()
		#ExitMenu = menubar.addMenu("Sair")
		#ExitMenu.addAction(exitAction)
		
		layoutfixo = QHBoxLayout(self.mainWidget)
		self.conteudo = Conteudo()
		layoutfixo.addWidget(self.conteudo)
		
		self.conteudo.botao.clicked.connect(self.enviar_email)
		
		self.mainWidget.setLayout(layoutfixo)
		self.setCentralWidget(self.mainWidget)
		self.setGeometry(1600, 700, 600, 600)
		self.setWindowTitle("Relatorio Trabalho Diario")
		self.setWindowIcon(QtGui.QIcon('brand.ico'))
		self.statusBar().showMessage(("Que fixe, quase a ir embora!"))
		self.setWindowFlags(Qt.FramelessWindowHint) #tira a frame da janela na totalidade
		#self.setWindowFlags(Qt.WindowTitleHint) # remove minimizar, maximizar e desabilita o fechar
	
	def enviar_email(self):
		try:
			self.statusBar().showMessage(("Aguarde..."))
			self.conteudo.enviar_dados()
			self.statusBar().showMessage(("Emails enviado com sucesso"))
			sleep(1)
			qApp.quit()

		except IOError:
			self.statusBar().showMessage(("ERRO! Emails nao foram enviados"))
	
	def fechar(self):
		qApp.quit


if __name__ == "__main__":
    main(sys.argv)
    #sys.exit()
