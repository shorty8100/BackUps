# -*- coding: utf-8 -*-
import SMComm
import os
from collections import deque
from threading import Thread
from bacpypes.debugging import bacpypes_debugging, ModuleLogger
from bacpypes.consolelogging import ConfigArgumentParser
from bacpypes.core import run, stop, deferred, enable_sleeping
from bacpypes.iocb import IOCB
from bacpypes.pdu import Address, GlobalBroadcast
from bacpypes.object import get_object_class, get_datatype
from bacpypes.apdu import SubscribeCOVRequest, SimpleAckPDU, RejectPDU, AbortPDU, WritePropertyRequest, WhoIsRequest
from bacpypes.constructeddata import Array, Any
from bacpypes.app import BIPSimpleApplication
from bacpypes.service.device import LocalDeviceObject
from bacpypes.primitivedata import Null, Atomic, Integer, Unsigned, Real
import time

_debug = 0
_log = ModuleLogger(globals())
rsvp = (True, None, None)
this_application = None
Dispositivos = {}
SMTags = []
RELACIONAL = {}
this_file_path = os.getcwd()
TimeBetweenSubs = 5.0 #tempo entre uma subscricao e a seguinte
TimeToRefreshSubs = 1000 #tempo para renovar todas as subscricoes / tempo de vida das subscricoes
TimeToWaitForSub = 10 #timeout para a tentativa de subscricao
SubRetrys = 3 #caso a subscricao falhe tenta de novo
TimeSMonitor = 0.001 #tempo entre pull/push de dados com o SMonitor
diretoriaPRT = "C:\\S-Monitor\\BacNet"


@bacpypes_debugging
class SubscribeCOVApplication(BIPSimpleApplication):

	def __init__(self, *args):
		BIPSimpleApplication.__init__(self, *args)

	def do_ConfirmedCOVNotificationRequest(self, apdu):
		global rsvp
		for element in apdu.listOfValues:
			datatype = get_datatype(apdu.monitoredObjectIdentifier[0], element.propertyIdentifier)
			if not datatype:
				pass
			if issubclass(datatype, Array) and (element.propertyArrayIndex is not None):
				if element.propertyArrayIndex == 0:
					value = element.value.cast_out(Unsigned)
				else:
					value = element.value.cast_out(datatype.subtype)
			else:
				value = element.value.cast_out(datatype)
			deviceid = str(apdu.initiatingDeviceIdentifier[1])
			objecto = str(str(apdu.monitoredObjectIdentifier[0]) + "_" + str(apdu.monitoredObjectIdentifier[1]))
			argumento = str(element.propertyIdentifier)
			if argumento in Dispositivos[deviceid][objecto]:
				Dispositivos[deviceid][objecto][argumento]["valorActual"] = round(float(value), 1)
			else:
				pass
		if rsvp[0]:
			response = SimpleAckPDU(context=apdu)
		elif rsvp[1]:
			response = RejectPDU(reason=rsvp[1], context=apdu)
		elif rsvp[2]:
			response = AbortPDU(reason=rsvp[2], context=apdu)
		self.response(response)

	def do_UnconfirmedCOVNotificationRequest(self, apdu):
		global rsvp
		for element in apdu.listOfValues:
			datatype = get_datatype(apdu.monitoredObjectIdentifier[0], element.propertyIdentifier)
			if not datatype:
				pass
			if issubclass(datatype, Array) and (element.propertyArrayIndex is not None):
				if element.propertyArrayIndex == 0:
					value = element.value.cast_out(Unsigned)
				else:
					value = element.value.cast_out(datatype.subtype)
			else:
				value = element.value.cast_out(datatype)
			deviceid = str(apdu.initiatingDeviceIdentifier[1])
			objecto = str(apdu.monitoredObjectIdentifier[0]) + "_" + str(apdu.monitoredObjectIdentifier[1])
			argumento = str(element.propertyIdentifier)
			if argumento in Dispositivos[deviceid][objecto]:
				Dispositivos[deviceid][objecto][argumento]["valorActual"] = round(float(value), 1)
			else:
				pass
		if rsvp[0]:
			response = SimpleAckPDU(context=apdu)
		elif rsvp[1]:
			response = RejectPDU(reason=rsvp[1], context=apdu)
		elif rsvp[2]:
			response = AbortPDU(reason=rsvp[2], context=apdu)
		self.response(response)

class SubscricaoDados(Thread):

	def __init__(self):
		Thread.__init__(self)
		global Dispositivos
		self.ProcessID = 0
		self.inicio = 0
		self.fim = 0

	def run(self):
		while True:
			self.inicio = time.time()
			for ids in Dispositivos:
				for obj in Dispositivos[ids]:
					addr = Dispositivos[ids]["IPort"]
					if not obj == "IPort":
						for args in Dispositivos[ids][obj]:
							RETRY = 0
							DONE = False
							if self.ProcessID > 3000: self.ProcessID = 0
							while RETRY < SubRetrys and DONE == False:
								try:
									#proc_id = Dispositivos[ids][obj][args]["ProcID"]
									proc_id = self.ProcessID
									lifetime = (int(TimeToRefreshSubs) + 30)
									obj_type, obj_inst = obj.split("_")
									issue_confirmed = True
									if obj_type.isdigit():
										obj_type = int(obj_type)
									elif not get_object_class(obj_type):
										with open("ErrorLog.txt", "a") as myfile:
											myfile.write(str(time.strftime("%d-%m-%Y %H:%M:%S")) + " Error trying to subscribe unknown object type.\n")
									obj_inst = int(obj_inst)
									request = SubscribeCOVRequest(subscriberProcessIdentifier=proc_id, monitoredObjectIdentifier=(obj_type, obj_inst),)
									request.pduDestination = Address(addr)
									if issue_confirmed is not None:
										request.issueConfirmedNotifications = issue_confirmed
									if lifetime is not None:
										request.lifetime = lifetime
									iocb = IOCB(request)
									this_application.request_io(iocb)
									#print "Trying to subscribe to", ids, addr, obj_type, obj_inst
									iocb.wait(TimeToWaitForSub)
									state = iocb.ioState
									'''
									IDLE = 0        # has not been submitted
									PENDING = 1     # queued, waiting for processing
									ACTIVE = 2      # being processed
									COMPLETED = 3   # finished
									ABORTED = 4 	# finished in a bad way
									'''
									if state == 0:
										time.sleep(TimeBetweenSubs)
										#print "ZZzzzzZZZzzzzZZZzzzzZZZ"
									elif state == 1:
										#print "Esta na queue, vai limpar e tentar de novo..."
										this_application.queue_by_address.clear()
										time.sleep(TimeBetweenSubs)
									elif state == 2:
										#print "Esta em processamento..."
										self.ProcessID += 1
										DONE = True
									elif state == 3:
										#print "YEIII"
										self.ProcessID += 1
										DONE = True
									elif state == 4:
										time.sleep(TimeBetweenSubs)
										#print "ABORTTTTTTTT, ja deu merdinha"
										with open("ErrorLog.txt", "a") as myfile:
											myfile.write(str(time.strftime("%d-%m-%Y %H:%M:%S")) + "ABORTTTTTTTT")
									else:
										time.sleep(TimeBetweenSubs)
										#print "WATTTT YYYY!!!! NUNCA VISTO"
										with open("ErrorLog.txt", "a") as myfile:
											myfile.write(str(time.strftime("%d-%m-%Y %H:%M:%S")) + "WATTTT YYYY!!!! NUNCA VISTO")
								except Exception as e:
									with open("ErrorLog.txt", "a") as myfile:
										myfile.write(str(time.strftime("%d-%m-%Y %H:%M:%S")) + " Error while trying to subscribe, proc_id:" + str(proc_id) + " Addr:" + str(addr) + "\n")
										myfile.write("Error -> " + str(e) + "\n")
								RETRY += 1
			self.fim = time.time()
			#print "Levou:", self.fim - self.inicio
			#print "Refresh Default:", TimeToRefreshSubs
			#print "Refresh Fixed:" , TimeToRefreshSubs - TimeBetweenSubs - round(self.fim - self.inicio, 1)
			#print Dispositivos
			time.sleep(abs(TimeToRefreshSubs - TimeBetweenSubs - round(self.fim - self.inicio, 1)))


class ComunicacaoSM(Thread):

	def __init__(self):
		Thread.__init__(self)
		global Dispositivos
		#print "smonitor thread"
		self.counter = 0
		try:
			if not os.path.exists(diretoriaPRT):
				os.makedirs(diretoriaPRT)
			if('smonitor' not in locals()):
				for ids in Dispositivos:
					for obj in Dispositivos[ids]:
						addr = Dispositivos[ids]["IPort"]
						if not obj == "IPort":
							dicrel = {}
							for args in Dispositivos[ids][obj]:
								dicrel["ID"] = ids
								dicrel["OBJ"] = obj
								dicrel["ARG"] = args
								dicrel["NOME"] = str(ids) + "_" + Dispositivos[ids][obj][args]["NomeVAR"]
								nome = str(ids) + "_" + Dispositivos[ids][obj][args]["NomeVAR"]
								valor = Dispositivos[ids][obj][args]["valorActual"]
								SMTags.append(SMComm.Tag(nome, valor))
								RELACIONAL[self.counter] = dicrel
								self.counter += 1
				self.smonitor = SMComm.SMServer(SMTags, diretoriaPRT + "\\BacNet.prt")
		except Exception as e:
			with open("ErrorLog.txt", "a") as myfile:
				myfile.write(str(time.strftime("%d-%m-%Y %H:%M:%S")) + " Failed to create PRT file.\n")
				myfile.write("Error -> " + str(e) + "\n")

	def run(self):
		while True:
			try:
				TagsUpdated = self.smonitor.Pull()
				while(len(TagsUpdated) > 0):
					Tag = TagsUpdated.pop()
					for idx in RELACIONAL:
						if Tag.name == RELACIONAL[idx]["NOME"]:
							if Dispositivos[RELACIONAL[idx]["ID"]][RELACIONAL[idx]["OBJ"]][RELACIONAL[idx]["ARG"]]["escrita"] == True:
								#print Tag.name, round(Tag.value, 2)
								try:
									addr = Dispositivos[RELACIONAL[idx]["ID"]]["IPort"]
									obj_type = RELACIONAL[idx]["OBJ"].split("_", 1)[0]
									obj_inst = int(RELACIONAL[idx]["OBJ"].split("_", 1)[1])
									prop_id = RELACIONAL[idx]["ARG"]
									#value = int(round(Tag.value, 0))
									value = round(Tag.value, 2)
									Dispositivos[RELACIONAL[idx]["ID"]][RELACIONAL[idx]["OBJ"]][RELACIONAL[idx]["ARG"]]["valorActual"] = value
									indx = None
									priority = None
									datatype = get_datatype(obj_type, prop_id)
									if (value == 'null'):
										value = Null()
									elif issubclass(datatype, Atomic):
										if datatype is Integer:
											value = int(value)
										elif datatype is Real:
											value = float(value)
										elif datatype is Unsigned:
											value = int(value)
										value = datatype(value)
									elif issubclass(datatype, Array) and (indx is not None):
										if indx == 0:
											value = Integer(value)
										elif issubclass(datatype.subtype, Atomic):
											value = datatype.subtype(value)
										elif not isinstance(value, datatype.subtype):
											break
											#raise TypeError("invalid result datatype, expecting %s" % (datatype.subtype.__name__,))
									elif not isinstance(value, datatype):
										break
										#raise TypeError("invalid result datatype, expecting %s" % (datatype.__name__,))
									request = WritePropertyRequest(
												objectIdentifier=(obj_type, obj_inst),
												propertyIdentifier=prop_id
												)
									request.pduDestination = Address(addr)
									request.propertyValue = Any()
									try:
										request.propertyValue.cast_in(value)
									except Exception as error:
										break
										#print("WriteProperty cast error: %r", error)
									if indx is not None:
										request.propertyArrayIndex = indx
									if priority is not None:
										request.priority = priority
									iocb = IOCB(request)
									this_application.queue_by_address.clear()
									this_application.request_io(iocb)
									iocb.wait(1)
									if iocb.ioResponse:
										if not isinstance(iocb.ioResponse, SimpleAckPDU):
											with open("ErrorLog.txt", "a") as myfile:
												myfile.write(str(time.strftime("%d-%m-%Y %H:%M:%S")) + "Did not received ACK for " + str(addr) + " " + str(obj_type) + " " + str(obj_inst) + " " + str(prop_id) + " " + str(value))
										else:
											pass
											#print "ACK"
									if iocb.ioError:
										with open("ErrorLog.txt", "a") as myfile:
											myfile.write(str(time.strftime("%d-%m-%Y %H:%M:%S")) + " Error on response to " + str(addr) + " " + str(obj_type) + " " + str(obj_inst) + " " + str(prop_id) + " " + str(value))
								except Exception as e:
									with open("ErrorLog.txt", "a") as myfile:
										myfile.write(str(time.strftime("%d-%m-%Y %H:%M:%S")) + " Failed to write parameter.\n")
										myfile.write("Error -> " + str(e) + "\n")
									pass #tenta processar a escrita, se nao conseguir ignora
							else:
								pass # se a flag de escrita, nao for verdadeira, nao interessa
							pass
						else:
							pass # se nao constar no dicionario de relacoes, nao interessa
						
				for idx in xrange(0, len(SMTags)):
					if SMTags[idx].name == RELACIONAL[idx]["NOME"]:
						SMTags[idx].value = Dispositivos[RELACIONAL[idx]["ID"]][RELACIONAL[idx]["OBJ"]][RELACIONAL[idx]["ARG"]]["valorActual"]
				self.smonitor.Push()
			except Exception as e:
				with open("ErrorLog.txt", "a") as myfile:
					myfile.write(str(time.strftime("%d-%m-%Y %H:%M:%S")) + " Failed to Pull/Push data to SMonitor.\n")
					myfile.write("Error -> " + str(e) + "\n")
			time.sleep(TimeSMonitor)


def main():
	global this_application
	global Dispositivos
	args = ConfigArgumentParser(description=__doc__).parse_args()
	this_device = LocalDeviceObject(objectName=args.ini.objectname,
			objectIdentifier=int(args.ini.objectidentifier),
			maxApduLengthAccepted=int(args.ini.maxapdulengthaccepted),
			segmentationSupported=args.ini.segmentationsupported,
			vendorIdentifier=int(args.ini.vendoridentifier),)
	this_application = SubscribeCOVApplication(this_device, args.ini.address)
	try:
		ficheiro = open(this_file_path + "/" + "Config.csv", "r")
		configs = ficheiro.read()
		ficheiro.close()
		numLinhas = 0
		for linha in configs.split("\n"):
			valores = {}
			argumento = {}
			objectos = {}
			try:
				if numLinhas == 0:
					numLinhas += 1
					pass
				else:
					DeviceID, IPort, ProcID, Object, ObjectID, Argument, VarName, DefaultVarValue, writeble = linha.split(";")
					valores["valorActual"] = int(DefaultVarValue)
					valores["NomeVAR"] = VarName
					valores["ProcID"] = int(ProcID)
					valores["escrita"] = bool(int(writeble))
					argumento[Argument] = valores
					objectos[Object + "_" + ObjectID] = argumento
					objectos["IPort"] = IPort
					if not DeviceID in Dispositivos:
						Dispositivos[DeviceID] = objectos
					else:
						Dispositivos[DeviceID].update(objectos)
					numLinhas += 1
			except:
				pass #serve para ignorar a ultima linha que nao contem qualquer tipo de informacao util
	except Exception as e:
		with open("ErrorLog.txt", "a") as myfile:
			myfile.write(str(time.strftime("%d-%m-%Y %H:%M:%S")) + " Failed to open configuration file.\n")
			myfile.write("Error -> " + str(e) + "\n")
	services_supported = this_application.get_services_supported()
	this_device.protocolServicesSupported = services_supported.value
	enable_sleeping()
	subscribe_thread = SubscricaoDados()
	SMmonitor_thread = ComunicacaoSM()
	deferred(SMmonitor_thread.start)
	deferred(subscribe_thread.start)
	run()


if __name__ == "__main__":
	main()
