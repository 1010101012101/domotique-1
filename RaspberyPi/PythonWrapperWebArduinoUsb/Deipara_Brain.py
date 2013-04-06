#!/usr/bin/python

import logging
import datetime
import serial
import jsonpickle

###################################################################################
########## Brain class....smart one       #########################################
###################################################################################

class Brain:
    "Une classe qui pense"
    
    def __init__(self):
        self.lastPeopleDetectedEntree =datetime.datetime.now()
        self.lastTemperatureEntree =(datetime.datetime.now(),0)
        self.lastHumiditeEntree =(datetime.datetime.now(),0)
        
        self.lastPeopleDetectedCharles =datetime.datetime.now()
        self.lastTemperatureCharles =(datetime.datetime.now(),0)
        self.lastHumiditeCharles =(datetime.datetime.now(),0)
        
    def PeopleDetectedCharlesRoom(self,iListOfDevice):
        logging.info("Detection chambre charles")
        aDataToWrite = "MSG:11_ORIGIN:PythonScript"
        self.lastPeopleDetectedCharles = datetime.datetime.now()
        self.SendMessage( aDataToWrite,iListOfDevice)
        
    def TurnCharlesLightOff(self,iListOfDevice):
        logging.info("Detection chambre charles")
        aDataToWrite = "MSG:12_ORIGIN:PythonScript"
        self.lastPeopleDetectedCharles = datetime.datetime.now()
        self.SendMessage( aDataToWrite,iListOfDevice)
        
    def TurnEntreeLightOff(self,iListOfDevice):
        logging.info("Detection chambre charles")
        aDataToWrite = "MSG:35_ORIGIN:PythonScript"
        self.lastPeopleDetectedEntree = datetime.datetime.now()
        self.SendMessage( aDataToWrite,iListOfDevice)
    
    def PeopleDetectedEntree(self,iListOfDevice):
        logging.info("Detection entree")
        aDataToWrite = "MSG:34_ORIGIN:PythonScript"
        self.lastPeopleDetectedEntree = datetime.datetime.now()
        self.SendMessage( aDataToWrite,iListOfDevice)
        
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
        
    def stop(self):
        logging.debug("Stoping") 
        

    def smartProcessing2(self,iListOfDevice):
        logging.debug("Trying to be smart")
        for aOneDevice in iListOfDevice.registeredDevices:
            logging.debug("checking event : " + str(aOneDevice))
            if ((aOneDevice.id == 2) and (aOneDevice.currentStatus=="incendie en cours")):
                sendEmailFireDetected()
            elif ((aOneDevice.id == 10) and (aOneDevice.currentStatus=="unstable")):
                self.PeopleDetectedEntree(iListOfDevice)
            elif ((aOneDevice.id == 9) and (aOneDevice.currentStatus=="unstable")):
                self.PeopleDetectedCharlesRoom(iListOfDevice)
            else :
                logging.debug("Nothing to do even if we are smart")
            aOneDevice.reset()
            
        for aOneDevice in iListOfDevice.registeredDevices:
            logging.debug("checking states : " + str(aOneDevice))
            if ((aOneDevice.id == 9) and (datetime.datetime.now() - self.lastPeopleDetectedCharles > datetime.timedelta (seconds = 600))):
                self.TurnCharlesLightOff(iListOfDevice)
            elif ((aOneDevice.id == 6) and (datetime.datetime.now() - self.lastPeopleDetectedEntree > datetime.timedelta (seconds = 180))):
                self.TurnEntreeLightOff(iListOfDevice)
            elif ((aOneDevice.type == "InterupteurStable") and (datetime.datetime.now() - aOneDevice.LastTMeaureDate > datetime.timedelta (seconds = 180))):
                aOneDevice.reset()
                
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
        fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
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
        
        logging.info("Looping on the devices and allow them to update themselve2.")
        for aOneObj in iListOfDevice.registeredDevices:
            #logging.info ("possible cmd : " + str(aOneObj.InPossibleCmd.keys()))
            if str(aCmdFromData) in aOneObj.InPossibleCmd.keys():
                logging.info("Updating device ID : " + str(aOneObj.id))
                aOneObj.executeCmd(str(aCmdFromData),str(aOriginFromData))
        
        fd.write(chr(aCmdFromData))
        
    def ReadDeviceStatus(self,iDataToWrite, iListOfDevice):
        aCmdFromData=int((iDataToWrite.split('_')[0]).split(':')[1])
        logging.info("Looking for the device : " + str(aCmdFromData))
        for aOneObj in iListOfDevice.registeredDevices:
            logging.info ("possible cmd : " + str(aOneObj.InPossibleCmd.keys()))
            if ((str(aCmdFromData) in aOneObj.InPossibleCmd.keys()) or (str(aCmdFromData) in aOneObj.OutPossibleCmd.keys())):
                logging.info("find it" + str(aOneObj.id))
                aRest = str(aOneObj.currentStatus)+"_"+str(aOneObj.LastTMeaureDate)
                logging.info("ret : " + aRest)
                return aRest
                
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
        aRetString = aRetString + "self.lastPeopleDetectedEntree : " + str(self.lastPeopleDetectedEntree) + "\n"
        aRetString = aRetString + "self.lastPeopleDetectedCharles : " + str(self.lastPeopleDetectedCharles) + "\n"
        return aRetString
