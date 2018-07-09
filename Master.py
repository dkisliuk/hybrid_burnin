#!/usr/python

#from CommonVars import * #Contains imports and environment variables
import sys
import os
import ROOT
HOME = os.environ['HOME']
try:
	SCTDAQ_ROOT = os.environ['SCTDAQ_ROOT']
	ROOTSYS     = os.environ['ROOTSYS']
except:
	print 'One of the following environment variables is not set:'
	print '    SCTDAQ_ROOT'
	print '    ROOTSYS'
	print 'Please set appropriately.'
	sys.exit()
sys.path.insert(0, HOME+'/hybrid_burnin/GUI')
import HybridGUI
from PyQt4 import QtGui

#Main program
def main():
	print '#######################################################'
	print 'Master.py - Starting master program for hybrid burn-in.'

	#Fork
	pid = os.fork()
	if pid == 0: #Child process
		#Launch GUI
		GUIpid = os.getpid()
		print 'Master.py - Opening GUI display'
		app = QtGui.QApplication(sys.argv)
		display = HybridGUI.Window()
		sys.exit(app.exec_())



	else: #Parent process
		#Launch ITSDAQ
		ITSDAQpid = os.getpid()
		print 'Master.py - Launching ITSDAQ'
		#os.chdir(SCTDAQ_ROOT)
		#ROOT.gInterpreter.ProcessLine(ROOTSYS+'/bin/root -l Stavelet.cpp')
		#os.system(ROOTSYS+'/bin/root -l Stavelet.cpp')

main()
