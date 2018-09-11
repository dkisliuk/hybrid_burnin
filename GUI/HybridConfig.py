#!/usr/bin/python

#Initial LV settings
CH1Volt = 4.5
CH1Curr = 1.5
CH2Volt = 0.0
CH2Curr = 0.0
CH3Volt = 1.55
CH3Curr = 2.0
#Initial device. Options are "Keithley2230G", "Instek", or "Sorensen"
deviceName = "Keithley2230G"

#Run test this many times
strobeDelay = 5
trimRange = 0
threePtGain = 0
responseCurve = 0
noiseOccup = 0

#Run tests on startup without user clicking "Run Tests"?
#Declare with 'True' or 'False'
runOnStart = False

#Module/Hybrid information
moduleName = "Celestica_DAQload"
moduleConfig = "/home/ITSDAQ/itsvar/config/st_system_config.dat"

#Raspberry pi info
#Can set raspIP to None if you don't have one
raspIP = "128.100.75.214"
raspPassword = "merlin"
raspHostName = "pi"
raspPort = 22
port = 6464
