#!/usr/bin/python

import serial
import time
import sys
import Deipara
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
import logging

###################################################################################
########## Starting the real program here #########################################
###################################################################################
        
#The loading API 
logging.basicConfig(filename='PythonWrapperWebArduinoUsbD.log',level=logging.INFO)
logging.info('Daemon starting...')

#Load the config
json_data = open('ConfigFiles')
Config = json.load(json_data)
logging.info("config is : " + str(Config))

#Object that handle all devices present on the networl
aRegisterDevices =Deipara.DevicesHandler()
aRegisterDevices.loadDevices()

#The brain
aBrain = Deipara.Brain()

#Liaison serie USB : moyen de com entre le raspberry pi et l arduino
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)

#Liaison network : moyen de com entre le client python et le serveur python
host = ''
port = 50007
backlog = 5
size = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen(backlog)

#input object used for "select" function to monitor both USB and network in same time
input = [server,fd]

#the infinit loop
while 1:
    inputready,outputready,exceptready = select.select(input,[],[])

    for s in inputready:

        if s == server:
            logging.info("handle the server socket")
            client, address = server.accept()
            input.append(client)
            
        elif s == fd:
            logging.info("handle USB port input")
            aResponse = fd.readline()
            aBrain.HandleUsbInput(aResponse,aRegisterDevices)

        else:
            logging.info("handle all other sockets")
            data = s.recv(size)
            logging.info("input is : " + data)
            if data:
                aBrain.SendMessage(fd,data,aRegisterDevices)
                s.send("ACK")
            else:
                logging.info("Closing socket")
                s.close()
                input.remove(s)
                
    aBrain.smartProcessing(aRegisterDevices,fd)
                
server.close() 