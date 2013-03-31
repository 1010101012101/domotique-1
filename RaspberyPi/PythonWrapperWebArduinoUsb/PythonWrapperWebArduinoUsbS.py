#!/usr/bin/python

import serial, time
import sys
import socket
import datetime
from time import sleep
import sqlite3
import subprocess
# Echo client program
import socket
from optparse import OptionParser

class Command:
    """A simple command"""
    
    def __init__(self):
        self.idTo = ""
        self.idFrom = ""
        self.message = ""
        
    def dumpAsString(self):
        return "MSG:" + self.message + "_ORIGIN:" + self.idFrom
         

parser = OptionParser(usage="usage: %prog [options]",version="%prog 1.0")
parser.add_option("-p", "--port",action="store",dest="aPortToUse",default="50007",help="the port to listen")
parser.add_option("-s", "--send",action="store",dest="aMsgToSend",default="20",help="Command to send to Arduino Leonardo")
parser.add_option("-o", "--originator",action="store",dest="aOriginator",default="UNKNOW",help="Originator of the request")
(options, args) = parser.parse_args()

HOST = ''
PORT = int(options.aPortToUse)

#aMsgToSend2 = "MSG:" + options.aMsgToSend + "_ORIGIN:" + options.aOriginator

aCmdToSend = Command()
aCmdToSend.message = options.aMsgToSend
aCmdToSend.idFrom = options.aOriginator
aMsgToSend2 = aCmdToSend.dumpAsString()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((HOST, PORT))
except:
    print("no server available")
    s.close()
    print("starting server")
    subprocess.call("python PythonWrapperWebArduinoUsbD.py", shell=True)
    #on va rester la a l infini

    
s.send(aMsgToSend2)

s.close()

