#!/usr/bin/python

'''
Hybrid Burn-in file for checking output from ITSDAQ tests.
Test output parameters are compared with a reference file CheckTestsRef.py

Author: Dylan Kisliuk
E-mail: dkisliuk@physics.utoronto.ca
'''

from ITSDAQTestClasses import ResultsSummaryFile
import CheckTestsRef as Ref
import WriteTests

DEBUG = 0

#Get the tests from output file
def GetTests(fileName):
	try:
		f = open(fileName, 'r')
		lines = f.readlines()
		f.close()
		tests = getTests(lines, nABC)
		return tests
	except IOError:
		ERROR("CheckTests.py - Could not find file '%s'." %fileName)
		return 1
#end def GetTests

def CheckTests(fileName, testName="STROBE_DELAY"):
	#Read output from ITSDAQ output files
	testSummary = ResultsSummaryFile(fileName)
	testSummary.getTests()
	results = testSummary.returnTests()

	if DEBUG: print results

	#Read tests array backwards to read latest tests
	for j in range(len(results) ):
		test = results[-j-1]
		print		
		if test['JSON']['testType'] == testName:
			if testName == "STROBE_DELAY":
				for i in range(len(test['JSON']['results']['STREAM0_DELAYS']) ):
					stream0 = Ref.StrobeDelay()
					stream0.setValues(test, i, stream=0)
					WriteTests.writeInfluxDB('daqload', stream0, stream=0)

					stream1 = Ref.StrobeDelay()
					stream1.setValues(test, i, stream=1)
					WriteTests.writeInfluxDB('daqload', stream1, stream=1)

					if DEBUG:
						print testName
						print "STREAM 0:"
						stream0.Print()
						if stream0.StrobeDelayCompare():
							print "S0:  CHIP %s - PASS" %stream0.ID
						else:
							print "S0:  CHIP %s - FAIL" %stream0.ID
						print
						print "STREAM 1:"
						stream0.Print()
						print
						if stream1.StrobeDelayCompare():
							print "S1:  CHIP %s - PASS" %stream0.ID
						else:
							print "S1:  CHIP %s - FAIL" %stream0.ID
						print
				break #Only read latest test

			elif testName == "THREE_POINT_GAIN":
				for i in range(len(test['JSON']['results']['STREAM1_INNSE']) ):
					stream0 = Ref.ThreePointGain()
					stream0.setValues(test, i, stream=0)
					WriteTests.writeInfluxDB('daqload', stream0, stream=0)

					stream1 = Ref.ThreePointGain()
					stream1.setValues(test, i, stream=1)
					WriteTests.writeInfluxDB('daqload', stream1, stream=1)

					if DEBUG:
						print testName
						print "STREAM 0:"
						stream0.Print()
						print
						print "STREAM 1:"
						stream1.Print()
						print
				break #Only read latest test
					
			elif testName == "RESPONSE_CURVE":
				for i in range(len(test['JSON']['results']['STREAM0_P1']) ):
					stream0 = Ref.ResponseCurve()
					stream0.setValues(test, i, stream=0)
					WriteTests.writeInfluxDB('daqload', stream0, stream=0)

					stream1 = Ref.ResponseCurve()
					stream1.setValues(test, i, stream=1)
					WriteTests.writeInfluxDB('daqload', stream1, stream=1)

					if DEBUG:
						print testName
						print "STREAM 0:"
						stream0.Print()
						print
						print "STREAM 1:"
						stream1.Print()
						print
				break #Only read latest test
		#end if		
	#end for
#end def CheckTests
