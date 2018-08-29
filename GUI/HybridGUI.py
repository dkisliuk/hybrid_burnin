#!/usr/python

'''
Hybrid Burn-in GUI

This GUI is intended make running the Hybrid burn-in cycle as intuitive as possible.

Author: Dylan Kisliuk
E-mail: dkisliuk@physics.utoronto.ca
'''

import sys
import os
import subprocess
from PyQt4 import QtGui, QtCore
from FIFOsharing import sendCommand, recvCommand, SendRecv #Local file
import HybridConfig as Config
SCTDAQ_ROOT = os.environ['SCTDAQ_ROOT']
ROOTSYS     = os.environ['ROOTSYS']
HYBRID_BURN = os.environ['PWD']
sys.path.insert(0, HYBRID_BURN+'/testManager')
from CheckTests import CheckTests

#FIFO
sendfifoName = HYBRID_BURN + "/GUI2DAQ.fifo"
recvfifoName = HYBRID_BURN + "/DAQ2GUI.fifo"

DEBUG = 1

#Window class defines the display, dimensions, buttons, etc.
class Window(QtGui.QMainWindow):
    def __init__(self):
        self.initX = 20
        self.initY = 20
        self.sizeX = 500
        self.sizeY = 500
        self.ITSDAQup = False
        self.LVup = False
        print '\nHybridGUI.py - Instantiating instance of Window class\n'
        super(Window, self).__init__()
        self.setGeometry(self.initX, self.initY, 
                         self.sizeX, self.sizeY)
        self.setWindowTitle("Hybrid Burn-in")
        self.setWindowIcon(QtGui.QIcon('hybridlogo.png') )
        self.home()
    #end __init__

    def home(self):
        #Quit, launch, Chip ID and HCC ID buttons
        quitX = 120
        quitY = 30
        quitBtn = QtGui.QPushButton("Quit", self)
        quitBtn.clicked.connect(self.exit_app)
        quitBtn.resize(quitX,quitY)
        quitBtn.move(self.sizeX - quitX, self.sizeY - quitY)
        self.startDAQ = QtGui.QPushButton("Launch ITSDAQ", self)
        self.startDAQ.clicked.connect(self.launchDAQ)
        self.startDAQ.resize(quitX,quitY)
        self.startDAQ.move(self.sizeX-quitX, self.sizeY-4*quitY)
        self.ChipBtn = QtGui.QPushButton("Chip ID", self)
        self.ChipBtn.clicked.connect(lambda: SendRecv(sendfifoName, recvfifoName, "ChipID"))
        self.ChipBtn.resize(quitX,quitY)
        self.ChipBtn.move(self.sizeX-quitX, self.sizeY-2*quitY)
        self.ChipBtn.setEnabled(False)
        self.HCCbtn = QtGui.QPushButton("HCC ID", self)
        self.HCCbtn.clicked.connect(lambda: SendRecv(sendfifoName, recvfifoName, "HCC"))
        self.HCCbtn.resize(quitX,quitY)
        self.HCCbtn.move(self.sizeX-quitX, self.sizeY-3*quitY)
        self.HCCbtn.setEnabled(False)

        #Tests box
        testsboxPosX = self.sizeX - 200
        testsboxPosY = 45
        testsboxLabel = QtGui.QLabel("Tests", self)
        testsboxLabel.move(testsboxPosX, testsboxPosY-20)

        #StrobeDelay stuff
        strobeLabel = QtGui.QLabel("Strobe Delay", self)
        strobeLabel.move(testsboxPosX+60, testsboxPosY)
        strobeLabel.resize(120, 25)
        self.strobeDelay = QtGui.QSpinBox(self)
        self.strobeDelay.move(testsboxPosX, testsboxPosY+4)
        self.strobeDelay.resize(50,20)
        self.strobeDelay.setValue(Config.strobeDelay)

        #TrimRange stuff
        trimLabel = QtGui.QLabel("Trim Range", self)
        trimLabel.move(testsboxPosX+60, testsboxPosY+20)
        trimLabel.resize(120, 25)
        self.trimRange = QtGui.QSpinBox(self)
        self.trimRange.move(testsboxPosX, testsboxPosY+24)
        self.trimRange.resize(50,20)
        self.trimRange.setValue(Config.trimRange)
        
        #ThreePtGain stuff
        threePtLabel = QtGui.QLabel("Three Point Gain", self)
        threePtLabel.move(testsboxPosX+60, testsboxPosY+40)
        threePtLabel.resize(120, 25)
        self.threePtGain = QtGui.QSpinBox(self)
        self.threePtGain.move(testsboxPosX, testsboxPosY+44)
        self.threePtGain.resize(50,20)
        self.threePtGain.setValue(Config.threePtGain)

        #ResponseCurve stuff
        responseLabel = QtGui.QLabel("Response Curve", self)
        responseLabel.move(testsboxPosX+60, testsboxPosY+60)
        responseLabel.resize(120, 25)
        self.responseCurve = QtGui.QSpinBox(self)
        self.responseCurve.move(testsboxPosX, testsboxPosY+64)
        self.responseCurve.resize(50,20)
        self.responseCurve.setValue(Config.responseCurve)

        #Noise Occupancy stuff
        noiseLabel = QtGui.QLabel("Noise Occupancy", self)
        noiseLabel.move(testsboxPosX+60, testsboxPosY+80)
        noiseLabel.resize(120, 25)
        self.noiseOccup = QtGui.QSpinBox(self)
        self.noiseOccup.move(testsboxPosX, testsboxPosY+84)
        self.noiseOccup.resize(50,20)
        self.noiseOccup.setValue(Config.noiseOccup)
        
        #Run button
        runX = 100
        runY = 30
        runBtn = QtGui.QPushButton("Run Tests", self)
        runBtn.clicked.connect(self.run_tests)
        runBtn.resize(runX, runY)
        runBtn.move(testsboxPosX, testsboxPosY+105)
        
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
        if self.LVup:
            sock = setClient()
            sock.sendall("Quit")
        sys.exit()
    #end exit_app

    def launchDAQ(self):
        if self.ITSDAQup == False:
            self.ITSDAQup = True
            recvMsg = SendRecv(sendfifoName, recvfifoName, "Start")
            self.ChipBtn.setEnabled(True)
            self.HCCbtn.setEnabled(True)
        else:
            print "ITSDAQ is already open"
    #end launchDAQ
            

    #Sends commands to RunTests.cpp server to run ITSDAQ tests
    def run_tests(self):
        print "HybridGUI.py - Opening fifo %s for sending" %sendfifoName
        #Only run the following commands if ITSDAQ has not yet been launched
        if self.ITSDAQup == False:
            self.ITSDAQup = True
            recvMsg = SendRecv(sendfifoName, recvfifoName, "Start")
            self.ChipBtn.setEnabled(True)
            self.HCCbtn.setEnabled(True)
            if DEBUG: print 'Received \'%s\'' %recvMsg
            recvMsg = SendRecv(sendfifoName, recvfifoName, "HCC")
            if DEBUG: print 'Received \'%s\'' %recvMsg
            recvMsg = SendRecv(sendfifoName, recvfifoName, "ChipID")
            if DEBUG: print 'Received \'%s\'' %recvMsg

        #TODO
        #Determine results file from date then CheckTests(fileName, testName)

        #Strobe Delay
        for i in range(self.strobeDelay.value() ):
            print "Running:    Strobe Delay test"
            recvMsg = SendRecv(sendfifoName, recvfifoName, "Strobe")
        #Trim Range
        for i in range(self.trimRange.value() ):
            print "Running:    Trim Range test"
            recvMsg = SendRecv(sendfifoName, recvfifoName, "Trim")
        #Three Point Gain (qCentre = 1fC)
        for i in range(self.threePtGain.value() ):
            print "Running:    Three Point Gain test"
            recvMsg = SendRecv(sendfifoName, recvfifoName, "ThreePt")
        #Response Curve (400 events)
        for i in range(self.responseCurve.value() ):
            print "Running:    Response Curve test"
            recvMsg = SendRecv(sendfifoName, recvfifoName, "RespCurve")
        #Noise Occupancy
        for i in range(self.noiseOccup.value() ):
            print "Running:    Noise Occupancy test"
            recvMsg = SendRecv(sendfifoName, recvfifoName, "NoiseOcc")
    #end run_tests

    def run_LV(self):
        if Config.raspIP is not None:
            #Launch server on raspberry pi
            #TODO
            '''
            if Config.raspPassword is not None:
                import paramiko
                command = "sudo python $LV_CONTROL/LV_server.py"
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy() )
                ssh.connect(port=Config.raspPort, hostname=Config.raspIP,
                            username=Config.raspHostName, password=Config.raspPassword)
                stdin, stdout, stderr = ssh.exec_command(command,timeout=10)
                #CHECK OUTPUT FOR DEBUGGING
                #stdout.
            '''
            
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
                    data += sock.recv(1024)
                    recvSize += len(data)
                print data
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
#end class Window

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
