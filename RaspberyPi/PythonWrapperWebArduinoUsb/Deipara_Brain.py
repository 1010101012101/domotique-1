#!/usr/bin/python

import logging
import datetime
import serial
import os
import jsonpickle

###################################################################################
########## Brain class....smart one       #########################################
###################################################################################

class Brain:
    "Une classe qui pense"
    
    def __init__(self):  
        logging.info("create brain")
        
    def PeopleDetectedCharlesRoom(self,iListOfDevice):
        logging.warning("PeopleDetectedCharlesRoom")
        aDataToWrite = "MSG:11_ORIGIN:PythonScript"
        self.SendMessage( aDataToWrite,iListOfDevice)
        
    def TurnCharlesLightOff(self,iListOfDevice):
        logging.warning("TurnCharlesLightOff")
        aDataToWrite = "MSG:12_ORIGIN:PythonScript"
        self.SendMessage( aDataToWrite,iListOfDevice)
        
    def refreshCapteur(self,iCapteur,iListOfDevice):
        logging.info("Refreshing capteur : " + str(iCapteur.id))
        aDataToWrite = "MSG:" + str(iCapteur.InPossibleCmd.keys()[0]) + "_ORIGIN:PythonScript"
        logging.info("Msg used to refresh : " + aDataToWrite)
        iCapteur.refreshOngoing = True
        self.SendMessage(aDataToWrite,iListOfDevice)
        
    def getExternalLuminosite():
        for aOneDevice in iListOfDevice.registeredDevices:
            if (aOneDevice.id == 22):
                return aOneDevice.currentStatus
                
    def TurnEntreeLightOff(self,iListOfDevice):
        logging.warning("TurnEntreeLightOff")
        aDataToWrite = "MSG:35_ORIGIN:PythonScript"
        self.SendMessage( aDataToWrite,iListOfDevice)
    
    def PeopleDetectedEntree(self,iListOfDevice):
        logging.warning("PeopleDetectedEntree")
        aDataToWrite = "MSG:34_ORIGIN:PythonScript"
        self.SendMessage( aDataToWrite,iListOfDevice)
        
    def sendEmailFireDetected():
        logging.warning("Envoi email detection incendie")
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
        logging.debug("Stoping") 

    def smartProcessing2(self,iListOfDevice):
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
            aOneDevice.reset()
            
        #Setp 2 : On reset les actions resultantes des detections passe
        #Par exemple si la lumiere de l entree ete ON car qq un avait ete detecte depuis 10 minutes mais qu il y a plus eu de detection depuis 10 min....on eteind
        logging.info("Reseting all previous automatic actions")
        for aOneDevice in iListOfDevice.registeredDevices:
            logging.debug("checking states : " + str(aOneDevice.id))
            if ((aOneDevice.id == 9) and ((iListOfDevice.getDevice(3)).currentStatus=="unstable") and (datetime.datetime.now() - aOneDevice.LastTMeaureDate > datetime.timedelta (seconds = 600))):
                self.TurnCharlesLightOff(iListOfDevice)
            elif ((aOneDevice.id == 10) and ((iListOfDevice.getDevice(8)).currentStatus=="unstable") and (datetime.datetime.now() - aOneDevice.LastTMeaureDate > datetime.timedelta (seconds = 180))):
                self.TurnEntreeLightOff(iListOfDevice)
                
        #Setp 3 : On force un refresh des capteurs periodiques
        logging.info("Force the auto refresh of capteur")
        for aOneDevice in iListOfDevice.registeredDevices:
            logging.debug("checking autoupdate : " + str(aOneDevice.id))
            if ( (aOneDevice.stateCanBeRefresh == True) and (aOneDevice.refreshOngoing == False)and (datetime.datetime.now() - aOneDevice.LastTMeaureDate > datetime.timedelta (minutes = aOneDevice.refreshRatemin) ) ):
                logging.debug("We can refresh : " + str(aOneDevice.id))
                self.refreshCapteur(aOneDevice,iListOfDevice)

                
    def HandleUsbInput(self,iUsbString,iListOfDevice):
        logging.info ("Handle USB incoming message : " + iUsbString)
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
                logging.info ("possible cmd : " + str(aOneObj.OutPossibleCmd.keys()))
                if str(aRequestorId) in aOneObj.OutPossibleCmd.keys():
                    logging.info("Updating device ID : " + str(aOneObj.id))
                    aOneObj.executeCmd(str(aRequestorId),aValueReceived)
                    logging.info("Device ID : " +str(aOneObj))
        else:
            logging.error("Strange response....ignore it")
        
    def SendMessage(self,iDataToWrite, iListOfDevice):
        logging.debug("Sending message")
        aCurrentDateTime = datetime.datetime.now()
        aCmdFromData=int((iDataToWrite.split('_')[0]).split(':')[1])
        aOriginFromData=(iDataToWrite.split('_')[1]).split(':')[1]
        aLogLine = "(V2)TO:USB DATE: " + str(aCurrentDateTime) + " ORIGIN: " + aOriginFromData  + " CMD: " + str(aCmdFromData)
        
        #c.execute("update object set status=off where id=?",(aCmdFromData))
        
        logging.info (aLogLine)
        aLogFile = open("/var/www/Logs/logs.txt", "a")
        aLogFile.write(aLogLine+"\n")
        aLogFile.close()
        
        logging.info("Looping on the devices and allow them to update themselve2.")
        for aOneObj in iListOfDevice.registeredDevices:
            #logging.info ("possible cmd : " + str(aOneObj.InPossibleCmd.keys()))
            if str(aCmdFromData) in aOneObj.InPossibleCmd.keys():
                logging.info("Updating device I5D : " + str(aOneObj.id))
                aOneObj.executeCmd(str(aCmdFromData),str(aOriginFromData))
                if (aOneObj.porteuse == "PYTHON"):
                    dumy = 7
                else:
                    fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
                    logging.info ("Writting input to USB port and sending back to sender")
                    fd.write(chr(aCmdFromData))
                
    def ReadDeviceStatus2(self,iDataToWrite, iListOfDevice):
        aCmdFromData=int((iDataToWrite.split('_')[0]).split(':')[1])
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
        return aRetString
