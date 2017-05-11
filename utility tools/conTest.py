import os
import time

__author__ = "Micael Martins"
__copyright__ = "Copyright 2016, Itelmatis"
__credits__ = ["Micael Martins"]
__version__ = "0.3"
__maintainer__ = "Micael Martins"
__email__ = "micaelmartins@itelmatis.com"
__status__ = "Em Desenvolvimento"

hostname = "google.com"
timestamp = str(time.strftime("%d-%m-%Y %H:%M:%S"))
time_between_requests = 60

with open("conTestLog.txt", "a") as myfile:
			myfile.write("\nArrancou!\n")
while True:
	response = os.system("ping -n 1 " + hostname)
	timestamp = str(time.strftime("%d-%m-%Y %H:%M:%S"))
	if response == 0:
		#print (hostname, 'is up!', timestamp)
		with open("conTestLog.txt", "a") as myfile:
			myfile.write(timestamp + " Ok")
	else:
		#print (hostname, 'is down!')
		with open("conTestLog.txt", "a") as myfile:
			myfile.write(timestamp + " Erro")
	with open("conTestLog.txt", "a") as myfile:
		myfile.write("\n")
	time.sleep(time_between_requests)
