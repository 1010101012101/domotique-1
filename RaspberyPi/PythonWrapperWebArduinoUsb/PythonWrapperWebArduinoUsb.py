#!/usr/bin/python

import serial, time
import sys
import datetime
import sqlite3
from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options] filename",version="%prog 1.0")
parser.add_option("-s", "--send",action="store",dest="aMsgToSend",default="20",help="Command to send to Arduino Leonardo")
parser.add_option("-t", "--timeout",action="store",dest="aTimeout",default="10",help="RTO for the response")
parser.add_option("-i", "--id",action="store",dest="aRequestorId",default="5",help="Id of the requestor")
parser.add_option("-o", "--originator",action="store",dest="aOriginator",default="UNKNOW",help="Originator of the request")
(options, args) = parser.parse_args()


aCurrentDateTime = datetime.datetime.now()
aLogLine = "DATE: " + str(aCurrentDateTime) + " ORIGIN: " + options.aOriginator + " CMD: " + options.aMsgToSend + " ID: " + options.aRequestorId
print ("Log line : " + aLogLine)

print ("Open virtual serial port")
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
fd.flush()
print ("Sending : " + options.aMsgToSend)

fd.write(options.aMsgToSend)

conn = sqlite3.connect('/var/www/DataBase/Domos.db')

c = conn.cursor()

aLoopIndex=1
aResponse=""
while aLoopIndex <= int(options.aTimeout):
    print ("checking in loop : " + str(aLoopIndex))
    aResponse = fd.readline() #How do I get the most recent line sent from the device?
    if(aResponse != ""):
        print ("Response : " + aResponse)
        expires = aCurrentDateTime
        #("INSERT INTO token VALUES (?, ?)", (token, expires))
        c.execute("INSERT INTO measures (id, timestamp, value) VALUES (?,?,?)",(options.aRequestorId,expires,float(aResponse)))
        conn.commit()
        print c.fetchone()
        conn.close()
        sys.exit(0)
    aLoopIndex=aLoopIndex+1
    time.sleep(1)
sys.exit(1)