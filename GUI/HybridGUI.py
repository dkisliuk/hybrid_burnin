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
import shutil
from PyQt4 import QtGui, QtCore
from FIFOsharing import sendCommand, recvCommand, SendRecv #Local file
import HybridConfig as Config
SCTDAQ_ROOT = os.environ['SCTDAQ_ROOT']
SCTDAQ_VAR  = os.environ['SCTDAQ_VAR']
ROOTSYS     = os.environ['ROOTSYS']
HYBRID_BURN = os.environ['PWD']
sys.path.insert(0, HYBRID_BURN+'/testManager')
from CheckTests import CheckTests
from MiscFuncs import *

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
        self.setFonts()
        if os.path.exists(sendfifoName) and os.path.exists(recvfifoName): pass
        else:
	        os.mkfifo(sendfifoName)
	        os.mkfifo(recvfifoName)
        print '\nHybridGUI.py - Instantiating instance of Window class\n'
        super(Window, self).__init__()
        self.setGeometry(self.initX, self.initY, 
                         self.sizeX, self.sizeY)
        self.setWindowTitle("Hybrid Burn-in")
        self.setWindowIcon(QtGui.QIcon('hybridlogo.png') )
        self.home()
    #end __init__

    def setFonts(self):
        self.headerFont = QtGui.QFont()
        self.headerFont.setPointSize(14)
        self.headerFont.setBold(True)
        self.statusFont = QtGui.QFont()
        self.statusFont.setPointSize(16)

        #self.redPalette = QtGui.QPalette()
        #self.redPalette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.red)

    #################################################################################################
    #Setup the whole GUI and then display it
    def home(self):
        #Status line
        status_X = 0
        status_Y = 0
        self.statusText = QtGui.QLabel("STATUS: Ready", self)
        self.statusText.setFont(self.statusFont)
        self.statusText.setStyleSheet('color: green')
        self.statusText.move(status_X, status_Y)
        self.statusText.resize(500, 25)
        self.statusText.setAutoFillBackground(True)

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
        testsboxLabel.setFont(self.headerFont)

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
        killBtn = QtGui.QPushButton("Kill Tests", self)
        #TODO add functionality
        #killBtn.clicked.connect(self.kill_runs)
        killBtn.resize(runX, runY)
        killBtn.move(testsboxPosX, testsboxPosY+135)
        
        #LV supply
        LV_X = 0
        LV_Y = 50
        LVlabel = QtGui.QLabel("LV Supply", self)
        LVlabel.move(LV_X+4, LV_Y-25)
        LVlabel.setFont(self.headerFont)
        VoltLabel = QtGui.QLabel("Volt (V)", self)
        VoltLabel.move(LV_X+50, LV_Y+25)
        CurrLabel = QtGui.QLabel("Curr (A)", self)
        CurrLabel.move(LV_X+110, LV_Y+25)
        LVbutton = QtGui.QPushButton("Set LV", self)
        LVbutton.move(LV_X+60, LV_Y+140)
        LVbutton.clicked.connect(self.run_LV)
        self.LVmenu = QtGui.QComboBox(self)
        self.LVmenu.move(LV_X, LV_Y)
        self.LVmenu.resize(150, 30)
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

        #Module/Hybrid Information
        module_X = 0
        module_Y = 220
        moduleLabel = QtGui.QLabel("Module Info", self)
        moduleLabel.move(module_X, module_Y)
        moduleLabel.resize(150, 30)
        moduleLabel.setFont(self.headerFont)
        moduleNameText = QtGui.QLabel("Name:", self)
        moduleNameText.move(module_X, module_Y+30)
        self.moduleName = QtGui.QLineEdit(self)
        self.moduleName.move(module_X+60, module_Y+30)
        self.moduleName.resize(150, 30)
        self.moduleName.setText(Config.moduleName)
        moduleConfigText = QtGui.QLabel("Config:", self)
        moduleConfigText.move(module_X, module_Y+60)
        self.moduleConfig = QtGui.QLineEdit(self)
        self.moduleConfig.move(module_X+60, module_Y+60)
        self.moduleConfig.resize(150,30)
        self.moduleConfig.setText(Config.moduleConfig)
        moduleLoad = QtGui.QPushButton("Load Config File", self)
        moduleLoad.move(module_X+60, module_Y+90)
        moduleLoad.resize(150, 30)
        moduleLoad.clicked.connect(self.selectConfig)

        #Save the current configuration to the HybridConfig file
        saveConfig = QtGui.QPushButton("Save Config", self)
        saveConfig.move(0, self.sizeY-30)
        saveConfig.resize(120,30)
        saveConfig.clicked.connect(self.saveConfig)

        #Display GUI
        self.show()

        #Run tests immediately if 'runOnStart' in config file is true
        if(Config.runOnStart):
            #TODO add functionality to turn on LV
            self.run_tests()
    #end home
    ####################################################################################################################

    #Update the STATUS text at the top of the Window and then show()
    def statusUpdate(self, text, color='green'):
        self.statusText.setText(text)
        self.statusText.setStyleSheet('color: ' + color)
        self.show()
    #end statusUpdate

    #Exit everything
    def exit_app(self):
        print("HybridGUI.py - Exiting")
        sendCommand(sendfifoName, "Quit")
        if self.LVup:
            sock = setClient()
            sock.sendall("Quit")
        os.remove(sendfifoName)
        os.remove(recvfifoName)
        sys.exit()
    #end exit_app

    #Update the HybridConfig file with the current settings
    def saveConfig(self):
        lines = open(HYBRID_BURN + '/GUI/HybridConfig.py').readlines()
        tempFile = open('temp.txt', 'w')
        for line in lines:
            if line.count('='):
                if   line.count("CH1Volt"): line = changeLineValue(line, self.CH1Volt.value() )
                elif line.count("CH2Volt"): line = changeLineValue(line, self.CH2Volt.value() )
                elif line.count("CH3Volt"): line = changeLineValue(line, self.CH3Volt.value() )
                elif line.count("CH1Curr"): line = changeLineValue(line, self.CH1Curr.value() )
                elif line.count("CH2Curr"): line = changeLineValue(line, self.CH2Curr.value() )
                elif line.count("CH3Curr"): line = changeLineValue(line, self.CH3Curr.value() )
                elif line.count("deviceName"): line = changeLineValue(line, str(self.LVmenu.currentText() ) )
                elif line.count("strobeDelay"  ): line = changeLineValue(line, self.strobeDelay.value() )
                elif line.count("trimRange"    ): line = changeLineValue(line, self.trimRange.value() )
                elif line.count("threePtGain"  ): line = changeLineValue(line, self.threePtGain.value() )
                elif line.count("responseCurve"): line = changeLineValue(line, self.responseCurve.value() )
                elif line.count("noiseOccup"   ): line = changeLineValue(line, self.noiseOccup.value() )
                elif line.count("moduleName"  ): line = changeLineValue(line, str(self.moduleName.text() ) )
                elif line.count("moduleConfig"): line = changeLineValue(line, str(self.moduleConfig.text() ) )
            tempFile.write(line)
        shutil.move('temp.txt', HYBRID_BURN + '/GUI/HybridConfig.py')

    #Launch ITSDAQ without running tests
    def launchDAQ(self):
        if self.ITSDAQup == False:
            self.ITSDAQup = True
            self.statusUpdate("Opening ITSDAQ", color='orange')
            self.ChipBtn.setEnabled(True)
            self.HCCbtn.setEnabled(True)
            self.startDAQ.setEnabled(False)
            QtGui.QApplication.processEvents()
            recvMsg = SendRecv(sendfifoName, recvfifoName, "Start")
            self.statusUpdate("Opened ITSDAQ", color='green')
        else:
            print "ITSDAQ is already open"
    #end launchDAQ
            

    #TODO run as background process. Add KILL TESTS functionality
    #Sends commands to RunTests.cpp server to run ITSDAQ tests
    def run_tests(self):
        print "HybridGUI.py - Opening fifo %s for sending" %sendfifoName
        self.statusUpdate("STATUS: Running Tests", color='orange')
        #Only run the following commands if ITSDAQ has not yet been launched
        if self.ITSDAQup == False:
            self.ITSDAQup = True
            recvMsg = SendRecv(sendfifoName, recvfifoName, "Start")
            self.ChipBtn.setEnabled(True)
            self.HCCbtn.setEnabled(True)
            self.startDAQ.setEnabled(False)
            if DEBUG: print 'Received \'%s\'' %recvMsg
            recvMsg = SendRecv(sendfifoName, recvfifoName, "HCC")
            if DEBUG: print 'Received \'%s\'' %recvMsg
            recvMsg = SendRecv(sendfifoName, recvfifoName, "ChipID")
            if DEBUG: print 'Received \'%s\'' %recvMsg

        #Strobe Delay
        for i in range(self.strobeDelay.value() ):
            self.statusUpdate("STATUS: Running Strobe Delay - " + str(i+1) + '/' + str(self.strobeDelay.value() ), color='orange')
            print bcolors.OKGREEN + "Running:    Strobe Delay test" + bcolors.ENDC
            QtGui.QApplication.processEvents()
            recvMsg = SendRecv(sendfifoName, recvfifoName, "Strobe")
            #Determine results file from date then CheckTests(fileName, testName)
            recordTest(testName = 'STROBE_DELAY')
        #Trim Range
        for i in range(self.trimRange.value() ):
            self.statusUpdate("STATUS: Running Trim Range - " + str(i+1) + '/' + str(self.trimRange.value() ), color='orange')
            print bcolors.OKGREEN + "Running:    Trim Range test" + bcolors.ENDC
            QtGui.QApplication.processEvents()
            recvMsg = SendRecv(sendfifoName, recvfifoName, "Trim")
        #Three Point Gain (qCentre = 1fC)
        for i in range(self.threePtGain.value() ):
            self.statusUpdate("STATUS: Running Three Point Gain - " + str(i+1) + '/' + str(self.threePtGain.value() ), color='orange')
            print bcolors.OKGREEN + "Running:    Three Point Gain test" + bcolors.ENDC
            QtGui.QApplication.processEvents()
            recvMsg = SendRecv(sendfifoName, recvfifoName, "ThreePt")
            recordTest(testName = 'THREE_POINT_GAIN')
        #Response Curve (400 events)
        for i in range(self.responseCurve.value() ):
            self.statusUpdate("STATUS: Running Response Curve - " + str(i+1) + '/' + str(self.responseCurve.value() ), color='orange')
            print bcolors.OKGREEN + "Running:    Response Curve test" + bcolors.ENDC
            QtGui.QApplication.processEvents()
            recvMsg = SendRecv(sendfifoName, recvfifoName, "RespCurve")
            recordTest(testName = 'RESPONSE_CURVE')
        #Noise Occupancy
        for i in range(self.noiseOccup.value() ):
            self.statusUpdate("STATUS: Running Noise Occupancy - " + str(i+1) + '/' + str(self.noiseOccup.value() ), color='orange')
            print bcolors.OKGREEN + "Running:    Noise Occupancy test" + bcolors.ENDC
            QtGui.QApplication.processEvents()
            recvMsg = SendRecv(sendfifoName, recvfifoName, "NoiseOcc")

        self.statusUpdate("STATUS: Ready", color='green')
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
                if DEBUG: print "HybridGUI.py - Sending message to LV server: %s" %message
                sock.settimeout(5.0)
                sock.send(message)
                response = ''
                if DEBUG: print "HybridGUI.py - Waiting on response from LV server..."
                sock.settimeout(5.0)
                response += sock.recv(1024)
                if response == "ACK\0":
                    print bcolors.OKGREEN + "HybridGUI.py - LV successfully set" + bcolors.ENDC
                else:
                    print bcolors.FAIL + "HybridGUI.py - Problem setting up LV" + bcolors.ENDC
            finally:
                print "HybridGUI.py - Closing socket"
                sock.close()        
    #end run_LV

    def LVdisplay(self):
        text = str(self.LVmenu.currentText() )
        print 'Selected: ' + text
    #end LVdisplay

    def selectConfig(self):
        configFile = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        shutil.copy(configFile, SCTDAQ_VAR + '/config/st_system_config.dat')
        self.moduleConfig.setText(configFile)
        print "Set " + configFile + " as new config file for ITSDAQ"
    #end selectConfig
        
#end class Window

def launch():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
#end launch

if __name__ == '__main__':
    launch()
