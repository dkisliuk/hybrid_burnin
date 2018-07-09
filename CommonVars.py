#!/usr/python

'''
This file includes all the import statements and environment variable declarations for python
'''

import sys
import os
HOME = os.environ['HOME']
try:
	SCTDAQ_ROOT = os.environ['SCTDAQ_ROOT']
except:
	print 'SCTDAQ_ROOT environment variable is not set. Please set it appropriately.'
	sys.exit()
sys.path.insert(0, HOME+'/hybrid_burnin/GUI')
import HybridGUI
