#!/usr/bin/python

import serial, time
import sys
import socket
import datetime
import sqlite3
from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options] filename",version="%prog 1.0")
parser.add_option("-s", "--send",action="store",dest="aMsgToSend",default="20",help="Command to send to Arduino Leonardo")
(options, args) = parser.parse_args()

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
#s.setblocking(0)



while 1:
    print ("loop")
    conn, addr = s.accept()
    print 'Connected by', addr
    data = conn.recv(1024)
    if data:
        print ("data : " + str(data))
        aCurrentDateTime = datetime.datetime.now()
        #aLogLine = "DATE: " + str(aCurrentDateTime) + " ORIGIN: " + options.aOriginator + " CMD: " + options.aMsgToSend + " ID: " + options.aRequestorId
        #print ("Log line : " + aLogLine)
        #aLogFile = open("/var/www/Logs/logs.txt", "a")
        #aLogFile.write(aLogLine+"\n")
        #aLogFile.close()

        #print ("Open virtual serial port")
        #fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
        #fd.flush()
        #print ("Sending : " + options.aMsgToSend)

        #fd.write(options.aMsgToSend)

        #sqliteCnx = sqlite3.connect('/var/www/DataBase/Domos.db')

    #aResponse = fd.readline() #How do I get the most recent line sent from the device?
    if(aResponse != ""):
        #c = sqliteCnx.cursor()
        print ("Response : " + aResponse)
        #expires = aCurrentDateTime
        #if("ID" in aResponse):
            #aValueReceived = (aResponse.split('_')[1]).split(':')[1]
            #c.execute("INSERT INTO measures (id, timestamp, value) VALUES (?,?,?)",(options.aRequestorId,expires,float(aValueReceived)))
            #sqliteCnx.commit()
            #print c.fetchone()
            #sqliteCnx.close()
            #sys.exit(0)

conn.close()


