from datetime import datetime
import random
import matplotlib.pyplot as plt


__author__ = "Micael Martins"
__copyright__ = "Copyright 2016, Itelmatis"
__credits__ = ["Micael Martins"]
__version__ = "0.4"
__maintainer__ = "Micael Martins"
__email__ = "micaelmartins@itelmatis.com"
__status__ = "Em Desenvolvimento"



logg = open("conTestLog.txt")
timeline = []
value = []

for linhas in logg:
	try:
		x , y , z = linhas.split(" ")
		dia, mes, ano = x.split("-")
		timeline.append(datetime.strptime(ano + "-" + mes + "-" + dia + " " + y, "%Y-%m-%d %H:%M:%S"))
		if "Ok" in z:
			value.append(1)
		else:
			value.append(0)
	except:
		pass

plt.ylabel('Estado da ligacao')
plt.xlabel('Linha temporal')
plt.ylim(-0.01,1.01)
plt.plot(timeline,value,"r-", fillstyle="full")
plt.show()
