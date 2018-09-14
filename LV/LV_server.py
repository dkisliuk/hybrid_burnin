#!/usr/bin/python

'''
Sets up a server for hybrid_burnin package to setup LV supply

Author: Dylan Kisliuk (dkisliuk@physics.utoronto.ca)
Date: July 2018
'''

import os
import socket
import threading
import multiprocessing
from time import sleep
port = 6464
BUF_SIZE = 1024
DEBUG = 1

#List of background processor objects
proc_list = []

##########################
 #Change these for your own setup!!!!
raspIP = '128.100.75.214'
KeithName = 'USB0::1510::8752::9103795::0::INSTR'
##########################
##########################

def server():
	#Setup the server
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (raspIP, port)
	sock.bind(server_address)
	sock.listen(1) #Only allow 1 client
	print "Opening LV_server client. Listening..."

	#Wait for client requests
	flag = True
	while flag:
		(connection, client_address) = sock.accept()
		try:
			print "Connection from " + str(client_address)
			msg = ''
			while True:
				connection.settimeout(3)
				data = connection.recv(BUF_SIZE)
				msg += data
				print data
				if DEBUG: print "Received message: %s" %msg
				if msg.count('Quit'):
					flag = False
					print "Shutting down LV server"
					break
				#Ping from client to make sure server is running
				if msg.count('Ping'):
					connection.sendall("Ping\0")
				LVsettings = LVmanage()
				LVsettings.parse(msg) #Setup LV supply
				status = LVsettings.configure()
				if status == 0:
					connection.sendall("ACK\0")
				else:
					connection.sendall("BAD\0")
				break
		finally:
			connection.close()

#Class for holding settings for LV
class LVmanage:
	def __init__(self):
		self.dev=None
		self.V1=0
		self.V2=0
		self.V3=0
		self.C1=0
		self.C2=0
		self.C3=0

	#Choose LV supply and setup appropriately according to LVblock
	#LVblock should be a string with fields separated by single spaces
	#Ex: LVblock = "dev=Keithley2230G V1=4.5 V2=0.0 V3=1.55 C1=1.5 C2=0.0 C3=2.0"
	def parse(self, setupBlock):
		parser = setupBlock.split(' ')
		for item in parser:
			if item.count('dev'):
				self.dev = item.split('=')[-1] #Get device name
			elif item.count("V1"):
				self.V1 = float(item.split('=')[-1])
			elif item.count("V2"):
				self.V2 = float(item.split('=')[-1])
			elif item.count("V3"):
				self.V3 = float(item.split('=')[-1])
			elif item.count("C1"):
				self.C1 = float(item.split('=')[-1])
			elif item.count("C2"):
				self.C2 = float(item.split('=')[-1])
			elif item.count("C3"):
				self.C3 = float(item.split('=')[-1])

	def configure(self):
		if self.dev == "Keithley2230G":
			status = setKeithley2230G(self)
			return status
		if self.dev == "Sorensen":
			#TODO
			return 0
		if self.dev == "Instek":
			#TODO
			return 0
#end class LVmanage

#Setup Keithley device to specified settings
def setKeithley2230G(settings):
	try:
		import Keithley2230G
	except ImportError:
		print "Could not find module for Keithley2230G. Make sure it's in the correct directory"
		return 1

	#If monitor is running on Keithley, terminate it
	for proc in proc_list:
		if proc.name == 'monitorKeithley2230G':
			print 'Terminating monitoring on Keithley2230G'
			index = proc_list.index(proc)
			proc.terminate()
			del proc_list[index]
			sleep(2)
	#Setup Keithley device
	#while True:
	try:
		Keith = Keithley2230G.Keithley2230G(name=KeithName)
		#break
	except:
		print 'Failed to open Keithley.'
		return 1
	#	continue
	Keith.setCURR(curr1=settings.C1, curr2=settings.C2, curr3=settings.C3)
	Keith.setVOLT(volt1=settings.V1, volt2=settings.V2, volt3=settings.V3)
	Keith.powerON()
	Keith.localMode()
	monitor = multiprocessing.Process(name='monitorKeithley2230G', target=monitorKeithley2230G, args=(settings,Keith))
	monitor.start()
	proc_list.append(monitor)
	return 0

#Monitors Keithley in while loop to ensure does not exceed current compliance. Turns off channel if compliance reached
def monitorKeithley2230G(settings, Keith):
	try:
		import Keithley2230G
	except ImportError:
		print "Could not find module for Keithley2230G. Make sure it's in the correct directory"
		return 1
	flag = False
	while True:
		sleep(5)
		Keith.remoteMode()
		C1 = float(Keithley2230G.getCURR(Keith, chan=1) )
		C2 = float(Keithley2230G.getCURR(Keith, chan=2) )
		C3 = float(Keithley2230G.getCURR(Keith, chan=3) )
		if DEBUG: print "Channel currents: C1=%.3fA C2=%.3fA C3=%.3fA" %(C1, C2, C3)
		#If voltage channel is exceeding current compliance (and current compliance isn't 0)
		if abs(C1-settings.C1)<0.002 and settings.C1 > 0.001:
			Keith.setVOLT(volt1=0.0, volt2=settings.V2, volt3=settings.V3)
			flag = True
		if abs(C2-settings.C2)<0.002 and settings.C2 > 0.001:
			Keith.setVOLT(volt1=settings.V1, volt2=0.0, volt3=settings.V3)
			flag = True
		if abs(C3-settings.C3)<0.002 and settings.C3 > 0.001:
			Keith.setVOLT(volt1=settings.V1, volt2=settings.V2, volt3=0.0)
			flag = True
		Keith.localMode()
		if flag == True:
			print "Channel exceeded compliance. Ramped down"
			return 1
	
if __name__=="__main__":
	server()
