#!/usr/bin/python

#Contains commands for sending and receiving messages through FIFOs

def sendCommand(fifoName, buf):
	sendfifo = open(fifoName, 'w')
	print "Sending '%s' signal to %s" %(buf, fifoName)
	sendfifo.write(buf + '\0')
	sendfifo.close()
#end sendCommand

def recvCommand(fifoName):
	print "Opening %s" %fifoName
	recvfifo = open(fifoName, 'r')
	buf = recvfifo.read()
	recvfifo.close()
	return buf
#end recvCommand

#Use both sendCommand and recvCommand
def SendRecv(sendfifo, recvfifo, buf):
	sendCommand(sendfifo, buf)
	buf = recvCommand(recvfifo)
	return buf	
#end SendRecv
