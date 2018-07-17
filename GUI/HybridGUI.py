#!/usr/python

'''
Hybrid Burn-in GUI

This GUI is intended make running the Hybrid burn-in cycle as intuitive as possible.

Author: Dylan Kisliuk
E-mail: dkisliuk@physics.utoronto.ca
'''

import sys
import os
from PyQt4 import QtGui, QtCore
from FIFOsharing import sendCommand, recvCommand, SendRecv #Local file
import HybridConfig as Config
SCTDAQ_ROOT = os.environ['SCTDAQ_ROOT']
ROOTSYS     = os.environ['ROOTSYS']
HYBRID_BURN = os.environ['PWD']

#FIFO
sendfifoName = HYBRID_BURN + "/GUI2DAQ.fifo"
recvfifoName = HYBRID_BURN + "/DAQ2GUI.fifo"

#Window class defines the display, dimensions, buttons, etc.
class Window(QtGui.QMainWindow):
	def __init__(self):
		self.initX = 20
		self.initY = 20
		self.sizeX = 500
		self.sizeY = 500
		self.ITSDAQup = False
		print '\nHybridGUI.py - Instantiating instance of Window class\n'
		super(Window, self).__init__()
		self.setGeometry(self.initX, self.initY, 
						 self.sizeX, self.sizeY)
		self.setWindowTitle("Hybrid Burn-in")
		self.setWindowIcon(QtGui.QIcon('hybridlogo.png') )
		self.home()
	#end __init__

	def home(self):
		#Quit button
		quitX = 100
		quitY = 30
		quitBtn = QtGui.QPushButton("Quit", self)
		quitBtn.clicked.connect(self.exit_app)
		quitBtn.resize(quitX,quitY)
		quitBtn.move(self.sizeX - quitX, self.sizeY - quitY)

		#Tests checkboxes
		checkboxPosX = self.sizeX - 150
		checkboxPosY = 40
		checkboxLabel = QtGui.QLabel("Tests", self)
		checkboxLabel.move(checkboxPosX, checkboxPosY-20)

		self.strobeDelay = QtGui.QCheckBox('Strobe Delay', self)
		self.strobeDelay.resize(150, 20)
		self.strobeDelay.move(checkboxPosX, checkboxPosY)
		if Config.strobeDelay: self.strobeDelay.toggle()

		self.trimRange = QtGui.QCheckBox('Trim Range', self)
		self.trimRange.resize(150, 20)
		self.trimRange.move(checkboxPosX, checkboxPosY+20)
		if Config.trimRange: self.trimRange.toggle()

		self.threePtGain = QtGui.QCheckBox('Three Point Gain', self)
		self.threePtGain.resize(150, 20)
		self.threePtGain.move(checkboxPosX, checkboxPosY+40)
		if Config.threePtGain: self.threePtGain.toggle()

		self.responseCurve = QtGui.QCheckBox('Response Curve', self)
		self.responseCurve.resize(150, 20)
		self.responseCurve.move(checkboxPosX, checkboxPosY+60)
		if Config.responseCurve: self.responseCurve.toggle()

		self.noiseOccup = QtGui.QCheckBox('Noise Occupancy', self)
		self.noiseOccup.resize(150, 20)
		self.noiseOccup.move(checkboxPosX, checkboxPosY+80)
		if Config.noiseOccup: self.noiseOccup.toggle()
		
		#Run button
		runX = 100
		runY = 30
		runBtn = QtGui.QPushButton("Run Tests", self)
		runBtn.clicked.connect(self.run_tests)
		runBtn.resize(runX, runY)
		runBtn.move(self.sizeX - runX, checkboxPosY+100)
		
		#LV supply
		LV_X = 0
		LV_Y = 40
		LVlabel = QtGui.QLabel("LV Supply", self)
		LVlabel.move(LV_X+4, LV_Y-25)
		VoltLabel = QtGui.QLabel("Volt (V)", self)
		VoltLabel.move(LV_X+50, LV_Y+25)
		CurrLabel = QtGui.QLabel("Curr (A)", self)
		CurrLabel.move(LV_X+110, LV_Y+25)
		LVbutton = QtGui.QPushButton("Set LV", self)
		LVbutton.move(LV_X+60, LV_Y+140)
		LVbutton.clicked.connect(self.run_LV)
		self.LVmenu = QtGui.QComboBox(self)
		self.LVmenu.move(LV_X, LV_Y)
		self.LVmenu.addItem("Keithley2230G")
		self.LVmenu.addItem("Instek")
		self.LVmenu.addItem("Sorensen")
		if Config.deviceName is not None:
			self.LVmenu.setCurrentIndex(self.LVmenu.findText(Config.deviceName) ) #Choose device from config file
		self.LVmenu.activated.connect(self.LVdisplay)
		self.CH1 = QtGui.QLabel("CH1", self)
		self.CH2 = QtGui.QLabel("CH2", self)
		self.CH3 = QtGui.QLabel("CH3", self)
		self.CH1.move(LV_X+4, LV_Y+50)
		self.CH2.move(LV_X+4, LV_Y+80)
		self.CH3.move(LV_X+4, LV_Y+110)
		self.CH1Volt = QtGui.QDoubleSpinBox(self)
		self.CH1Curr = QtGui.QDoubleSpinBox(self)
		self.CH2Volt = QtGui.QDoubleSpinBox(self)
		self.CH2Curr = QtGui.QDoubleSpinBox(self)
		self.CH3Volt = QtGui.QDoubleSpinBox(self)
		self.CH3Curr = QtGui.QDoubleSpinBox(self)
		self.CH1Volt.move(LV_X+50, LV_Y+50)
		self.CH1Curr.move(LV_X+110, LV_Y+50)
		self.CH2Volt.move(LV_X+50, LV_Y+80)
		self.CH2Curr.move(LV_X+110, LV_Y+80)
		self.CH3Volt.move(LV_X+50, LV_Y+110)
		self.CH3Curr.move(LV_X+110, LV_Y+110)
		self.CH1Volt.resize(60, 30)
		self.CH2Volt.resize(60, 30)
		self.CH3Volt.resize(60, 30)
		self.CH1Curr.resize(60, 30)
		self.CH2Curr.resize(60, 30)
		self.CH3Curr.resize(60, 30)
		#Initial values from configuration file
		self.CH1Volt.setValue(Config.CH1Volt)
		self.CH1Curr.setValue(Config.CH1Curr)
		self.CH2Volt.setValue(Config.CH2Volt)
		self.CH2Curr.setValue(Config.CH2Curr)
		self.CH3Volt.setValue(Config.CH3Volt)
		self.CH3Curr.setValue(Config.CH3Curr)
		self.show()

		#Run tests immediately if 'runOnStart' in config file is true
		if(Config.runOnStart):
			#TODO add functionality to turn on LV
			self.run_tests()
	#end home

	def exit_app(self):
		print("HybridGUI.py - Exiting")
		sendCommand(sendfifoName, "Quit")
		sock = setClient()
		sock.sendall("Quit")
		sys.exit()
	#end exit_app

	#Sends commands to RunTests.cpp server to run ITSDAQ tests
	def run_tests(self):
		print "HybridGUI.py - Opening fifo %s for sending" %sendfifoName
		#Only run the following commands if ITSDAQ has not yet been launched
		if self.ITSDAQup == False:
			self.ITSDAQup = True
			recvMsg = SendRecv(sendfifoName, recvfifoName, "Start")
			recvMsg = SendRecv(sendfifoName, recvfifoName, "HCC")
			recvMsg = SendRecv(sendfifoName, recvfifoName, "ChipID")
		#Strobe Delay
		if self.strobeDelay.isChecked():
			print "Running:    Strobe Delay test"
			recvMsg = SendRecv(sendfifoName, recvfifoName, "Strobe")
		#Trim Range
		if self.trimRange.isChecked():
			print "Running:    Trim Range test"
			recvMsg = SendRecv(sendfifoName, recvfifoName, "Trim")
		#Three Point Gain (qCentre = 2fC)
		if self.threePtGain.isChecked():
			print "Running:    Three Point Gain test"
			recvMsg = SendRecv(sendfifoName, recvfifoName, "ThreePt")
		#Response Curve (400 events)
		if self.responseCurve.isChecked():
			print "Running:    Response Curve test"
			recvMsg = SendRecv(sendfifoName, recvfifoName, "RespCurve")
		#Noise Occupancy
		if self.noiseOccup.isChecked():
			print "Running:    Noise Occupancy test"
			recvMsg = SendRecv(sendfifoName, recvfifoName, "NoiseOcc")
	#end run_tests

	def run_LV(self):
		if Config.raspIP is not None:
			#Setup client
			import socket
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_address = (Config.raspIP, Config.port)
			print "HybridGUI.py - Connecting to %s port %s" %server_address
			sock.connect(server_address)

			dev = str(self.LVmenu.currentText() )
			V1 = str(self.CH1Volt.value() )
			V2 = str(self.CH2Volt.value() )
			V3 = str(self.CH3Volt.value() )
			C1 = str(self.CH1Curr.value() )
			C2 = str(self.CH2Curr.value() )
			C3 = str(self.CH3Curr.value() )

			try:
				message = "dev=%s V1=%s V2=%s V3=%s C1=%s C2=%s C3=%s" %(dev, V1, V2, V3, C1, C2, C3)
				print "HybridGUI.py - Sending message to server: %s" %message
				sock.sendall(message)
				recvSize = 0
				recvExpct = 4
				data = ''
				while recvSize < recvExpct:
					data = sock.recv(1024)
					recvSize += len(data)
				if data == "ACK\0":
					print "HybridGUI.py - LV successfully set"
				else:
					print "HybridGUI.py - Problem setting up LV"
			finally:
				print "HybridGUI.py - Closing socket"
				sock.close()		
	#end run_LV

	def LVdisplay(self):
		text = str(self.LVmenu.currentText() )
		print 'Selected: ' + text
	#end LVdisplay

def launch():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())
#end launch

def setClient():
	#Setup client
	import socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (Config.raspIP, Config.port)
	print "HybridGUI.py - Connecting to %s port %s" %server_address
	sock.connect(server_address)
	return sock
#end setClient

if __name__ == '__main__':
	launch()
