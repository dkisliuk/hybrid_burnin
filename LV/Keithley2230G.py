#!/usr/bin/python

'''
Defines a class to control Keithley2230G model low voltage power supply
Read out is via USB-USB (serial) connection using pyvisa-py library
Also has a 'main' program for testing purposes

**NOTES**
The Keithley2230G is very finnicky when it comes to reading out things through pyvisa-py.
For this reason, many 'hacky' procedures are implemented to avoid exceptions that arise due to reading things

Author: Dylan Kisliuk (dkisliuk@physics.utoronto.ca)
Date: May 2018
'''

import visa
import time
import sys
DEBUG = 0

class Keithley2230G:
    def __init__(self, name='USB0::1510::8752::9103795::0::INSTR'):
        self.resources = visa.ResourceManager('@py')
        if DEBUG:
            print('Resources available:')
            print(self.resources.list_resources() )
	    print
        #To check the 'name' of your device, run the above commands
        try:
            self.device = self.resources.open_resource(name)
        except ValueError:
            print 'Could not find device %s. Instantiate class object with:' %name
            print '>>>device = Keithley2230G(name="USB0::0000::1111::2345678::0::INSTR")'
            self.device = None
            return
        self.device.write('SYST:REM\n') #Need this to turn on REMote mode. Absolutely critical
        self.device.write('*RST; *ESE; :STATUS:PRESET; *CLS') #Start with a clean slate

        #Voltage set for each channel
        self.volt = [0, 0, 0]
        #Current set for each channel
        self.curr = [0, 0, 0]
	
    #This is a general command function
    # 'comm' should be a string with the command you wish to perform
    def sendCommand(self, comm, mode='write'):
        command = comm + '\n'
        if mode == 'query':
            return self.device.query(command)
        elif mode == 'read':
            return self.device.read(command)
        elif mode == 'write':
            return self.device.write(command) 

    #Print what this device is
    def IDN(self):
        print 'IDN'
        flag = -1
        while flag is -1:
            try:
                self.device.close()
                self.device.open()
                print self.device.query('*IDN?\n')
                flag = 0
            except Exception:
                flag = -1

    #Turn ON output 
    def powerON(self):
        print 'Powering ON'
        self.sendCommand(':OUTP:STAT 1', mode='write')

    #Turn OFF output
    def powerOFF(self):
        print 'Powering OFF'
        self.sendCommand(':OUTP:STAT 0', mode='write')

    #Read voltage from channel 'chan' (1 2 or 3) and return
    def readVOLT(self, chan=1):
        self.sendCommand(':INST:SEL CH%d' %chan, 'write')
        self.sendCommand(':MEAS:SCAL:VOLT:DC?', 'write')
        self.sendCommand(':FETC:VOLT:DC?', 'write')
        #Only way I could figure out how to read is by closing then opening again
        try:
            self.device.close()
            self.device.open()
            return self.device.read().split('\n')[0] #For some reason this operation gives a bunch of garbage after the voltage
        except Exception as e:
            return False

    #Read current from channel 'chan' (1 2 or 3) and return
    def readCURR(self, chan=1):
        self.sendCommand(':INST:SEL CH%d' %chan, 'write')
        self.sendCommand(':MEAS:SCAL:CURR:DC?', 'write')
        self.sendCommand(':FETC:CURR:DC?', 'write')
        #Only way I could figure out how to read is by closing then opening again
        try:
            self.device.close()
            self.device.open()
            return self.device.read().split('\n')[0] #For some reason this operation gives a bunch of garbage after the current
        except Exception as e:
            return False

    # Set voltage for device's three channels
    def setVOLT(self, volt1='none', volt2='none', volt3='none'):
        if volt1 is not 'none':
             self.volt[0] = volt1
        if volt2 is not 'none':
             self.volt[1] = volt2
        if volt3 is not 'none':
             self.volt[2] = volt3
        if DEBUG: print 'Setting Voltages to %f  %f  %f'  %(self.volt[0], self.volt[1], self.volt[2])
        self.device.write(':APP:VOLT %f,%f,%f\n' %(self.volt[0], self.volt[1], self.volt[2]) )

    #Ramp voltage over a period of time
    def rampVOLT(self, chan=1, stepSize=1.0, wait=1.0, finalVolt=5.0):
        if DEBUG: print 'Ramping voltage of channel %d' %chan
        if chan is not 1 and chan is not 2 and chan is not 3:
            print '"chan" must be 1, 2, or 3'
            return
        #Ramp up if stepSize > 0 and Ramp down if stepSize < 0
        while (self.volt[chan-1] < finalVolt if stepSize > 0 else self.volt[chan-1] > finalVolt):
             stepVolt = self.volt[chan-1] + stepSize
             if (stepVolt > finalVolt if stepSize >0 else stepVolt < finalVolt):
                 stepVolt = finalVolt
             if chan == 1:
                 self.setVOLT(volt1=stepVolt) 
             if chan == 2:
                 self.setVOLT(volt2=stepVolt)
             if chan == 3:
                 self.setVOLT(volt3=stepVolt)
             time.sleep(wait)

    # Set current for device's three channels
    def setCURR(self, curr1='none', curr2='none', curr3='none'):
        if curr1 is not 'none':
             self.curr[0] = curr1
        if curr2 is not 'none':
             self.curr[1] = curr2
        if curr3 is not 'none':
             self.curr[2] = curr3
        if DEBUG: print 'Setting Currents to %f  %f  %f'  %(self.curr[0], self.curr[1], self.curr[2])
        self.device.write(':APP:CURR %f,%f,%f\n' %(self.curr[0], self.curr[1], self.curr[2]) )

    def localMode(self):
        if DEBUG: print 'Setting to local mode'
        self.sendCommand(':SYST:LOC', 'write')

    def remoteMode(self):
        if DEBUG: print 'Setting to remote mode'
        self.sendCommand(':SYST:REM', 'write')
#end Keithley2230G class definition

# 'device' is the instance of Keithley2230G object you want read
def getVOLT(device, chan=1):
    if DEBUG: print 'Read Voltage of Channel %d' %chan
    voltage = False
    while voltage == False:
        voltage = device.readVOLT(chan) #Returns false in case of exception
    return voltage

# 'device' is the instance of Keithley2230G object you want read
def getCURR(device, chan=1):
    if DEBUG: print 'Read Current of Channel %d' %chan
    current = False
    while current == False:
        current = device.readCURR(chan) #Returns false in case of exception
    return current

#Class and function testing
if __name__ == '__main__':
    print 'Initiating class tests:\n'
    keith = Keithley2230G()
    if keith.device is None:
        sys.exit()
    keith.IDN()
    keith.powerON()

    #Set voltage of each channel
    keith.setVOLT(volt1=1.3, volt2=0.5, volt3=0.3)
    time.sleep(1)

    #Set current of each channel
    keith.setCURR(curr1=0.5, curr3=1.5)
    time.sleep(1)

    #Read voltage of each channel
    print getVOLT(keith, chan=1)
    print getVOLT(keith, chan=2)
    print getVOLT(keith, chan=3)

    #Read current of each channel
    print getCURR(keith, chan=1)
    print getCURR(keith, chan=2)
    print getCURR(keith, chan=3)

    #Ramp voltage of channel 1
    keith.rampVOLT(chan=1, finalVolt=10.0)
    keith.rampVOLT(chan=1, stepSize=-1, finalVolt = 0.4)

    time.sleep(1)
    keith.powerOFF()
    keith.localMode()

