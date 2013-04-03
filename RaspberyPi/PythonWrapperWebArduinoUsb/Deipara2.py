#!/usr/bin/python

import glob
import jsonpickle
import logging
import datetime
import serial

###################################################################################
########## Brain class....smart one       #########################################
###################################################################################

class Brain:
    "Une classe qui pense"
    
    def __init__(self):
        self.lastPeopleDetectedEntree =datetime.datetime.now()
        self.lastPeopleDetectedCharles =datetime.datetime.now()
        
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

    def smartProcessing2(self,iListOfDevice):
        logging.debug("Trying to be smart")
        for aOneDevice in iListOfDevice.registeredDevices:
            logging.debug("checking event : " + str(aOneDevice))
            if ((aOneDevice.id == 2) and (aOneDevice.currentStatus=="incendie en cours")):
                sendEmailFireDetected()
            elif ((aOneDevice.id == 6) and (aOneDevice.currentStatus=="personne detecte")):
                self.PeopleDetectedEntree(iListOfDevice)
            elif ((aOneDevice.id == 7) and (aOneDevice.currentStatus=="personne detecte")):
                self.PeopleDetectedCharlesRoom(iListOfDevice)
            else :
                logging.debug("Nothing to do even if we are smart")
            aOneDevice.reset()
            
        for aOneDevice in iListOfDevice.registeredDevices:
            logging.debug("checking states : " + str(aOneDevice))
            if ((aOneDevice.id == 7) and (datetime.datetime.now() - self.lastPeopleDetectedCharles > datetime.timedelta (seconds = 600))):
                self.TurnCharlesLightOff(iListOfDevice)
            elif ((aOneDevice.id == 6) and (datetime.datetime.now() - self.lastPeopleDetectedEntree > datetime.timedelta (seconds = 180))):
                self.TurnEntreeLightOff(iListOfDevice)
                
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

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + "self.lastPeopleDetectedEntree : " + str(self.lastPeopleDetectedEntree) + "\n"
        aRetString = aRetString + "self.lastPeopleDetectedCharles : " + str(self.lastPeopleDetectedCharles) + "\n"
        return aRetString

###################################################################################
########## Classes used to store datas    #########################################
###################################################################################
        
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
        
    def executeCmd(self,aCmdFromData,aData):
        exec(self.ActionsCommands[aCmdFromData])
        
    def reset(self):
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
        
class Temperature(Object):
    "Une classe qui decrit un capteur"
    
    def __init__(self):
        Object.__init__(self)
        self.temperature="0"
        self.humidite="0"
        self.LastTMeaureDate=datetime.datetime.now()
        self.LastHMeaureDate=datetime.datetime.now()

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + Object.__repr__(self) + "\n"
        aRetString = aRetString + "self.temperature : " + str(self.temperature) + "\n"
        aRetString = aRetString + "self.humidite : " + str(self.humidite) + "\n"
        aRetString = aRetString + "self.LastTMeaureDate : " + str(self.LastTMeaureDate) + "\n"
        aRetString = aRetString + "self.LastHMeaureDate : " + str(self.LastHMeaureDate) + "\n"
        return aRetString
        
class InterupteurBiStable(Object):
    "Une classe qui decrit un capteur"
    
    def __init__(self):
        Object.__init__(self)
        self.status="off"

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + Object.__repr__(self) + "\n"
        aRetString = aRetString + "self.status : " + str(self.status) + "\n"
        return aRetString 

class InterupteurStable(Object):
    "Une classe qui decrit un capteur"
    
    def __init__(self):
        Object.__init__(self)
        self.status="off"

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + Object.__repr__(self) + "\n"
        aRetString = aRetString + "self.status : " + str(self.status) + "\n"
        return aRetString 

        
        
class DevicesHandler:
    "Gere un ensemble de devices"
    
    def __init__(self):
        self.registeredDevices =[]
        
    def loadDevices(self):
        #for aOneDeviceFile in glob.glob("*.device"):
            #f = open(aOneDeviceFile)
            #json_str = f.read()
            #aOneDeviceObj = jsonpickle.decode(json_str)
            #self.registeredDevices.append(aOneDeviceObj)
            
        charlesT = Temperature()
        charlesT.OutPossibleCmd ={"15" : "recoit Nouvelle T","16" : "recoit Nouvelle H"}
        charlesT.ActionsCommands ={"15" : "self.temperature=aData","16" : "self.humidite=aData"}
        charlesT.id =15
        self.registeredDevices.append(charlesT)
        
        entreeT = Temperature()
        charlesT.OutPossibleCmd ={"30" : "recoit Nouvelle T","31" : "recoit Nouvelle H"}
        charlesT.ActionsCommands ={"30" : "self.temperature=aData","31" : "self.humidite=aData"}
        charlesT.id =17
        self.registeredDevices.append(entreeT)
        
        lumiereCharles = InterupteurBiStable()
        lumiereCharles.PossibleStates=[ "on","off"]
        lumiereCharles.id =1
        lumiereCharles.InPossibleCmd ={ "5" : "on","6" : "off"}
        lumiereCharles.ActionsCommands={ "5" : "self.currentStatus=\"on\"","6" : "self.currentStatus=\"off\""}
        self.registeredDevices.append(lumiereCharles)
        
        lumiere2Charles = InterupteurBiStable()
        lumiere2Charles.PossibleStates=[ "on","off"]
        lumiere2Charles.id =3
        lumiere2Charles.InPossibleCmd ={ "11" : "on","12" : "off"}
        lumiere2Charles.ActionsCommands={ "11" : "self.currentStatus=\"on\"","12" : "self.currentStatus=\"off\""}
        self.registeredDevices.append(lumiere2Charles)
        
        VoletCharles = InterupteurBiStable()
        VoletCharles.PossibleStates=[ "on","off"]
        VoletCharles.id =4
        VoletCharles.InPossibleCmd ={ "7" : "on","8" : "off"}
        VoletCharles.ActionsCommands={ "7" : "self.currentStatus=\"on\"","8" : "self.currentStatus=\"off\""}
        self.registeredDevices.append(VoletCharles)
        
        VoletCharles = InterupteurBiStable()
        VoletCharles.PossibleStates=[ "on","off"]
        VoletCharles.id =5
        VoletCharles.InPossibleCmd ={ "9" : "on","10" : "off"}
        VoletCharles.ActionsCommands={ "9" : "self.currentStatus=\"on\"","10" : "self.currentStatus=\"off\""}
        self.registeredDevices.append(VoletCharles)
        
        LumiereSalonHalogene = InterupteurBiStable()
        LumiereSalonHalogene.PossibleStates=[ "on","off"]
        LumiereSalonHalogene.id =6
        LumiereSalonHalogene.InPossibleCmd ={ "13" : "on","14" : "off"}
        LumiereSalonHalogene.ActionsCommands={ "13" : "self.currentStatus=\"on\"","14" : "self.currentStatus=\"off\""}
        self.registeredDevices.append(LumiereSalonHalogene)
        
        ChaffageSdb = InterupteurBiStable()
        ChaffageSdb.PossibleStates=[ "on","off"]
        ChaffageSdb.id =7
        ChaffageSdb.InPossibleCmd ={ "42" : "on","43" : "off"}
        ChaffageSdb.ActionsCommands={ "42" : "self.currentStatus=\"on\"","43" : "self.currentStatus=\"off\""}
        self.registeredDevices.append(ChaffageSdb)
        
        Lumiereentree = InterupteurBiStable()
        Lumiereentree.PossibleStates=[ "on","off"]
        Lumiereentree.id =7
        Lumiereentree.InPossibleCmd ={ "34" : "on","35" : "off"}
        Lumiereentree.ActionsCommands={ "34" : "self.currentStatus=\"on\"","35" : "self.currentStatus=\"off\""}
        self.registeredDevices.append(Lumiereentree)
        
        VoletCharles = InterupteurStable()
        VoletCharles.PossibleStates=[ "on","off"]
        VoletCharles.id =9
        VoletCharles.OutPossibleCmd ={ "2" : "detected"}
        VoletCharles.ActionsCommands={ "2" : "self.currentStatus=\"on\""}
        VoletCharles.Reset = "self.currentStatus=\"pas personne detecte\""
        self.registeredDevices.append(VoletCharles)
        

        
    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + "self.registeredDevices : " + str(self.registeredDevices) + "\n"
        return aRetString