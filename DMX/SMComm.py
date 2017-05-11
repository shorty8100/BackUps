import os.path
import ctypes
import struct
import math
import copy
import logging

__author__ = "Ivo Vargas"
__copyright__ = "Copyright 2016, Itelmatis"
__credits__ = ["Rui Palma"]
__version__ = "0.2.6"
__maintainer__ = "Ivo Vargas"
__email__ = "informatica@itelmatis.com"
__status__ = "Development"

logname = 'SMComm.log'
logger = logging.getLogger(logname)
format = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(filename=logname,
                    filemode='a',
                    format=format, 
                    level=logging.DEBUG)

# SMonitor interface
class SMComm:

    Tags = []           # Tags List
    FilePath = ""       # Path to Prt File
    handle = None       # Handle

    # Constructor
    def __init__(self, sTags, sFilePath):
        try:
            #SMonitor Library Path
            dll_path = r"c:\S-Monitor"
            os.chdir(dll_path)
            self.smlib = ctypes.WinDLL("S-Monitor.dll")

            self.Tags = sTags
            self.FilePath = sFilePath
        except Exception, e:
            logger.debug('Init error: '+ str(e))


    ##### Expose Library objects #####

    # Cria um ficheiro novo de partilhas com o nome "ficheiro" que deve ser o caminho completo
    # do ficheiro PRT(eg. "c:\s-monitor\rs485\node 0\id1.prt") com a quantidade de variaveis "Tamanho"
    # Devolve o endereco do ficheiro "HANDLE" se tiver conseguido cirar o ficheio ou "NULL" se nao tiver conseguido criar o ficheiro.
    def SMCreateVARFile(self, Tamanho, Ficheiro):
        try:
            self.smlib.SMCreateVARFile.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_char))
            return self.smlib.SMCreateVARFile(ctypes.c_int(Tamanho), Ficheiro)
        except Exception, e:
            logger.debug('SMCreateVARFile error: '+ str(e))

    # Publica as variaveis do array "Valores[]" que tem "Quantidade" variaveis, no ficheiro com o endereco "Endereco" obtido com
    # a funcao SMCreateVARFile(...)
    def ServerSetVARs(self, Valores, Quantidade, Handle):
        try:
            self.smlib.ServerSetVARs.argtypes = (ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_void_p)
            return self.smlib.ServerSetVARs(Valores, ctypes.c_int(Quantidade), ctypes.c_void_p(Handle))
        except Exception, e:
            logger.debug('ServerSetVARs error: '+ str(e))

    # Devolve a lista de ordens pendentes no ponteiro "Valores" e no ponteiro "Offsets" (estes dois arrays deverao ter capacidade
    # para alojar o caso pior que e haver 1 ordem pendente para cada variavel do sistema) que representam os pares
    # [Valor de N da Variavel] com a "Quantidade" de ordens encontradas no ficheiro com o endereco "Endereco" obtido com a funcao
    # SMCreateVARFile(...) que tem a quantidade de variaveis "Tamanho"
    # Devolve "true" se tiver conseguido realizar a tarefa ou "false" se nao tiver conseguido criar o ficheiro.
    def ServerGetVARs(self, Valores, Offsets, Quantidade, Tamanho, Handle):
        try:
            self.smlib.ServerGetVARs.argtypes = (ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_void_p)
            return self.smlib.ServerGetVARs(Valores, Offsets, Quantidade, ctypes.c_int(Tamanho), ctypes.c_void_p(Handle))
        except Exception, e:
            logger.debug('ServerGetVARs error: '+ str(e))

    # Abre o "ficheiro" que deve ser o caminho completo do ficheiro PRT (eg. "c:\S-Monitor\rs485\node 0\id1.prt") com a quantidade de
    # variaveis "Tamanho"
    # Devolve o endereco do ficheiro "HANDLE" se este existir e tiver conseguido abri-lo ou "NULL" se nao tiver conseguido abrir
    # o ficheiro.
    def SMOpen(self, Ficheiro):
        try:
            self.smlib.SMOpen.argtypes = [ctypes.POINTER(ctypes.c_char)]
            return self.smlib.SMOpen(Ficheiro)
        except Exception, e:
            logger.debug('SMOpen error: '+ str(e))

    # Fecha o "ficheiro" com o endereco "Endereco# obtido por qualquer das funcoes SMOpen(...) ou SMCreateVARFile(...)
    # Devolve "true" se tiver conseguido realizar a tarefa ou "false" se nao tiver conseguido fechar o ficheiro.
    # Se o ficheiro nao ficar fechado pode significar que ainda ha outra aplicacao com ele aberto, o ficheiro na realidade
    # quando a ultima aplicacao que o tem aberto o fecha.
    def SMClose(self, Handle):
        try:
            self.smlib.SMClose.argtypes = [ctypes.c_void_p]
            return self.smlib.SMClose(ctypes.c_void_p(Handle))
        except Exception, e:
            logger.debug('SMClose error: '+ str(e))

    # Escreve a variavel n"Offset" com o valor "Valor" no ficheiro com o endereco "Endereco" obtido com a funcao SMOpen(...) que tem
    # a quantidade de variaveis "Tamanho".
    # Devolve "true" se tiver conseguido realizar a tarefa ou "false" se nao tiver conseguido abrir o ficheiro.
    def ClientSetVAR(self, Valor, Offset, Handle):
        try:
            self.smlib.ClientSetVAR.argtypes = (ctypes.c_float, ctypes.c_int, ctypes.c_void_p)
            return self.smlib.ClientSetVAR(ctypes.c_float(Valor), ctypes.c_int(Offset), ctypes.c_void_p(Handle))
        except Exception, e:
            logger.debug('ClientSetVAR error: '+ str(e))

    # Devolve a variavel no ponteiro "Valor" no ficheiro com o endereco "Endereco" obtido com a funcao SMOpen(...) que tem a quantidade
    # de variaveis "Tamanho"
    # Devolve "true" se tiver conseguido realizar a tarefa ou "false" se nao tiver conseguido abrir o ficheiro
    def ClientGetVAR(self, Valor, Offset, Handle):
        try:
            self.smlib.ClientGetVAR.argtypes = (ctypes.c_float, ctypes.c_float, ctypes.c_void_p)
            return self.smlib.ClientGetVAR(ctypes.c_float(Valor), ctypes.c_float(Offset), ctypes.c_void_p(Handle))
        except Exception, e:
            logger.debug('ClientGetVAR error: '+ str(e))

    # Devolve a lista de variaveis no array "Valores" no ficheiro com o endereco "Endereco" obtido com a funcao SMOpen(...) que tem
    # a quantidade de variaveis "Tamanho"
    # Devolve "true" se tiver conseguido realizar a tarefa ou "false" se nao tiver conseguido abrir o ficheiro.
    def ClientGetVARs(self, Valores, Tamanho, Handle):
        try:
            self.smlib.ClientGetVARs.argtypes = (ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_void_p)
            return self.smlib.ClientGetVARs(Valores, ctypes.c_int(Tamanho), ctypes.c_void_p(Handle))
        except Exception, e:
            logger.debug('ClientGetVARs error: '+ str(e))

    # Create File Handle
    def ServerSetVarsToFile(self, prtFilePath):
        try:
            SMFile = open(prtFilePath, 'w')

            # Write Data to file
            for x in range(0, len(self.Tags)):
                SMFile.seek(x * 44, 0)
                SMFile.write(str(self.Tags[x].name))
                SMFile.seek(x * 44 + 40, 0)
                data = bytearray(struct.pack("f", self.Tags[x].value))
                SMFile.write(data)

            # Close file
            SMFile.close()

        except Exception, e:
            logger.debug('ServerSetVarsToFile error: '+ str(e))
            return False

    # Atualiza os valores das Tags a partir de um ficheiro prt
    def ClientGetVARsFromFile(self, Valores, FilePath):
        try:
            SMFile = open(FilePath, 'rb')
            Tamanho = len(Valores)

            # Read Data from file
            nTags = math.floor(len(SMFile) / 44)

            if(Tamanho < nTags):
                nTags = Tamanho

            for x in range(0, nTags):
                SMFile.seek(x * 44 + 40, 0)
                Valores[x] = SMFile.read(1)

            SMFile.close()
            return True
        except Exception, e:
            logger.debug('ClientGetVARsFromFile error: '+ str(e))
            return False

    # Publica as ordens no servidor atraves de um ficheiro
    def ClientSetVARtoFile(self, Valor, Offset, FilePath):
        try:
            SMFile = open(FilePath, 'a')

            # Write Data to file
            SMFile.write(Offset)
            SMFile.write(Valor)

            # Close file
            SMFile.close()
            return True
        except Exception, e:
            logger.debug('ClientSetVARFile error: '+ str(e))
            return False

    # Cria uma lista de variaveis a partir de um ficheiro prt
    # Devolve uma lista de tags "Tag"
    def ReadExternalIndex(self, FilePath):
        try:
            SMFile = open(FilePath, 'rb')

            nTags = os.path.getsize(FilePath)

            SMFile.seek(0, 0)

            for x in range(0, nTags):
                if(SMFile.tell() > nTags - 44):
                    break

                variablen = str(SMFile.read(40))
                try:
                    variablev = struct.unpack('f', SMFile.read(4))[0]
                except:
                    variablev = -1

                if(variablen.startswith("\0")):
                    variablen = "-----------------FREE-----------------"

                if("\0" in variablen):
                    variablen = variablen[0:variablen.index('\0')]

                var = Tag(variablen, variablev)
                var.index = x

                self.Tags.append(var)

            SMFile.close()

            return True
        except Exception, e:
            logger.debug('ReadExternalIndex error: '+ str(e))
            return False

##### CLIENT #####
class SMClient(SMComm):
    TagsUpdated = []
    OldTags = []

    # Import Tags
    def ImportTags(self, FilePath):
        try:
            if(os.path.isfile(FilePath)):
                hPath = self.FilePath + '\0'
                self.FilePath = (ctypes.c_char * len(hPath))(*hPath)

                self.ReadExternalIndex(FilePath)
        except Exception, e:
            logger.debug('ImportTags error: '+ str(e))

    # Push the updated values to the external source
    def Push(self):
        self.handle = self.SMOpen(self.FilePath)

        # Check the connection is open
        if(self.handle == 0):
            logger.debug('No Handle!')
            return False

        try:
            if(self.Tags == self.OldTags):
                return True
            else:
                set1 = set((tag.name, tag.value, tag.index) for tag in self.OldTags)
                self.TagsUpdated = [ tag for tag in self.Tags if (tag.name, tag.value, tag.index) not in set1 ]

            toRemove = []

            for tag in self.TagsUpdated:
                val = (float)(tag.value)
                self.ClientSetVAR(val, tag.index, self.handle)
        except Exception, e:
            logger.debug('Push error: '+ str(e))
            self.SMClose(self.handle)
            self.handle = 0;
            return False

        self.handle = 0;
        self.SMClose(self.handle)

        return True

    # Pull the values from the external source and update the Tags
    def Pull(self):
        self.handle = self.SMOpen(self.FilePath)

        # Check the connection is open
        if(self.handle == 0):
            logger.debug('No Handle!')
            return False

        try:
            # Import tags before update
            if (len(self.Tags) <= 0):
                self.ImportTags(self.FilePath)
                self.OldTags = copy.deepcopy(self.Tags)

            LP_c_float = ctypes.c_float * len(self.Tags)
            vals = LP_c_float()
            test = False

            test = self.ClientGetVARs(vals, len(self.Tags), self.handle)

            for x in range(0, len(self.Tags)):
                if(self.Tags[x].value != vals[x]): # and self.Tags[x] not in self.TagsUpdated):
                    self.Tags[x].value = vals[x]

        except Exception, e:
            logger.debug('Pull error: '+ str(e))
            self.SMClose(self.handle)
            self.handle = 0;
            return False


        self.SMClose(self.handle)
        self.handle = 0;

        return True

##### SERVER #####
class SMServer(SMComm):
    def ExportTags(self):
        try:
            hPath = self.FilePath 
            self.FilePath = (ctypes.c_char * len(hPath + '\0'))(*hPath + '\0')
            self.handle = self.SMCreateVARFile(len(self.Tags), self.FilePath)
            # Create Prt File
            self.ServerSetVarsToFile(hPath);
        except Exception, e:
            logger.debug('ExportTags error: '+ str(e))


    # Push the updated values to the external source
    def Push(self):
        if(self.handle == None):
            self.ExportTags()

        try:
            # Publish Values to RAM
            Values = []
            for tag in self.Tags:
                Values.append(tag.value)

            Vals = (ctypes.c_float * len(Values))(*Values)
            result = self.ServerSetVARs(Vals, len(Vals), self.handle)

            if (result != 1):
                return False

        except Exception, e:
            logger.debug('Push error: '+ str(e))
            return False

        return True


    # Pull the values from external source and update the Tags
    # Return list of Tags "Tag"
    def Pull(self):
        TagsUpdated = []

        try:
            LP_int = ctypes.c_int
            Quantidade = LP_int()
            LP_c_float = ctypes.c_float * len(self.Tags)
            LP_c_floatb = ctypes.c_float * len(self.Tags)
            Valores = LP_c_float()
            Offsets = LP_c_floatb()
            if(self.handle > 0):
                result = self.ServerGetVARs(Valores, Offsets, Quantidade, len(self.Tags), self.handle)

                # Update Tag values
                for x in range(0, Quantidade.value):
                    self.Tags[int(Offsets[x])].value = Valores[x]
                    TagsUpdated.append(self.Tags[int(Offsets[x])])

        except Exception, e:
            logger.debug('Pull error: '+ str(e))

        return TagsUpdated

# Tag Object
# name -> Tag Name/Address
# value -> Value(float)
# index
class Tag:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.index = 0