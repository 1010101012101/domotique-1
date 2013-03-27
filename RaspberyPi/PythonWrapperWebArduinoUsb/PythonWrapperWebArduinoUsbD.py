#!/usr/bin/python

import serial
import time
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
import logging

class Object:
    "Une classe qui decrit un capteur"
    
    def __init__(self):
        self.id =0
        self.physicalLocation =""
        self.currentStatus =""
        self.description =""
        self.Reset =""
        self.InPossibleCmd ={}
        self.OutPossibleCmd ={}
        self.ActionsCommands ={}
        self.PossibleStates ={}
        
    def executeCmd(self,aCmdFromData):
        #logging.info ("executing : " + str(aCmdFromData) )
        exec(self.ActionsCommands[aCmdFromData])
        
    def reset(self):
        logging.debug("reseting")
        exec(self.Reset)

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + "self.id : " + str(self.id) + "\n"
        aRetString = aRetString + "self.physicalLocation : " + str(self.physicalLocation) + "\n"
        aRetString = aRetString + "self.currentStatus : " + str(self.currentStatus) + "\n"
        aRetString = aRetString + "self.description : " + str(self.description) + "\n"
        aRetString = aRetString + "self.Reset : " + str(self.Reset) + "\n"
        aRetString = aRetString + "self.InPossibleCmd : " + str(self.InPossibleCmd) + "\n"
        aRetString = aRetString + "self.OutPossibleCmd : " + str(self.OutPossibleCmd) + "\n"
        aRetString = aRetString + "self.ActionsCommands : " + str(self.ActionsCommands) + "\n"
        aRetString = aRetString + "self.PossibleStates : " + str(self.PossibleStates) + "\n"
        return aRetString


def sendEmailFireDetected():
    logging.info("Envoi email detection incendie")
    # Define email addresses to use
    addr_to   = Config["addr_to"]
    addr_from = Config["addr_from"]
    # Define SMTP email server details
    smtp_server = Config["smtp_server"]
    smtp_user   = Config["smtp_user"]
    smtp_pass   = Config["smtp_pass"]
    
    # Construct email
    expires = datetime.datetime.now()
    msg = MIMEText('Fire detected at ' + str(expires))
    msg['To'] = addr_to
    msg['From'] = addr_from
    msg['Subject'] = 'Fire alarm'

    # Send the message via an SMTP server
    s = smtplib.SMTP(smtp_server, 587)
    s.login(smtp_user,smtp_pass)
    s.sendmail(addr_from, addr_to, msg.as_string())
    s.quit()

def PeopleDetectedCharlesRoom(iSerialLink,iListOfDevice):
    logging.info("Detection chambre charles")
    aDataToWrite = "MSG:11_ORIGIN:PythonScript"
    SendMessage(iSerialLink, aDataToWrite,iListOfDevice)
    
def PeopleDetectedEntree(iSerialLink):
    logging.info("Detection entree")
    #aDataToWrite = "MSG:11_ORIGIN:PythonScript"
    #SendMessage(iSerialLink, aDataToWrite)
    
def smartProcessing(iListOfDevice,iSerialLink):
    logging.info("Trying to be smart")
    for aOneDevice in iListOfDevice:
        logging.debug("checking : " + str(aOneDevice))
        if ((aOneDevice.id == 2) and (aOneDevice.currentStatus=="incendie en cours")):
            sendEmailFireDetected()
        elif ((aOneDevice.id == 6) and (aOneDevice.currentStatus=="personne detecte")):
            PeopleDetectedEntree()
        elif ((aOneDevice.id == 7) and (aOneDevice.currentStatus=="personne detecte")):
            PeopleDetectedCharlesRoom(iSerialLink,iListOfDevice)
        else :
            logging.debug("Nothing to do even if we are smart")
        aOneDevice.reset()
    
    
def SendMessage(iSerialLink,iDataToWrite, iListOfDevice):
    logging.info ("Writting input to USB port and sending back to sender")
    aCurrentDateTime = datetime.datetime.now()
    aCmdFromData=int((iDataToWrite.split('_')[0]).split(':')[1])
    aOriginFromData=(iDataToWrite.split('_')[1]).split(':')[1]
    aLogLine = "(V2)TO:USB DATE: " + str(aCurrentDateTime) + " ORIGIN: " + aOriginFromData  + " CMD: " + str(aCmdFromData)
    
    #c.execute("update object set status=off where id=?",(aCmdFromData))
    
    logging.info (aLogLine)
    aLogFile = open("/var/www/Logs/logs.txt", "a")
    aLogFile.write(aLogLine+"\n")
    aLogFile.close()
    
    logging.info("Looping on the devices and allow them to update themselve.")
    for aOneObj in iListOfDevice:
        #logging.info ("possible cmd : " + str(aOneObj.InPossibleCmd.keys()))
        if aCmdFromData in aOneObj.InPossibleCmd.keys():
            logging.info("Updating device ID : " + str(aOneObj.id))
            aOneObj.executeCmd(aCmdFromData)
    
    iSerialLink.write(chr(aCmdFromData))
    
def HandleUsbInput(iUsbString,iListOfDevice):
    logging.info ("Handle USB incoming message : " + iUsbString)
    if("ID" in iUsbString):
        sqliteCnx = sqlite3.connect('/var/www/DataBase/Domos.db')
        c = sqliteCnx.cursor()
        expires = datetime.datetime.now()
        aValueReceived = float((iUsbString.split('_')[1]).split(':')[1])
        aRequestorId = int((iUsbString.split('_')[0]).split(':')[1])
        c.execute("INSERT INTO measures (id, timestamp, value) VALUES (?,?,?)",(str(aRequestorId),expires,aValueReceived))
        sqliteCnx.commit()
        sqliteCnx.close()
        
        aCurrentDateTime = datetime.datetime.now()
        aLogLine = "(V2)FROM:USB DATE: " + str(aCurrentDateTime) + " ORIGIN: " + str(aRequestorId)  + " VALUE: " + str(aValueReceived)
        logging.info (aLogLine)
        aLogFile = open("/var/www/Logs/logs.txt", "a")
        aLogFile.write(aLogLine+"\n")
        aLogFile.close()
        
        logging.info("Looping on the devices and allow them to update themselve.")    
        for aOneObj in iListOfDevice:
            #logging.info ("possible cmd : " + str(aOneObj.OutPossibleCmd.keys()))
            if aRequestorId in aOneObj.OutPossibleCmd.keys():
                logging.info("Updating device ID : " + str(aOneObj.id))
                aOneObj.executeCmd(aRequestorId)
    else:
        logging.error("Strange response....ignore it")

logging.basicConfig(filename='PythonWrapperWebArduinoUsbD.log',level=logging.INFO)
logging.info('Daemon starting...')

fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)

json_data = open('ConfigFiles')
Config = json.load(json_data)
logging.info("config is : " + str(Config))

#Create static object (the modules bought since I can not change them to register themselve)
aLampeCharles = Object()
aLampeCharles.physicalLocation = "Charles"
aLampeCharles.id = 1
aLampeCharles.description = "Lampe charles"
aLampeCharles.Reset = "self.currentStatus=\"on\""
aLampeCharles.InPossibleCmd = {5:"on",6:"off"}
aLampeCharles.OutPossibleCmd = {}
aLampeCharles.PossibleStates = ["on","off"]
aLampeCharles.ActionsCommands ={5:"self.currentStatus=\"on\"", 6:"self.currentStatus=\"off\""}

aVoletCharles = Object()
aVoletCharles.physicalLocation = "Charles"
aVoletCharles.id = 4
aVoletCharles.description = "Volet charles"
aVoletCharles.InPossibleCmd = {7:"ouvert",8:"ferme"}
aVoletCharles.OutPossibleCmd = {}
aVoletCharles.PossibleStates = ["ouvert","ferme"]
aVoletCharles.ActionsCommands ={7:"self.currentStatus=\"ouvert\"", 8:"self.currentStatus=\"ferme\""}

aLampeSecondaireCharles = Object()
aLampeSecondaireCharles.physicalLocation = "Charles"
aLampeSecondaireCharles.id = 3
aLampeSecondaireCharles.description = "Lampe secondaire charles"
aLampeSecondaireCharles.InPossibleCmd = {11:"on",12:"off"}
aLampeSecondaireCharles.OutPossibleCmd = {}
aLampeSecondaireCharles.PossibleStates = ["on","off"]
aLampeSecondaireCharles.ActionsCommands ={11:"self.currentStatus=\"on\"", 12:"self.currentStatus=\"off\""}

aDetecteurFumee = Object()
aDetecteurFumee.physicalLocation = "Cuisine"
aDetecteurFumee.id = 2
aDetecteurFumee.description = "Detecteur fumee cuisine"
aDetecteurFumee.Reset = "self.currentStatus=\"pas incendie\""
aDetecteurFumee.InPossibleCmd = {39:"ping avec reponse",40:"Buz"}
aDetecteurFumee.OutPossibleCmd = {1:"incendie ongoing"}
aDetecteurFumee.PossibleStates = ["incendie en cours","pas incendie"]
aDetecteurFumee.ActionsCommands ={39:"", 40:"",1:"self.currentStatus=\"incendie en cours\""}

aDetecteurEntree = Object()
aDetecteurEntree.physicalLocation = "Entree"
aDetecteurEntree.id = 6
aDetecteurEntree.Reset = "self.currentStatus=\"pas personne detecte\""
aDetecteurEntree.description = "Detecteur entree"
aDetecteurEntree.InPossibleCmd = {34:"allume lumiere",35:"teindre lumiere",36:"allume lumiere 2 min",33:"debug simule passage detecteur"}
aDetecteurEntree.OutPossibleCmd = {50:"personne detecte"}
aDetecteurEntree.PossibleStates = ["personne detecte","pas personne detecte"]
aDetecteurEntree.ActionsCommands ={34:"", 35:"", 36:"", 33:"",50:"self.currentStatus=\"personne detecte\""}

aDetecteurCharles = Object()
aDetecteurCharles.physicalLocation = "Charles"
aDetecteurCharles.id = 7
aDetecteurCharles.Reset = "self.currentStatus=\"pas personne detecte\""
aDetecteurCharles.description = "Detecteur entree"
aDetecteurCharles.InPossibleCmd = {34:"allume lumiere",35:"teindre lumiere",36:"allume lumiere 2 min",33:"debug simule passage detecteur"}
aDetecteurCharles.OutPossibleCmd = {2:"personne detecte"}
aDetecteurCharles.PossibleStates = ["personne detecte","pas personne detecte"]
aDetecteurCharles.ActionsCommands ={34:"", 35:"", 36:"", 33:"",2:"self.currentStatus=\"personne detecte\""}


aRegisterDevices =[]
aRegisterDevices.append(aLampeCharles)
aRegisterDevices.append(aDetecteurFumee)
aRegisterDevices.append(aLampeSecondaireCharles)
aRegisterDevices.append(aVoletCharles)
aRegisterDevices.append(aDetecteurEntree)
aRegisterDevices.append(aDetecteurCharles)

host = ''
port = 50007
backlog = 5
size = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen(backlog)
input = [server,fd]
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
            HandleUsbInput(aResponse,aRegisterDevices)

        else:
            logging.info("handle all other sockets")
            data = s.recv(size)
            logging.info("input is : " + data)
            if data:
                SendMessage(fd,data,aRegisterDevices)
                s.send("ACK")
            else:
                logging.info("Closing socket")
                s.close()
                input.remove(s)
                
    smartProcessing(aRegisterDevices,fd)
                
server.close() 