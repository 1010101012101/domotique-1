#!/usr/bin/python

import serial, time
import sys
import socket
import datetime
import select
import sys

import json

# Import smtplib to provide email functions
import smtplib
# Import the email modules
from email.mime.text import MIMEText

import sqlite3
from optparse import OptionParser


def sendEmailFireDetected():
    print("Envoi email detection incendie")
    # Define email addresses to use
    addr_to   = Config["addr_to"]
    addr_from = Config["addr_from"]
    # Define SMTP email server details
    smtp_server = Config["smtp_server"]
    smtp_user   = Config["smtp_user"]
    smtp_pass   = Config["smtp_pass"]
    
    # Construct email
    msg = MIMEText('Fire detected at ' + str(expires))
    msg['To'] = addr_to
    msg['From'] = addr_from
    msg['Subject'] = 'Fire alarm'

    # Send the message via an SMTP server
    s = smtplib.SMTP(smtp_server, 587)
    s.login(smtp_user,smtp_pass)
    s.sendmail(addr_from, addr_to, msg.as_string())
    s.quit()

def PeopleDetectedCharlesRoom(iSerialLink):
    print("Detection chambre charles")
    aDataToWrite = "MSG:11_ORIGIN:PythonScript"
    SendMessage(iSerialLink, aDataToWrite)
    
def SendMessage(iSerialLink,iDataToWrite):
    print ("Writting input to USB port and sending back to sender")
    aCurrentDateTime = datetime.datetime.now()
    aCmdFromData=int((iDataToWrite.split('_')[0]).split(':')[1])
    aOriginFromData=(iDataToWrite.split('_')[1]).split(':')[1]
    #print ("chr(0x1F):" + chr(0x1F) + "_chr(31):" + chr(aCmdFromData))
    aLogLine = "(V2)DATE: " + str(aCurrentDateTime) + " ORIGIN: " + aOriginFromData  + " CMD: " + str(aCmdFromData)
    print ("Log line : " + aLogLine)
    aLogFile = open("/var/www/Logs/logs.txt", "a")
    aLogFile.write(aLogLine+"\n")
    aLogFile.close()
    iSerialLink.write(chr(aCmdFromData))
    

parser = OptionParser(usage="usage: %prog [options]",version="%prog 1.0")
parser.add_option("-p", "--port",action="store",dest="aPortToUse",default="50007",help="the port to listen")
(options, args) = parser.parse_args()

fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)

json_data = open('ConfigFiles')
Config = json.load(json_data)
print ("config is : " + str(Config))

host = ''
port = int(options.aPortToUse)
backlog = 5
size = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen(backlog)
input = [server,fd]
print ("Daemon starting")
while 1:
    inputready,outputready,exceptready = select.select(input,[],[])

    for s in inputready:

        if s == server:
            print ("handle the server socket")
            client, address = server.accept()
            input.append(client)
            
        elif s == fd:
            print ("handle USB port input")
            aResponse = fd.readline()
            print ("USB response : " + aResponse)
            if("ID" in aResponse):
                sqliteCnx = sqlite3.connect('/var/www/DataBase/Domos.db')
                c = sqliteCnx.cursor()
                expires = datetime.datetime.now()
                aValueReceived = (aResponse.split('_')[1]).split(':')[1]
                aRequestorId = (aResponse.split('_')[0]).split(':')[1]
                c.execute("INSERT INTO measures (id, timestamp, value) VALUES (?,?,?)",(aRequestorId,expires,float(aValueReceived)))
                sqliteCnx.commit()
                sqliteCnx.close()
                if(aRequestorId == "2"):
                    print("OMG...Hell on earth1")
                    sendEmailFireDetected()

                elif (aRequestorId == "1"):
                    print("OMG...Hell on earth2")
                    PeopleDetectedCharlesRoom(fd)
                else :
                    print ("KO")
            else:
                print("Strange response....ignore it")

        else:
            print ("handle all other sockets")
            data = s.recv(size)
            print ("input is : " + data)
            if data:
                SendMessage(fd,data)
                s.send("ACK")
            else:
                print ("Closing socket")
                s.close()
                input.remove(s)
server.close() 