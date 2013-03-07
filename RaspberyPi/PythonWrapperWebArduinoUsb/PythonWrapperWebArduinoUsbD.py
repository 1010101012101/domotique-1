#!/usr/bin/python

import serial, time
import sys
import socket
import datetime
import select
import sys
import sqlite3
from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options]",version="%prog 1.0")
parser.add_option("-p", "--port",action="store",dest="aPortToUse",default="50007",help="the port to listen")
(options, args) = parser.parse_args()

fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)

host = ''
port = int(options.aPortToUse)
backlog = 5
size = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen(backlog)
input = [server,sys.stdin,fd]
while 1:
    inputready,outputready,exceptready = select.select(input,[],[])

    for s in inputready:

        if s == server:
            print ("handle the server socket")
            client, address = server.accept()
            input.append(client)

        elif s == sys.stdin:
            print ("handle standard input")
            aInput = sys.stdin.readline()
            print ("input is : " + aInput)
            fd.write(aInput)
            
        elif s == fd:
            print ("handle USB port input")
            aResponse = fd.readline()
            print ("USB response : " + aResponse)
            sqliteCnx = sqlite3.connect('/var/www/DataBase/Domos.db')
            c = sqliteCnx.cursor()
            expires = datetime.datetime.now()
            aValueReceived=aResponse
            aRequestorId="UNKNOW"
            if("ID" in aResponse):
                aValueReceived = (aResponse.split('_')[1]).split(':')[1]
                aRequestorId = (aResponse.split('_')[0]).split(':')[1]
            c.execute("INSERT INTO measures (id, timestamp, value) VALUES (?,?,?)",(aRequestorId,expires,float(aValueReceived)))
            sqliteCnx.commit()
            sqliteCnx.close()

        else:
            print ("handle all other sockets")
            data = s.recv(size)
            print ("input is : " + data)
            if data:
                print ("Writting input to USB port and sending back to sender")
                aCurrentDateTime = datetime.datetime.now()
                aCmdFromData=(data.split('_')[0]).split(':')[1]
                aIdFromData=(data.split('_')[1]).split(':')[1]
                aOriginFromData=(data.split('_')[2]).split(':')[1]
                aLogLine = "DATE: " + str(aCurrentDateTime) + " ORIGIN: "  + " CMD: " + data + " ID: " 
                print ("Log line : " + aLogLine)
                aLogFile = open("/var/www/Logs/logs.txt", "a")
                aLogFile.write(aLogLine+"\n")
                aLogFile.close()
                fd.write(data)
                s.send(data)
            else:
                print ("Closing socket")
                s.close()
                input.remove(s)
server.close() 