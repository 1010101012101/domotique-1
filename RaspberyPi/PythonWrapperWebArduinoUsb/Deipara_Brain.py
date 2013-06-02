#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import datetime
import serial
import os
import json
import jsonpickle

###################################################################################
########## Brain class....smart one       #########################################
###################################################################################

class Brain:
    '''Une classe qui pense. Elle gere les evenements USB/TCP recus et l etat des objets. Elle gere aussi les liens entre les objets
    Par ex : un evenement sur un detecteur de presence va allumer une lumiere dans la meme piece''' 
    
    def __init__(self, iConfig):  
        logging.error("create brain")
        self.config=iConfig
        
    def PeopleDetectedCharlesRoom(self,iListOfDevice):
        '''Action trige lors de la detection de presence dans la chambre charles'''
        logging.error("PeopleDetectedCharlesRoom")
        aDataToWrite = "MSG:11_ORIGIN:PythonScript"
        self.SendMessage( "11","PythonScript",iListOfDevice)
        
    def PeopleDetectedSalon(self,iListOfDevice):
        '''Action trige lors de la detection de presence dans le salon'''
        logging.error("PeopleDetectedSalon")
        aDataToWrite = "MSG:3_ORIGIN:PythonScript"
        self.SendMessage( "3","PythonScript",iListOfDevice)
     
    def PeopleDetectedCuisine(self,iListOfDevice):
        '''Action trige lors de la detection de presence dans le salon'''
        logging.error("PeopleDetectedCuisine")
        aDataToWrite = "MSG:46_ORIGIN:PythonScript"
        self.SendMessage( "46","PythonScript",iListOfDevice) 

    def TurnCuisineLightOff(self,iListOfDevice):
        '''Action trige lorsqu plus personne est detecte ds la chambre charles depuis un certains temps'''
        logging.error("TurnCuisineLightOff")
        aDataToWrite = "MSG:47_ORIGIN:PythonScript"
        self.SendMessage( "47","PythonScript",iListOfDevice)  
        
    def FermeVoletSalon(self,iListOfDevice):
        '''Action trige lorsqu plus personne est detecte ds la chambre charles depuis un certains temps'''
        logging.error("FermeVoletSalon")
        aDataToWrite = "MSG:10_ORIGIN:PythonScript"
        self.SendMessage( "10","PythonScript",iListOfDevice) 
        
    def FermeVoletCharles(self,iListOfDevice):
        '''Action trige lorsqu plus personne est detecte ds la chambre charles depuis un certains temps'''
        logging.error("FermeVoletCharles")
        aDataToWrite = "MSG:8_ORIGIN:PythonScript"
        self.SendMessage( "8","PythonScript",iListOfDevice) 
        
    def TurnSalonLightOff(self,iListOfDevice):
        '''Action trige lorsqu plus personne est detecte ds la chambre charles depuis un certains temps'''
        logging.error("TurnSalonLightOff")
        aDataToWrite = "MSG:4_ORIGIN:PythonScript"
        self.SendMessage( "4","PythonScript",iListOfDevice)
        
    def TurnCharlesLightOff(self,iListOfDevice):
        '''Action trige lorsqu plus personne est detecte ds la chambre charles depuis un certains temps'''
        logging.error("TurnCharlesLightOff")
        aDataToWrite = "MSG:12_ORIGIN:PythonScript"
        self.SendMessage( "12","PythonScript",iListOfDevice)
        
    def getExternalLuminosite():
        '''Wrapper pour aller lire la luminosite exterieur depuis le capteur terrasse'''
        for aOneDevice in iListOfDevice.registeredDevices:
            if (aOneDevice.id == 22):
                return aOneDevice.currentStatus
                
    def TurnEntreeLightOff(self,iListOfDevice):
        '''Action trige lorsqu plus personne est detecte ds l entree depuis un certains temps'''
        logging.error("TurnEntreeLightOff")
        aDataToWrite = "MSG:35_ORIGIN:PythonScript"
        self.SendMessage( "35","PythonScript",iListOfDevice)
    
    def PeopleDetectedEntree(self,iListOfDevice):
        '''Action trige lors de la detection de presence dans l entree'''
        logging.error("PeopleDetectedEntree")
        aDataToWrite = "MSG:34_ORIGIN:PythonScript"
        self.SendMessage( "34","PythonScript",iListOfDevice)
        
    def sendEmailFireDetected():
        '''Envoie email lors de la detection incendie'''
        logging.error("Envoi email detection incendie")
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
        
    def stop(self):
        '''Gere le stop de l application (dump l etat des objets dans un fichier)'''
        logging.error("Stoping") 

    def smartProcessing2(self,iListOfDevice):
        '''Une boucle qui a lieu regulierement pour prendre des decision. Elle va verifier les detecteur et en fonction triger certains evenements.
        Par ex si qq un est detecte dans l entree on decide d allumer la lumiere.
        Cette classe va aussi verifier si certaines autres actions (non lie a la detection de personne) peuvent etre prise.
        Par ex : si on a pas eut de detection de personne depuis un moment ds l entree et que la lumiere est allume....on etient
        Enfin elle va aussi mettre a jour tous les capteurs en fonction de leur refresh rate
        Par exemple si ca fait trop longtemps qu on a pas updater la T alors on la met a jour'''
        logging.info("Begining of a smart loop")
        
        #Step 1 : Verifier tous les detecteurs (interupteurs stables) pour voir si ils ont ete actives et prendre les actions correspondantes avant de les reset
        #Par exemple si le detecteur de fumee a ete active alors on va envoyer un mail 
        logging.info("Checking all possible event")
        for aOneDevice in iListOfDevice.registeredDevices:
            logging.debug("checking event : " + str(aOneDevice.id))
            if ((aOneDevice.id == 2) and (aOneDevice.currentStatus=="unstable")):
                sendEmailFireDetected()
            elif ((aOneDevice.id == 10) and (aOneDevice.currentStatus=="unstable")):
                self.PeopleDetectedEntree(iListOfDevice)
            elif ((aOneDevice.id == 9) and (aOneDevice.currentStatus=="unstable")):
                self.PeopleDetectedCharlesRoom(iListOfDevice)
            elif ((aOneDevice.id == 13) and (aOneDevice.currentStatus=="unstable")):
                self.PeopleDetectedSalon(iListOfDevice)
            elif ((aOneDevice.id == 27) and (aOneDevice.currentStatus=="unstable")):
                self.PeopleDetectedCuisine(iListOfDevice)
            aOneDevice.reset()
            
        #Setp 2 : On reset les actions resultantes des detections passe
        #Par exemple si la lumiere de l entree ete ON car qq un avait ete detecte depuis 10 minutes mais qu il y a plus eu de detection depuis 10 min....on eteind
        logging.info("Reseting all previous automatic actions")
        for aOneDevice in iListOfDevice.registeredDevices:
            logging.debug("checking states : " + str(aOneDevice.id))
            if ((aOneDevice.id == 9) and ((iListOfDevice.getDevice(3)).currentStatus=="on") and (datetime.datetime.now() - aOneDevice.LastTMeaureDate > datetime.timedelta (seconds = 600))):
                self.TurnCharlesLightOff(iListOfDevice)
            elif ((aOneDevice.id == 10) and ((iListOfDevice.getDevice(8)).currentStatus=="on") and (datetime.datetime.now() - aOneDevice.LastTMeaureDate > datetime.timedelta (seconds = 180))):
                self.TurnEntreeLightOff(iListOfDevice)
            elif ((aOneDevice.id == 13) and ((iListOfDevice.getDevice(12)).currentStatus=="on") and (datetime.datetime.now() - aOneDevice.LastTMeaureDate > datetime.timedelta (seconds = 600))):
                self.TurnSalonLightOff(iListOfDevice)
            elif ((aOneDevice.id == 27) and ((iListOfDevice.getDevice(11)).currentStatus=="on") and (datetime.datetime.now() - aOneDevice.LastTMeaureDate > datetime.timedelta (seconds = 240))):
                self.TurnCuisineLightOff(iListOfDevice)
                
        #Setp 3 : On force un refresh des capteurs periodiques
        logging.info("Force the auto refresh of capteur")
        for aOneDevice in iListOfDevice.registeredDevices:
            logging.debug("checking autoupdate : " + str(aOneDevice.id))
            if ( (aOneDevice.stateCanBeRefresh == True) and (datetime.datetime.now() - aOneDevice.LastRefreshDate > datetime.timedelta (seconds = aOneDevice.refreshRatemin) ) ):
                logging.debug("We can refresh : " + str(aOneDevice.id))
                aOneDevice.RequestNewValue()
                
        #Setp 4 : action auto non lie a une detection (genre ferme les volets parce qu il fait nuit)
        logging.info("Force auto non lie a une detection")
        for aOneDevice in iListOfDevice.registeredDevices:
            try:
                logging.debug("checking : " + str(aOneDevice.id))
                if ((aOneDevice.id == 22) and ((int(aOneDevice.currentStatus)) < 10) and (datetime.datetime.now() - aOneDevice.LastTMeaureDate < datetime.timedelta (seconds = 900))):
                    #self.FermeVoletSalon(iListOfDevice)
                    if((iListOfDevice.getDevice(4)).currentStatus!="off"):
                        #self.FermeVoletCharles(iListOfDevice)
                        logging.error("je dois fermer les volets")
            except Exception: 
                logging.error("Error when checking automatic action for device : " + str(aOneDevice.id))
                
    def HandleUsbInput(self,iUsbString,iListOfDevice):
        '''Cette fonction est lance lorsqu on recoit qq chose sur le port USB (qui provient donc de l Arduino Leonardo).
        Elle va trouver la fonction associe a la requette entrante et permettre au device de se mettre a jour'''
        logging.warning ("Handle USB incoming message : " + iUsbString)
        if("ID" in iUsbString):
            expires = datetime.datetime.now()
            aValueReceived = float((iUsbString.split('_')[1]).split(':')[1])
            aRequestorId = int((iUsbString.split('_')[0]).split(':')[1])
            
            aCurrentDateTime = datetime.datetime.now()
            aLogLine = "(V2)FROM:USB DATE: " + str(aCurrentDateTime) + " ORIGIN: " + str(aRequestorId)  + " VALUE: " + str(aValueReceived)
            logging.info (aLogLine)
            aLogFile = open("/var/www/Logs/logs.txt", "a")
            aLogFile.write(aLogLine+"\n")
            aLogFile.close()
            
            logging.info("Looping on the devices and allow them to update themselve7.")    
            for aOneObj in iListOfDevice.registeredDevices:
                logging.debug ("possible cmd : " + str(aOneObj.OutPossibleCmd.keys()))
                if str(aRequestorId) in aOneObj.OutPossibleCmd.keys():
                    logging.info("Updating device ID : " + str(aOneObj.id))
                    aOneObj.executeOutCmd(str(aRequestorId),aValueReceived)
                    logging.debug("Device ID : " +str(aOneObj))
        else:
            logging.error("Strange response....ignore it")
            
    def TranslateVocalAction(self,Sentences, Devices):
        logging.warning("Translate : " + str(Sentences))
        #Weight, Device ID, CommandID
        aBestDeviceMatch=(0,0,0)
        for aOneObj in Devices.registeredDevices:
            (aWeight,aCmdId)=aOneObj.getDeviceWeightSpeech(Sentences)
            logging.warning ("DeviceId : " + str(aOneObj.id) + " has weight : " + str(aWeight))
            if(aWeight > aBestDeviceMatch[0]):
                aBestDeviceMatch=(aWeight,aOneObj.id,aCmdId)
        logging.warning("Device is : " + str(aBestDeviceMatch))
        self.SendMessage( str(aBestDeviceMatch[2]),"VoiceAction",Devices)
        return (Devices.getDevice(aBestDeviceMatch[1]).description,aBestDeviceMatch[2])
        
        
    def SendMessage(self,iDataToWrite,iOriginator, iListOfDevice):
        '''Cette fonction est lance lorsqu on recoit qq chose sur TCP (qui provient donc du client et probablement du site web) si il sagit d un ordre write
        Elle va trouver la fonction associe a la requette entrante et permettre au device de se mettre a jour
        ET elle va envoyer le message sur le port USB pour l Arduino Leonardo'''
        logging.error("Sending message")
        aCurrentDateTime = datetime.datetime.now()
        if(iOriginator=="DUM"):
            aCmdFromData=int((iDataToWrite.split('_')[0]).split(':')[1])
            aOriginFromData=(iDataToWrite.split('_')[1]).split(':')[1]
        else:
            aCmdFromData=int(iDataToWrite)
            aOriginFromData=(iOriginator)
        aLogLine = "(V2)TO:USB DATE: " + str(aCurrentDateTime) + " ORIGIN: " + aOriginFromData  + " CMD: " + str(aCmdFromData)
        
        logging.error (aLogLine)
        aLogFile = open("/var/www/Logs/logs.txt", "a")
        aLogFile.write(aLogLine+"\n")
        aLogFile.close()
        
        logging.error("Looping on the devices and allow them to update themselve2.")
        for aOneObj in iListOfDevice.registeredDevices:
            #logging.info ("possible cmd : " + str(aOneObj.InPossibleCmd.keys()))
            if str(aCmdFromData) in aOneObj.InPossibleCmd.keys():
                logging.info("Updating device I5D : " + str(aOneObj.id))
                aOneObj.executeInCmd(str(aCmdFromData),str(aOriginFromData))
                
    def ReadDeviceStatus2(self,iDataToWrite, iListOfDevice):
        '''Cette fonction est lance lorsqu on recoit qq chose sur TCP (qui provient donc du client et probablement du site web) si il sagit d un ordre read
        Elle va trouver la fonction associe a la requette entrante et renvoyer l object fonction en JSON au client pour mettre a jour le site WEB'''
        if("_" in iDataToWrite):        
            aCmdFromData=int((iDataToWrite.split('_')[0]).split(':')[1])
        else:
            aCmdFromData=int(iDataToWrite)
        logging.info("Looking for the device : " + str(aCmdFromData))
        for aOneObj in iListOfDevice.registeredDevices:
            logging.info ("possible cmd : " + str(aOneObj.InPossibleCmd.keys()))
            if (str(aCmdFromData) == str(aOneObj.id)):
                logging.info("find it" + str(aOneObj.id))
                aRest = str(aOneObj)
                pickled = jsonpickle.encode(aOneObj)
                logging.info("ret : " + pickled)
                return pickled
               
    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + "self.config : " + str(self.config) + "\n"
        return aRetString
