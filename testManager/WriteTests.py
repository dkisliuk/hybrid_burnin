#!/usr/bin/python

'''
Hybrid Burn-in file for writing parameters from tests to an InfluxDB

Author: Dylan Kisliuk
E-mail: dkisliuk@physics.utoronto.ca
'''

import sys
try:
    from influxdb import InfluxDBClient
except ImportError:
    print "Could not find the 'influxdb' library. This is required to display test parameters."
    print "Installation instructions can be found at:"
    print "https://docs.influxdata.com/influxdb/v1.6/introduction/installation/"
    sys.exit()
import InfluxConfig as conf
import CheckTestsRef

#Client info includes host, port, user, password, dbname
#Measurement is a string
#Tags is a dictionary
#Fields is a dictionary

#Take data object and create tags/fields
def convertData(dataObj, stream=0):
    if isinstance(dataObj, CheckTestsRef.StrobeDelay):
        measurement = "StrobeDelay"
        tags   = {"chip": dataObj.ID, "stream": stream}
        fields = {"delay": dataObj.Delay, "pass": dataObj.StrobeDelayCompare() }
        return measurement,tags,fields
    if isinstance(dataObj, CheckTestsRef.ThreePointGain):
        measurement = "ThreePointGain"
        tags   = {"chip": dataObj.ID, "stream": stream}
        fields = {
            "P0": dataObj.P0,
            "P1": dataObj.P1,
            "Gain": dataObj.Gain,
            "GainRMS": dataObj.GainRMS,
            "Offset": dataObj.Offset,
            "OffsetRMS": dataObj.OffsetRMS,
            "VT50": dataObj.VT50,
            "VT50RMS": dataObj.VT50RMS,
            "InNoise": dataObj.InNoise,
            "InNoiseRMS": dataObj.InNoiseRMS,
            "OutNoise": dataObj.OutNoise,
            "pass": dataObj.compareAll()
        }
        return measurement,tags,fields
    if isinstance(dataObj, CheckTestsRef.ResponseCurve):
        measurement = "ResponseCurve"
        tags   = {"chip": dataObj.ID, "stream": stream}
        fields = {
            "P0": dataObj.P0,
            "P1": dataObj.P1,
            "P2": dataObj.P2,
            "Gain": dataObj.Gain,
            "GainRMS": dataObj.GainRMS,
            "Offset": dataObj.Offset,
            "OffsetRMS": dataObj.OffsetRMS,
            "VT50": dataObj.VT50,
            "VT50RMS": dataObj.VT50RMS,
            "InNoise": dataObj.InNoise,
            "InNoiseRMS": dataObj.InNoiseRMS,
            "OutNoise": dataObj.OutNoise,
            "pass": dataObj.compareAll()
        }
        return measurement,tags,fields
#end def convertData

def writeInfluxDB(dbname, dataObj, stream=0):
    (measurement, tags, fields) = convertData(dataObj, stream)
    client = InfluxDBClient(conf.host, conf.port, conf.user, conf.password, dbname)

    #Create database. Does nothing if database already exists
    client.create_database(dbname)

    json_body = [
        {
            "measurement": measurement,
            "tags": tags,
            "fields": fields
        }
    ]
    client.write_points(json_body)
