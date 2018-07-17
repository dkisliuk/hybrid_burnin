#!/usr/bin/python

#Initial LV settings
CH1Volt = 4.50
CH1Curr = 1.50
CH2Volt = 0.00
CH2Curr = 0.00
CH3Volt = 1.55
CH3Curr = 2.00
#Initial device. Options are "Keithley2230G", "Instek", or "Sorensen"
deviceName = "Keithley2230G"

#Tests to be 'checked' on startup
strobeDelay = 1
trimRange = 0
threePtGain = 0
responseCurve = 0
noiseOccup = 0

#Run tests on startup without user clicking "Run Tests"?
#Declare with 'True' or 'False'
runOnStart = False

#Raspberry pi info
#Can set raspIP to None if you don't have one
raspIP = "128.100.75.214"
raspHostName = "pi"
port = 6464
