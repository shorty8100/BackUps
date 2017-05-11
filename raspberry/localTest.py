
import SMonitor
import os.path
import ctypes
import struct
import time

__author__ = "Ivo Vargas"
__copyright__ = "Copyright 2016, Itelmatis"
__credits__ = ["Rui Palma"]
__version__ = "0.1.0"
__maintainer__ = "Ivo Vargas"
__email__ = "informatica@itelmatis.com"
__status__ = "Development"

#Convert string to int or float
def convertStr(s):
    """Convert string to either int or float."""
    try:
        ret = int(s)
    except ValueError:
        #Try float
        ret = float(s)
    return ret

##### CLIENT #####
def client():
	print "Client Started"

    # Init Tags List
	Tags = []

    # Open PRT
	smonitor = SMonitor.SMClient(Tags, "c:\\S-Monitor\\S-Monitor.prt")
	while True:
		try:
			time.sleep(3)
			smonitor.Pull()
			#print str(Tags[0].name) + " => " + str(Tags[0].value) + " => " + str(Tags[0].index)
			Tags[1].value = Tags[1].value + 1
			if smonitor.Push():
				print "correu ppush"
			else:
				print "fudeu push"
				
			# tag in smonitor.Tags:
			#	print tag.name + " => " + str(tag.value) + " => " + str(tag.index)
		except Exception, e:
			print('Something went terrible wrong: '+ str(e))


##### SERVER #####
def server():
    print "Server Started"

    # Read registers
    # Init Tags List
    Tags = []

    for x in range(0, 4000):
        Tags.append(SMonitor.Tag(0, x))

    while True:
        try:
            # SMonitor Set Values
            if('smonitor' not in locals()):
                smonitor = SMonitor.SMServer(Tags, "c:\\S-Monitor\\test.prt")
            smonitor.Push()

            smonitor.Pull()

            Tags[2].value = Tags[0].value * Tags[1].value

            # Go to bed for 100 miliseconds
            time.sleep(0.1)

        except Exception, e:
            print('Something went terrible wrong: '+ str(e))


## START SERVER TEST ##
#server()

## START CLIENT TEST ##
client()
