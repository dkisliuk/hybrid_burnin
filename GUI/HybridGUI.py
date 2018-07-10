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
		self.strobeDelay.toggle()

		self.trimRange = QtGui.QCheckBox('Trim Range', self)
		self.trimRange.resize(150, 20)
		self.trimRange.move(checkboxPosX, checkboxPosY+20)
		self.trimRange.toggle()

		self.threePtGain = QtGui.QCheckBox('Three Point Gain', self)
		self.threePtGain.resize(150, 20)
		self.threePtGain.move(checkboxPosX, checkboxPosY+40)

		self.responseCurve = QtGui.QCheckBox('Response Curve', self)
		self.responseCurve.resize(150, 20)
		self.responseCurve.move(checkboxPosX, checkboxPosY+60)
		self.responseCurve.toggle()

		self.noiseOccup = QtGui.QCheckBox('Noise Occupancy', self)
		self.noiseOccup.resize(150, 20)
		self.noiseOccup.move(checkboxPosX, checkboxPosY+80)
		self.noiseOccup.toggle()
		
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
		CurrLabel = QtGui.QLabel("Curr (A)", self)
		VoltLabel.move(LV_X+50, LV_Y+25)
		CurrLabel.move(LV_X+110, LV_Y+25)
		self.LVmenu = QtGui.QComboBox(self)
		self.LVmenu.move(LV_X, LV_Y)
		self.LVmenu.addItem("Keithley2230G")
		self.LVmenu.addItem("Instek")
		self.LVmenu.addItem("Sorensen")
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
	#end home

	def exit_app(self):
		print("HybridGUI.py - Exiting")
		#TODO Quit ITSDAQ
		sendCommand(sendfifoName, "Quit")
		sys.exit()
	#end exit_app

	#Sends commands to RunTests.cpp server to run ITSDAQ tests
	def run_tests(self):
		print "HybridGUI.py - Opening fifo %s for sending" %sendfifoName
		sendCommand(sendfifoName, "Start")
		recvMsg = recvCommand(recvfifoName)
		sendCommand(sendfifoName, "HCC")
		recvMsg = recvCommand(recvfifoName)
		sendCommand(sendfifoName, "ChipID")
		recvMsg = recvCommand(recvfifoName)
		if self.strobeDelay.isChecked():
			print "    Strobe Delay test"
			sendCommand(sendfifoName, "Strobe")
			recvMsg = recvCommand(recvfifoName)
		if self.trimRange.isChecked():
			print "    Trim Range test"
			sendCommand(sendfifoName, "Trim")
			recvMsg = recvCommand(recvfifoName)
		if self.threePtGain.isChecked():
			print "    Three Point Gain test"
			recvMsg = recvCommand(recvfifoName)
		if self.responseCurve.isChecked():
			print "    Response Curve test"
		if self.noiseOccup.isChecked():
			print "    Noise Occupancy test"
	#end run_tests

	def LVdisplay(self):
		text = str(self.LVmenu.currentText() )
		print 'Selected: ' + text
	#end LVdisplay

def launch():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())
#end launch

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
	

if __name__ == '__main__':
	launch()
