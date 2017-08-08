import paramiko
import cmd
import sys
import datetime
from time import strftime

#a ordem e importante para nao se perder o link
ips = [33, 29, 32, 26, 28, 27, 23, 22, 15, 16, 21, 14, 13, 12, 11, 10]
datinha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
with open("Logger.txt", "a") as myfile:
	myfile.write("Executado " + datinha + "\n")
print "StarTed" , datinha
for ip in ips: 
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ipstr='192.168.1.'+str(ip)
	sys.stdout.write("Connecting to " + ipstr + "\t\t\t")
	sys.stdout.flush()
	try:
		#ssh.connect(ipstr, username='ubnt', password='micael')
		ssh.connect(ipstr, username='ubnt', password='2G33N015')
		print "[Ok]"
		with open("Logger.txt", "a") as myfile:
			myfile.write(ipstr + "\t\t\t OK" + "\n")
	except:
		print "[Fail]"
		with open("Logger.txt", "a") as myfile:
			myfile.write(ipstr + "\t\t\t Erro" + "\n")
		continue
	ssh.exec_command("reboot")
	ssh.close()
datinha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print "Finish!!!", datinha
with open("Logger.txt", "a") as myfile:
	myfile.write(">-----------------------------------------<\n")
