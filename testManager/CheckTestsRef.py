#!/usr/bin/python

'''
Hybrid Burn-in reference file for tests.
Test outputs are compared with parameters in this configurable 'header' file.

Author: Dylan Kisliuk
E-mail: dkisliuk@physics.utoronto.ca
'''

DEBUG = 1

class StrobeDelay:
	#Strobe Delay parameters
	delay_low  = 15.0
	delay_high = 40.0

	def __init__(self):
		self.ID = "NONE"
		self.Delay = -1000000.0

	#Sets values for StrobeDelay object from dictionary 'test'
	def setValues(self, test, chip, stream=0):
		if stream == 0:
			self.ID    = test['extra_data']['identifiers']['stream0'][chip]
			self.Delay = test['JSON']['results']['STREAM0_DELAYS'][chip]
		elif stream == 1:
			self.ID    = test['extra_data']['identifiers']['stream1'][chip]
			self.Delay = test['JSON']['results']['STREAM1_DELAYS'][chip]
		else:
			print "CheckTestsRef - Invalid choice of stream for StrobeDelay"	

	def Print(self):
		print "  %s: %s" %(self.ID, self.Delay)

	def StrobeDelayCompare(self):
		return Window(self.delay_low, self.delay_high, self.Delay)

class ThreePointGain:
	(p0_low, p0_high)               = (20.0, 65.0)
	(p1_low, p1_high)               = (60.0, 100.0)
	(gain_low, gain_high)           = (70.0, 90.0)
	(gainrms_low, gainrms_high)     = (3.0, 5.0)
	(offset_low, offset_high)       = (70.0, 90.0)
	(offsetrms_low, offsetrms_high) = (3.0, 5.0)
	(vt50_low, vt50_high)           = (125.0, 135.0)
	(vt50rms_low, vt50rms_high)     = (1.2, 1.8)
	(innse_low, innse_high)         = (400.0, 480.0)
	(innserms_low, innserms_high)   = (20.0, 30.0)
	(outnse_low, outnse_high)       = (5.5, 6.3)

	def __init__(self):
		self.ID = "NONE"
		self.P0 = -1000000.0
		self.P1 = -1000000.0
		self.Gain = -1000000.0
		self.GainRMS = -1000000.0
		self.Offset = -1000000.0
		self.OffsetRMS = -1000000.0
		self.VT50 = -1000000.0
		self.VT50RMS = -1000000.0
		self.InNoise = -1000000.0
		self.InNoiseRMS = -1000000.0
		self.OutNoise = -1000000.0

	def setValues(self, test, chip, stream=0):
		if stream == 0:
			self.ID         = test['extra_data']['identifiers']['stream0'][chip]
			self.P0         = test['JSON']['results']['STREAM0_P0'][chip]
			self.P1         = test['JSON']['results']['STREAM0_P1'][chip]
			self.Gain       = test['JSON']['results']['STREAM0_GAIN'][chip]
			self.GainRMS    = test['JSON']['results']['STREAM0_GAIN_RMS'][chip]
			self.Offset     = test['JSON']['results']['STREAM0_OFFSET'][chip]
			self.OffsetRMS  = test['JSON']['results']['STREAM0_OFFSET_RMS'][chip]
			self.VT50       = test['JSON']['results']['STREAM0_VT50'][chip]
			self.VT50RMS    = test['JSON']['results']['STREAM0_VT50_RMS'][chip]
			self.InNoise    = test['JSON']['results']['STREAM0_INNSE'][chip]
			self.InNoiseRMS = test['JSON']['results']['STREAM0_INNSE_RMS'][chip]
			self.OutNoise   = test['JSON']['results']['STREAM0_OUTNSE'][chip]
		elif stream == 1:
			self.ID         = test['extra_data']['identifiers']['stream1'][chip]
			self.P0         = test['JSON']['results']['STREAM1_P0'][chip]
			self.P1         = test['JSON']['results']['STREAM1_P1'][chip]
			self.Gain       = test['JSON']['results']['STREAM1_GAIN'][chip]
			self.GainRMS    = test['JSON']['results']['STREAM1_GAIN_RMS'][chip]
			self.Offset     = test['JSON']['results']['STREAM1_OFFSET'][chip]
			self.OffsetRMS  = test['JSON']['results']['STREAM1_OFFSET_RMS'][chip]
			self.VT50       = test['JSON']['results']['STREAM1_VT50'][chip]
			self.VT50RMS    = test['JSON']['results']['STREAM1_VT50_RMS'][chip]
			self.InNoise    = test['JSON']['results']['STREAM1_INNSE'][chip]
			self.InNoiseRMS = test['JSON']['results']['STREAM1_INNSE_RMS'][chip]
			self.OutNoise   = test['JSON']['results']['STREAM1_OUTNSE'][chip]
		else:
			print "CheckTestsRef - Invalid choice of stream for ThreePointGain"

	def Print(self):
		print "ID:          %s" %self.ID
		print "P0:          %d" %self.P0
		print "P1:          %d" %self.P1
		print "Gain:        %d" %self.Gain
		print "GainRMS:     %d" %self.GainRMS
		print "Offset:      %d" %self.Offset
		print "OffsetRMS:   %d" %self.OffsetRMS
		print "VT50:        %d" %self.VT50
		print "VT50RMS:     %d" %self.VT50RMS
		print "InNoise:     %d" %self.InNoise
		print "InNoiseRMS:  %d" %self.InNoiseRMS
		print "OutNoise:    %d" %self.OutNoise

	def p0Compare(self):
		return Window(self.p0_low, self.p0_high, self.P0)

	def p1Compare(self):
		return Window(self.p1_low, self.p1_high, self.P1)

	def gainCompare(self):
		return Window(self.gain_low, self.gain_high, self.Gain)

	def gainrmsCompare(self):
		return Window(self.gainrms_low, self.gainrms_high, self.GainRMS)

	def offsetCompare(self):
		return Window(self.offset_low, self.offset_high, self.Offset)

	def offsetrmsCompare(self):
		return Window(self.offsetrms_low, self.offsetrms_high, self.OffsetRMS)

	def vt50Compare(self):
		return Window(self.vt50_low, self.vt50_high, self.VT50)

	def vt50rmsCompare(self):
		return Window(self.vt50rms_low, self.vt50rms_high, self.VT50RMS)

	def innseCompare(self):
		return Window(self.innse_low, self.innse_high, self.InNoise)

	def innsermsCompare(self):
		return Window(self.innserms_low, self.innserms_high, self.InNoiseRMS)

	def outnseCompare(self):
		return Window(self.outnse_low, self.outnse_high, self.OutNoise)

	#Do all comparisons simultaneously. Or choose which parameters you don't care about by setting argument to False
	def compareAll(self,P0=True,P1=True,Gain=True,GainRMS=True,Offset=True,OffsetRMS=True,VT50=True,VT50RMS=True,InNoise=True,InNoiseRMS=True,OutNoise=True):
		if P0 and not self.p0Compare(): return False
		if P1 and not self.p1Compare(): return False
		if Gain and not self.gainCompare(): return False
		if GainRMS and not self.gainrmsCompare(): return False
		if Offset and not self.offsetCompare(): return False
		if OffsetRMS and not self.offsetrmsCompare(): return False
		if VT50 and not self.vt50Compare(): return False
		if VT50RMS and not self.vt50rmsCompare(): return False
		if InNoise and not self.innseCompare(): return False
		if InNoiseRMS and not self.innsermsCompare(): return False
		if OutNoise and not self.outnseCompare(): return False
		return True
	
class ResponseCurve(ThreePointGain):
	(p2_low, p2_high) = (-550.0, -450.0)

	def __init__(self):
		ThreePointGain.__init__(self)
		self.P2 = -1000000.0

	def setValues(self, test, chip, stream=0):
		ThreePointGain.setValues(self, test, chip, stream)
		if stream == 0:
			self.P2 = test['JSON']['results']['STREAM0_P2'][chip]
		elif stream == 1:
			self.P2 = test['JSON']['results']['STREAM1_P2'][chip]
		else:
			print "CheckTestsRef - Invalid choice of stream for ResponseCurve"

	def p2Compare(self):
		return Window(self.p2_low, self.p2_high, self.P2)

	def compareAll(self,P0=True,P1=True,P2=True,Gain=True,GainRMS=True,Offset=True,OffsetRMS=True,VT50=True,VT50RMS=True,InNoise=True,InNoiseRMS=True,OutNoise=True):
		if P2 and not self.p2Compare(): return False 
		if not ThreePointGain.compareAll(self,P0,P1,Gain,GainRMS,Offset,OffsetRMS,VT50,VT50RMS,InNoise,InNoiseRMS,OutNoise): return False
		return True 

	def Print(self):
		print "ID:          %s" %self.ID
		print "P0:          %d" %self.P0
		print "P1:          %d" %self.P1
		print "P2:          %d" %self.P2
		print "Gain:        %d" %self.Gain
		print "GainRMS:     %d" %self.GainRMS
		print "Offset:      %d" %self.Offset
		print "OffsetRMS:   %d" %self.OffsetRMS
		print "VT50:        %d" %self.VT50
		print "VT50RMS:     %d" %self.VT50RMS
		print "InNoise:     %d" %self.InNoise
		print "InNoiseRMS:  %d" %self.InNoiseRMS
		print "OutNoise:    %d" %self.OutNoise

def Window(low, high, value):
	if value < high and value > low:
		return True
	else:
		return False
