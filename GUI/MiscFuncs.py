#!/usr/python

import os
import sys
SCTDAQ_VAR  = os.environ['SCTDAQ_VAR']
HYBRID_BURN = os.environ['PWD']
sys.path.insert(0, HYBRID_BURN+'/testManager')
from CheckTests import CheckTests
import HybridConfig as Config

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#Determine the name of the results files created today
def getResultsFiles():
    import datetime
    now = datetime.datetime.now()
    if now.day < 10: day = '0%d' % now.day
    else:            day = str(now.day)
    if now.month < 10: month = '0%d' %now.month
    else:              month = str(now.month)
    year = str(now.year)
    date = year + month + day
    #return date

    resultsFileNames = []
    lines = open(SCTDAQ_VAR + '/config/st_system_config.dat').readlines()
    for line in lines:
        if line.count('#', 0, 1):
            continue
        if line.count('Module', 0, len('Module') ):
            modFile = line.split()[-2]
            resultsFile = modFile + '_' + date + '.txt'
            resultsFileNames.append(resultsFile)
    return resultsFileNames
#end getResultsFiles

def recordTest(testName='STROBE_DELAY'):
    resultsFileNames = getResultsFiles()
    for resultsFile in resultsFileNames:
        path = SCTDAQ_VAR + '/results/' + resultsFile
        if os.path.isfile(path):
            status = CheckTests(path, testName)
        else:
            print bcolors.FAIL + 'File %s was not created. Ensure you can read HCC and Chip IDs' %(path) + bcolors.ENDC
            return 1
        if status:
            print bcolors.FAIL + 'Could not save results of %s test from file %s to database' %(testName, resultsFile) + bcolors.ENDC
    return 0
#end recordTest

def setClient():
    #Setup client
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (Config.raspIP, Config.port)
    print "HybridGUI.py - Connecting to %s port %s" %server_address
    sock.connect(server_address)
    return sock
#end setClient

def changeLineValue(line, val):
    pieces = line.split()
    if isinstance(val, basestring): #Strings should be in quotes
        pieces[-1] = '"%s"' %val
    else:
        pieces[-1] = str(val)
    line = ' '.join(pieces)
    return line + '\n'
