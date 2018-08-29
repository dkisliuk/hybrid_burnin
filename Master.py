#!/usr/python

#from CommonVars import * #Contains imports and environment variables
import sys
import os
import ROOT
import subprocess
os.environ["HYBRID_BURN"] = os.environ["PWD"] #Needs to be launched in correct directory
HYBRID_BURN = os.environ["HYBRID_BURN"]

#ID number for the network card used for connecting to FPGA
#Will change from machine to machine. Can determine by running 'ifconfig'
NETWORK_CARD_ID = "enp3s0"

try:
	SCTDAQ_ROOT = os.environ['SCTDAQ_ROOT']
	ROOTSYS     = os.environ['ROOTSYS']
except:
	print 'One of the following environment variables is not set:'
	print '    SCTDAQ_ROOT'
	print '    ROOTSYS'
	print 'Please set appropriately.'
	sys.exit()
sys.path.insert(0, HYBRID_BURN+'/GUI')
import HybridGUI
from PyQt4 import QtGui

#Main program
def main():
	print '#######################################################'
	print 'Master.py - Starting master program for hybrid burn-in.'

	#Launch hsioPipe
	toHsio   = "/tmp/hsioPipe.toHsio"
	fromHsio = "/tmp/hsioPipe.fromHsio"
	if os.path.exists(toHsio) and os.path.exists(fromHsio): pass
	else:
		os.mkfifo(toHsio  )
		os.mkfifo(fromHsio)
	subprocess.call(['sudo ip link set dev ' + NETWORK_CARD_ID + ' up'], shell=True)
	runHsio = subprocess.Popen(['sudo gnome-terminal -x '+SCTDAQ_ROOT+'/bin/hsioPipe --eth '+NETWORK_CARD_ID+',e0:dd:cc:bb:aa:00 --file '+toHsio+','+fromHsio], shell=True)
	print 'Master.py - Opening hsioPipe'
	

	#Fork
	pid = os.fork()

	if pid > 0: #Parent process
		#Launch ITSDAQ
		ParentPid = os.getpid()
		GUIpid = pid
		print 'Master.py - Launching ITSDAQ server locally'
		subprocess.Popen([ROOTSYS+'/bin/root', '-l', 'RunTests.cpp'],
						 stdin=subprocess.PIPE)
						 

	if pid == 0: #Child process
		#Launch GUI
		GUIpid = os.getpid()
		print 'Master.py - Opening GUI display'
		app = QtGui.QApplication(sys.argv)
		display = HybridGUI.Window()
		sys.exit(app.exec_())

main()
