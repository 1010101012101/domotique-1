#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import datetime
import time
import itertools
import os
import urllib
import serial
import json
import inspect
import requests
from hashlib import sha1
import hmac

class Function:
    '''Une classe generique qui decrit une fonctionalite (temperature, lampe, volet, ...)''' 
    
    def __init__(self):
        self.id =0
        self.type=""
        self.currentStatus =""
        self.LastTMeaureDate=datetime.datetime.now()
        self.LastRefreshDate=datetime.datetime.now()
        self.refreshRatemin = 3600
        self.description =""
        self.stateCanBeRefresh = False
        self.Reset =""
        self.InPossibleCmd ={}
        self.OutPossibleCmd ={}
        self.InActionsCommands ={}
        self.OutActionsCommands ={}
        self.PossibleStates ={}
        
    def executeInCmd(self,aCmdFromData,aData):
        exec(self.InActionsCommands[aCmdFromData])
        
    def executeOutCmd(self,aCmdFromData,aData):
        exec(self.OutActionsCommands[aCmdFromData])
        
    def reset(self):
        exec(self.Reset)
        
    def getDeviceWeightSpeech(self, Sentences):
        logging.warning("Speech matching for device : " + str(self.id) + " with sentence : " +  str(Sentences))
        aDeviceWeight = 0
        aCommand = None
        #command weight, command ID
        aBestCommand = (0,0)
        
        aSplitedSentences = Sentences.split("_")
        for aOnesentence in aSplitedSentences:
            logging.debug("sentence : " + aOnesentence)
            for aOneWord in aOnesentence.split("-"):
                #Compare match with word in device description
                for aOneDescriptionDeviceWord in self.description.split(" "):
                    logging.debug("compare : " + aOneWord +" and " + aOneDescriptionDeviceWord)
                    if (aOneWord==aOneDescriptionDeviceWord):
                        aDeviceWeight=aDeviceWeight+len(aOneWord)
                #Compare match with word in device possible commands
                for (aOnePossibleInCmdID,aOnePossibleInCmd) in self.InPossibleCmd.items():
                    logging.warning("checking new command : " + aOnePossibleInCmd )
                    aCommandWeight = 0
                    for aOnePossibleInCmdWord in aOnePossibleInCmd.split(" "):
                        logging.debug("compare : " + aOneWord +" and " + aOnePossibleInCmdWord)
                        if (aOneWord==aOnePossibleInCmdWord):
                            aCommandWeight=aCommandWeight+len(aOneWord)
                            aDeviceWeight=aDeviceWeight+len(aOneWord)
                    logging.warning("aCommandWeight : " + str(aCommandWeight) )
                    if(aCommandWeight>aBestCommand[0]):
                        aBestCommand=(aCommandWeight,int(aOnePossibleInCmdID))
        logging.debug("aDeviceWeight : " + str(aDeviceWeight))
        return (aDeviceWeight,aBestCommand[1])

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + "self.id : " + str(self.id) + "\n"
        aRetString = aRetString + "self.LastTMeaureDate : " + str(self.LastTMeaureDate) + "\n"
        aRetString = aRetString + "self.currentStatus : " + str(self.currentStatus) + "\n"
        aRetString = aRetString + "self.description : " + str(self.description) + "\n"
        aRetString = aRetString + "self.Reset : " + str(self.Reset) + "\n"
        aRetString = aRetString + "self.InPossibleCmd : " + str(self.InPossibleCmd) + "\n"
        aRetString = aRetString + "self.OutPossibleCmd : " + str(self.OutPossibleCmd) + "\n"
        aRetString = aRetString + "self.InActionsCommands : " + str(self.InActionsCommands) + "\n"
        aRetString = aRetString + "self.OutActionsCommands : " + str(self.OutActionsCommands) + "\n"
        aRetString = aRetString + "self.PossibleStates : " + str(self.PossibleStates) + "\n"
        return aRetString
        
class CapteurMesure(Function):
    '''Une classe qui decrit un capteur de mesure (temperature, lumiere, humidite, ...)''' 
    
    def __init__(self):
        Function.__init__(self)
        self.type="CapteurMesure"
        self.stateCanBeRefresh = True
        
    def UpdateValue(self,iData):
        self.currentStatus=iData
        self.LastTMeaureDate=datetime.datetime.now()
        
    def RequestNewValue(self):
        self.LastRefreshDate=datetime.datetime.now()
        aRefreshStr = str(self.OutPossibleCmd.keys()[0])
        logging.info ("Using "+ aRefreshStr + " to refresh")
        exec(self.InActionsCommands[aRefreshStr])

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + Function.__repr__(self) + "\n"
        aRetString = aRetString + "self.refreshRatemin : " + str(self.refreshRatemin) + "\n"
        return aRetString
        
class InterupteurBiStable(Function):
    '''Une classe qui decrit un interupteur bi stable (lumiere, PC, volets, ...)''' 
    
    def __init__(self):
        Function.__init__(self)
        self.type="InterupteurBiStable"
        self.PossibleStates=[ "off","on"]
        
    def RequestNewValue(self):
        self.LastRefreshDate=datetime.datetime.now()
        aRefreshStr = str(self.OutPossibleCmd.keys()[0])
        logging.info ("Using "+ aRefreshStr + " to refresh")
        exec(self.OutActionsCommands[aRefreshStr])
        
    def turnOn(self,iDataToSend):
        if((self.currentStatus=="off")or(self.currentStatus=="")):
            self.currentStatus="on"
            fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
            logging.info ("Writting "+ str(iDataToSend) + " to USB port and sending back to sender")
            fd.write(chr(iDataToSend))
        else:
            logging.error ("Device "+ str(self.id) + " can not be turn on because it is already on")
        
    def turnOff(self,iDataToSend):
        if((self.currentStatus=="on")or(self.currentStatus=="")):
            self.currentStatus="off"
            fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
            logging.info ("Writting "+ str(iDataToSend) + " to USB port and sending back to sender")
            fd.write(chr(iDataToSend))
        else:
            logging.error ("Device "+ str(self.id) + " can not be turn off because it is already off")

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + Function.__repr__(self) + "\n"
        return aRetString 
        
class InterupteurMultiStable(InterupteurBiStable):
    '''Une classe qui decrit un interupteur bi stable (lumiere, PC, volets, ...)''' 
    
    def __init__(self):
        Function.__init__(self)
        self.type="InterupteurMultiStable"
        self.PossibleStates=[ "off","on","unknow"]
        
    def RequestNewValue(self):
        self.LastRefreshDate=datetime.datetime.now()
        aRefreshStr = str(self.OutPossibleCmd.keys()[0])
        logging.info ("Using "+ aRefreshStr + " to refresh")
        exec(self.OutActionsCommands[aRefreshStr])
        
    def turnOn(self,iDataToSend):
        if((self.currentStatus=="off")or(self.currentStatus=="")):
            self.currentStatus="on"
            fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
            logging.info ("Writting "+ str(iDataToSend) + " to USB port and sending back to sender")
            fd.write(chr(iDataToSend))
        else:
            logging.error ("Device "+ str(self.id) + " can not be turn on because it is already on")
        
    def turnOff(self,iDataToSend):
        if((self.currentStatus=="on")or(self.currentStatus=="")):
            self.currentStatus="off"
            fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
            logging.info ("Writting "+ str(iDataToSend) + " to USB port and sending back to sender")
            fd.write(chr(iDataToSend))
        else:
            logging.error ("Device "+ str(self.id) + " can not be turn off because it is already off")
            
    def stop(self,iDataToSend):
        self.currentStatus=""
        fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
        logging.info ("Writting "+ str(iDataToSend) + " to USB port and sending back to sender")
        fd.write(chr(iDataToSend))

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + Function.__repr__(self) + "\n"
        return aRetString 

class InterupteurStable(Function):
    '''Une classe qui decrit un interupteur stable (detecteur presence, ...)''' 
    
    def __init__(self):
        Function.__init__(self)
        self.stateForceByUser = False
        self.type="InterupteurStable"
        self.PossibleStates=[ "unstable","stable"]
        self.DateTimeStateForce = datetime.datetime.now()
        
    def detectionEventReceived(self):
        self.currentStatus="unstable"
        self.LastTMeaureDate=datetime.datetime.now()

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + Function.__repr__(self)
        aRetString = aRetString + "self.stateForceByUser : " + str(self.stateForceByUser) + "\n"
        aRetString = aRetString + "self.DateTimeStateForce : " + str(self.DateTimeStateForce) + "\n"
        return aRetString 
        
class Complex(Function):
    '''Une classe qui decrit un interupteur stable (detecteur presence, ...)''' 
    
    def __init__(self):
        Function.__init__(self)
        self.type="Complex"

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + Function.__repr__(self)
        return aRetString 
        
    def sendMsgToFreebox(self,key):
        url = "http://hd1.freebox.fr/pub/remote_control?" + "key=" + key + "&code=59999459"
        logging.error("sending : " + url)
        reponse = urllib.urlopen(url)
        logging.error("reponse : " + str(reponse))

class FreeboxWifi(Function):
    '''Une classe qui decrit un interupteur stable (detecteur presence, ...)''' 

    class WifiUser:
        '''Represents a wifi user'''

        def __init__(self):
            self.user_name=""
            self.last_activity=""

        def __repr__(self):
            aRetString = "self.__dict__: " + str(self.__dict__)
            return aRetString
    
    def __init__(self):
        Function.__init__(self)
        #I kept the same parameter name than the one use in freebox API for more readability
        self.app_id="DomosId"
        self.app_name="DomosApp"
        self.app_version="1"
        self.device_name="DomosDeviceName"
        #To know if the APP is register on freeboxOS side
        self.registerIntoFreeboxServer=False
        #Registration parameters
        self.app_token=""
        self.users = []
        self.track_id=""
        self.session_token=""
        self.loadAppTokenFromFile()

    def __repr__(self):
        aRetString = "self.__dict__: " + str(self.__dict__)
        return aRetString

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + Function.__repr__(self)
        return aRetString

    def computePassword(self, iChallenge):
        logging.debug("Starting " + inspect.stack()[0][3])
        hashed = hmac.new(self.app_token, iChallenge, sha1)
        logging.info("Password computed : " + str(hashed.digest().encode('hex')))
        return hashed.digest().encode('hex')
        
    def loginProcedure(self):
        logging.debug("Starting " + inspect.stack()[0][3])
        aRequestUrl = "http://mafreebox.freebox.fr/api/v1/login/"
        aHeaders = {'Content-type': 'application/json', 'Accept': 'application/json'}
        aRequestResult = requests.get(aRequestUrl, headers=aHeaders)

        if (aRequestResult.status_code != requests.codes.ok) or (aRequestResult.json()['success'] != True):
            logging.critical("Error in " + inspect.stack()[0][3])
        else:
            achallenge=aRequestResult.json()['result']['challenge']
            logging.debug("We have the challenge : " + str(achallenge))
            return achallenge

    def logWithPassword(self, iPassword):
        #only once. Register the APP on freebox side
        logging.debug("Starting " + inspect.stack()[0][3])
        aRequestUrl = "http://mafreebox.freebox.fr/api/v1/login/session/"
        aHeaders = {'Content-type': 'application/json', 'Accept': 'application/json'}
        aDataToLog = json.dumps({"app_id": self.app_id,"password": iPassword})

        aRequestResult = requests.post(aRequestUrl, data=aDataToLog, headers=aHeaders)
        logging.debug("Request result : " + str(aRequestResult.json()))

        if (aRequestResult.status_code != requests.codes.ok) or (aRequestResult.json()['success'] != True):
            logging.critical("Error in " + inspect.stack()[0][3])
        else:
            self.session_token=aRequestResult.json()['result']['session_token']
        logging.debug("Ending " + inspect.stack()[0][3])

    def trackRegristration(self):
        logging.debug("Starting " + inspect.stack()[0][3])
        aRequestUrl = "http://mafreebox.freebox.fr/api/v1/login/authorize/" + str(self.track_id)
        aHeaders = {'Content-type': 'application/json', 'Accept': 'application/json'}
        aRequestResult = requests.get(aRequestUrl, headers=aHeaders)

        if (aRequestResult.status_code != requests.codes.ok) or (aRequestResult.json()['result']['status'] != "granted"):
            logging.critical("Error in " + inspect.stack()[0][3])
        else:
            self.registerIntoFreeboxServer=True
        logging.debug("Ending " + inspect.stack()[0][3])

    def initialLogging(self):
        #only once. Register the APP on freebox side
        logging.debug("Starting " + inspect.stack()[0][3])

        aRequestUrl = "http://mafreebox.freebox.fr/api/v1/login/authorize/"
        aHeaders = {'Content-type': 'application/json', 'Accept': 'application/json'}
        aDataToLog = json.dumps({"app_id": self.app_id,"app_name": self.app_name,"app_version": self.app_version,"device_name": self.device_name})

        aRequestResult = requests.post(aRequestUrl, data=aDataToLog, headers=aHeaders)

        if (aRequestResult.status_code != requests.codes.ok) or (aRequestResult.json()['success'] != True):
            logging.critical("Error during intial registration into Freebox Server")
        else:
            logging.debug("Please go to your Freebox. There should be a message saying that an application request access to freebox API. Please validate the request using the front display")
            self.app_token = aRequestResult.json()['result']['app_token']
            self.track_id = aRequestResult.json()['result']['track_id']
            logging.debug("app_token : " + str(self.app_token))
            logging.debug("track_id : " + str(self.track_id))
        logging.info("Ending initial registration")
        
        aLoopInd = 0
        while ((self.registerIntoFreeboxServer != True) and (aLoopInd < 10)):
            self.trackRegristration()
            time.sleep(15)  # Delay for 1 minute (60 seconds)
            aLoopInd = aLoopInd + 1
        if (self.registerIntoFreeboxServer != True):
            logging.critical("Initial registration fails - Exiting with error")
        else:
            #Degeu...
            aAppTokenBackupFile = open("AppToken.txt", "w")
            aAppTokenBackupFile.write(self.app_token)
            aAppTokenBackupFile.close()
            #Fin Degeu

    def loadAppTokenFromFile(self):
        #Degeu...
        logging.debug("Starting " + inspect.stack()[0][3])
        if (os.path.isfile("AppToken.txt")):
            aAppTokenBackupFile = open("AppToken.txt", "r")
            self.app_token = aAppTokenBackupFile.read()
            logging.info("APP token read from file. New APP token is : " + str(self.app_token))
            aAppTokenBackupFile.close()
        else:
            logging.info("No file for APP token - request a new one")
            self.initialLogging()
        #Fin Degeu

    def getLastActivity(self):
        aLastActivity = datetime.datetime(2007, 12, 5)
        for aOneUser in self.users:
            if aOneUser.last_activity > aLastActivity:
                aLastActivity=aOneUser.last_activity
        return aLastActivity

    def listWifiUser(self):
        logging.debug("Starting " + inspect.stack()[0][3])
        aRequestUrl = "http://mafreebox.freebox.fr/api/v1/wifi/stations/perso/"
        aHeaders = {'Content-type': 'application/json', 'Accept': 'application/json','X-Fbx-App-Auth':self.session_token}
        aRequestResult = requests.get(aRequestUrl, headers=aHeaders)

        if (aRequestResult.status_code != requests.codes.ok) or (aRequestResult.json()['success'] != True):
            logging.critical("Error in " + inspect.stack()[0][3])
        else:
            aNbUser=len(aRequestResult.json()['result'])
            logging.info("Nb user : " + str(aNbUser))
            logging.info("Nb user : " + str(aRequestResult.json()))
            for aOneUser in aRequestResult.json()['result']:
                aWifiUser = WifiUser()
                aWifiUser.user_name=aOneUser[u'hostname']
                aWifiUser.last_activity = datetime.datetime.fromtimestamp(aOneUser[u'host'][u'last_time_reachable'])
                self.users.append(aWifiUser)
        logging.debug("Ending " + inspect.stack()[0][3])

    def loginfull(self):
        logging.debug("Starting " + inspect.stack()[0][3])

        aNewChallenge = self.loginProcedure()
        #password = hmac-sha1(app_token, challenge)
        #voir http://stackoverflow.com/questions/8338661/implementaion-hmac-sha1-in-python
        #http://stackoverflow.com/questions/13019598/python-hmac-sha1-vs-java-hmac-sha1-different-results
        aPassword = self.computePassword(aNewChallenge)
        self.logWithPassword(aPassword)
        logging.debug("Ending " + inspect.stack()[0][3])

    def changeWifiState(self,iWifiState):
        self.loginfull()
        logging.debug("Starting " + inspect.stack()[0][3])
        aRequestUrl = "http://mafreebox.freebox.fr/api/v1/wifi/config/"
        aHeaders = {'Content-type': 'application/json', 'Accept': 'application/json','X-Fbx-App-Auth':self.session_token}
        aDataToLog = json.dumps({"ap_params": {"enabled": iWifiState}})
        aRequestResult = requests.put(aRequestUrl,data=aDataToLog, headers=aHeaders)

        if (aRequestResult.status_code != requests.codes.ok) or (aRequestResult.json()['success'] != True):
            logging.critical("Error in " + inspect.stack()[0][3])
            logging.critical("Request results : " + str(aRequestResult.json()))
        else:
            logging.info("Wifi should be off")
        logging.debug("Ending " + inspect.stack()[0][3])

    def turnWifiOn(self):
        logging.critical("Turning wifi ON")
        self.changeWifiState(True)

    def stopWifi(self):
        logging.critical("Turning wifi OFF")
        self.changeWifiState(False)

    def turnwifiOff(self):
        logging.critical("Turning wifi OFF")
        self.changeWifiState(False)

    def getWifiConfig(self):
        logging.debug("Starting " + inspect.stack()[0][3])
        aRequestUrl = "http://mafreebox.freebox.fr/api/v1/wifi/config/"
        aHeaders = {'Content-type': 'application/json', 'Accept': 'application/json','X-Fbx-App-Auth':self.session_token}
        aRequestResult = requests.get(aRequestUrl, headers=aHeaders)

        if (aRequestResult.status_code != requests.codes.ok) or (aRequestResult.json()['success'] != True):
            logging.critical("Error in " + inspect.stack()[0][3])
        else:
            logging.info("Wifi config : " + str(aRequestResult.json()))
        logging.debug("Ending " + inspect.stack()[0][3])




class PhysicalDevice:
    '''Une classe generique qui decrit une carte physique et possede 1 ou plusieurs fonction''' 
    
    def __init__(self):
        self.id =0
        
class DevicesHandler:
    '''Une classe qui gere un ensemble de fonctionalite''' 
    
    def __init__(self, iConfig):
        self.registeredDevices =[]
        self.config = iConfig
        
    def getDevice(self,iDeviceId):
        for aOneDevice in self.registeredDevices:
            if (aOneDevice.id == iDeviceId):
                logging.debug("checking states : " + str(aOneDevice.id))
                return aOneDevice
        
    def loadDevices(self):
        #for aOneDeviceFile in glob.glob("*.device"):
            #f = open(aOneDeviceFile)
            #json_str = f.read()
            #aOneDeviceObj = jsonpickle.decode(json_str)
            #self.registeredDevices.append(aOneDeviceObj)
            
        charlesT = CapteurMesure()
        charlesT.OutPossibleCmd ={"15" : "recoit Nouvelle T"}
        charlesT.description="capteur temperature chambre Charles"
        charlesT.InPossibleCmd ={"15" : "recoit Nouvelle T"}
        charlesT.OutActionsCommands ={"15" : "self.UpdateValue(aData)"}
        charlesT.InActionsCommands ={"15" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 15 to USB port and sending back to sender")
fd.write(chr(15))"""}
        charlesT.id =15
        charlesT.refreshRatemin = 240
        self.registeredDevices.append(charlesT)
        
        charlesH = CapteurMesure()
        charlesH.description="capteur humidite chambre Charles"
        charlesH.OutPossibleCmd ={"16" : "recoit Nouvelle H"}
        charlesH.InPossibleCmd ={"16" : "recoit Nouvelle H"}
        charlesH.InActionsCommands ={"16" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 16 to USB port and sending back to sender")
fd.write(chr(16))"""}
        charlesH.OutActionsCommands ={"16" : "self.UpdateValue(aData)"}
        charlesH.id =16
        charlesH.refreshRatemin = 250
        self.registeredDevices.append(charlesH)
        
        entreeT = CapteurMesure()
        entreeT.description="capteur temperature entree"
        entreeT.OutPossibleCmd ={"30" : "recoit Nouvelle T"}
        entreeT.InPossibleCmd ={"30" : "recoit Nouvelle T"}
        entreeT.InActionsCommands ={"30" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 30 to USB port and sending back to sender")
fd.write(chr(30))"""}
        entreeT.OutActionsCommands ={"30" : "self.UpdateValue(aData)"}
        entreeT.id =17
        entreeT.refreshRatemin = 260
        self.registeredDevices.append(entreeT)
        
        SalonT = CapteurMesure()
        SalonT.OutPossibleCmd ={"18" : "recoit Nouvelle T"}
        SalonT.description="capteur temperature salon"
        SalonT.InPossibleCmd ={"18" : "recoit Nouvelle T"}
        SalonT.InActionsCommands ={"18" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 18 to USB port and sending back to sender")
fd.write(chr(18))"""}
        SalonT.OutActionsCommands ={"18" : "self.UpdateValue(aData)"}
        SalonT.id =24
        SalonT.refreshRatemin = 265
        self.registeredDevices.append(SalonT)
        
        salonH = CapteurMesure()
        salonH.OutPossibleCmd ={"19" : "recoit Nouvelle H"}
        salonH.description="capteur humidite salon"
        salonH.InPossibleCmd ={"19" : "recoit Nouvelle H"}
        salonH.InActionsCommands ={"19" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 19 to USB port and sending back to sender")
fd.write(chr(19))"""}
        salonH.OutActionsCommands ={"19" : "self.UpdateValue(aData)"}
        salonH.id =25
        salonH.refreshRatemin = 275
        self.registeredDevices.append(salonH)
        
        CuisineT = CapteurMesure()
        CuisineT.OutPossibleCmd ={"39" : "recoit Nouvelle T"}
        CuisineT.description="capteur temperature cuisine"
        CuisineT.InPossibleCmd ={"39" : "recoit Nouvelle T"}
        CuisineT.InActionsCommands ={"39" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 39 to USB port and sending back to sender")
fd.write(chr(39))"""}
        CuisineT.OutActionsCommands ={"39" : "self.UpdateValue(aData)"}
        CuisineT.id =21
        CuisineT.refreshRatemin = 270
        self.registeredDevices.append(CuisineT)
        
        CuisineH = CapteurMesure()
        CuisineH.OutPossibleCmd ={"40" : "recoit Nouvelle T"}
        CuisineH.description="capteur humidite cuisine"
        CuisineH.refreshRatemin = 280
        CuisineH.InPossibleCmd ={"40" : "recoit Nouvelle T"}
        CuisineH.InActionsCommands ={"40" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 40 to USB port and sending back to sender")
fd.write(chr(40))"""}
        CuisineH.OutActionsCommands ={"40" : "self.UpdateValue(aData)"}
        CuisineH.id =23
        self.registeredDevices.append(CuisineH)
        
        entreeH = CapteurMesure()
        entreeH.OutPossibleCmd ={"31" : "recoit Nouvelle H"}
        entreeH.description="capteur humidite entree"
        entreeH.InPossibleCmd ={"31" : "recoit Nouvelle H"}
        entreeH.InActionsCommands ={"31" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 31 to USB port and sending back to sender")
fd.write(chr(31))"""}
        entreeH.OutActionsCommands ={"31" : "self.UpdateValue(aData)"}
        entreeH.id =18
        entreeH.refreshRatemin = 290
        self.registeredDevices.append(entreeH)
        
        lumiereCharles = InterupteurBiStable()
        lumiereCharles.id =1
        lumiereCharles.description="lumiere plafond principale chambre Charles"
        lumiereCharles.InPossibleCmd ={ "5" : "on allume allumer","6" : "off eteint eteindre"}
        lumiereCharles.InActionsCommands={ "5" : "self.turnOn(5)","6" : "self.turnOff(6)"}
        self.registeredDevices.append(lumiereCharles)
        
        PcCharles = InterupteurBiStable()
        PcCharles.id =19
        PcCharles.stateCanBeRefresh = True
        PcCharles.description="PC ordinateur Charles"
        PcCharles.OutPossibleCmd ={"61" : "checkStatus"}
        PcCharles.InPossibleCmd ={ "60" : "on allume allumer", "62" : "off eteint eteindre"}
        PcCharles.InActionsCommands={ "60" : """self.currentStatus=\"on\"
os.system('sudo /usr/sbin/etherwake 20:cf:30:ca:8a:50')""", "62" : "os.system('net rpc shutdown -f -I 192.168.0.7 -U charles%"+self.config["WinPasswdRpcShutdown"]+"')"}
        PcCharles.OutActionsCommands={"61" : """self.LastTMeaureDate=datetime.datetime.now()
logging.info ("refresh pc")
if os.system('ping -c 1 -W 2 192.168.0.7'):
    self.currentStatus="off"
    logging.info ("off")
else:
    self.currentStatus="on"
    logging.info ("on")"""}
        PcCharles.refreshRatemin = 300
        self.registeredDevices.append(PcCharles)
        
        lumiere2Charles = InterupteurBiStable()
        lumiere2Charles.id =3
        lumiere2Charles.description="lumiere secondaire Charles ambiance d'ambiance secondaires"
        lumiere2Charles.InPossibleCmd ={ "11" : "on allumer allume","12" : "off eteint eteindre"}
        lumiere2Charles.InActionsCommands={ "11" : "self.turnOn(11)","12" : "self.turnOff(12)"}
        self.registeredDevices.append(lumiere2Charles)
        
        VoletCharles = InterupteurMultiStable()
        VoletCharles.id =4
        VoletCharles.description="volets chambre Charles"
        VoletCharles.InPossibleCmd ={ "8" : "off ferme fermer","7" : "on ouvrir ouvre","24" : "stop arreter arrete"}
        VoletCharles.InActionsCommands={ "7" : "self.turnOn(7)","8" : "self.turnOff(8)","24" : "self.stop(8)"}
        self.registeredDevices.append(VoletCharles)
        
        VoletSalon = InterupteurMultiStable()
        VoletSalon.id =5
        VoletSalon.description="volets salon"
        VoletSalon.InPossibleCmd ={ "10" : "off fermer ferme","9" : "on ouvre ouvrir","25" : "stop arreter arrete"}
        VoletSalon.InActionsCommands={ "9" : "self.turnOn(9)","10" : "self.turnOff(10)","25" : "self.stop(10)"}
        self.registeredDevices.append(VoletSalon)
        
        LumiereSalonHalogene = InterupteurBiStable()
        LumiereSalonHalogene.id =6
        LumiereSalonHalogene.description="lumiere halogene salon"
        LumiereSalonHalogene.InPossibleCmd ={ "13" : "off eteint eteindre","14" : "on allume allumer"}
        LumiereSalonHalogene.InActionsCommands={ "13" : "self.turnOff(13)","14" : "self.turnOn(14)"}
        self.registeredDevices.append(LumiereSalonHalogene)

        #Wifi freebox
        WifiFreeboxCharles = FreeboxWifi()
        WifiFreeboxCharles.id =28
        WifiFreeboxCharles.description="wifi freebox"
        WifiFreeboxCharles.InPossibleCmd ={ "26" : "off eteint eteindre","27" : "on allume allumer"}
        WifiFreeboxCharles.InActionsCommands={ "26" : "self.stopWifi()","27" : "self.turnWifiOn()"}
        self.registeredDevices.append(WifiFreeboxCharles)
        
        ChaffageSdb = InterupteurBiStable()
        ChaffageSdb.id =7
        ChaffageSdb.description="chauffage salle de baim"
        ChaffageSdb.InPossibleCmd ={ "42" : "off eteint eteindre","43" : "on allumer allume"}
        ChaffageSdb.InActionsCommands={ "42" : "self.turnOff(42)","43" : "self.turnOn(43)"}
        self.registeredDevices.append(ChaffageSdb)
        
        Lumiereentree = InterupteurBiStable()
        Lumiereentree.id =8
        Lumiereentree.description="lumiere led guirlande entree"
        Lumiereentree.InPossibleCmd ={ "34" : "on allume allumer","35" : "off etient eteindre"}
        Lumiereentree.InActionsCommands={ "34" : "self.turnOn(34)","35" : "self.turnOff(35)"}
        self.registeredDevices.append(Lumiereentree)
        
        GuirlandeLedCuisine = InterupteurBiStable()
        GuirlandeLedCuisine.id =11
        GuirlandeLedCuisine.description="lumiere led guirlande cuisine"
        GuirlandeLedCuisine.InPossibleCmd ={ "47" : "off eteint eteindre","46" : "on allumer allume"}
        GuirlandeLedCuisine.InActionsCommands={ "46" : "self.turnOn(46)","47" : "self.turnOff(47)"}
        self.registeredDevices.append(GuirlandeLedCuisine)
        
        GuirlandeLedSalon = InterupteurBiStable()
        GuirlandeLedSalon.id =12
        GuirlandeLedSalon.description="lumiere led guirlande salon"
        GuirlandeLedSalon.InPossibleCmd ={ "3" : "on allumer allume","4" : "off eteint eteindre"}
        GuirlandeLedSalon.InActionsCommands={ "3" : "self.turnOn(3)","4" : "self.turnOff(4)"}
        self.registeredDevices.append(GuirlandeLedSalon)
        
        luminoTersa = CapteurMesure()
        luminoTersa.stateCanBeRefresh = False
        luminoTersa.description="capteur lumiere luminosite terrasse soleil"
        luminoTersa.OutPossibleCmd ={"36" : "recoit Nouvelle L"}
        luminoTersa.InPossibleCmd ={"36" : "recoit Nouvelle L"}
        luminoTersa.InActionsCommands ={"36" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 31 to USB port and sending back to sender")
fd.write(chr(36))"""}
        luminoTersa.OutActionsCommands ={"36" : "self.UpdateValue(aData)"}
        luminoTersa.id =22
        self.registeredDevices.append(luminoTersa)
        
        TerrasseTemperature = CapteurMesure()
        TerrasseTemperature.stateCanBeRefresh = False
        TerrasseTemperature.description="capteur temperature terrasse"
        TerrasseTemperature.OutPossibleCmd ={"37" : "recoit Nouvelle L"}
        TerrasseTemperature.InPossibleCmd ={"37" : "recoit Nouvelle L"}
        TerrasseTemperature.InActionsCommands ={"37" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 31 to USB port and sending back to sender")
fd.write(chr(37))"""}
        TerrasseTemperature.OutActionsCommands ={"37" : "self.UpdateValue(aData)"}
        TerrasseTemperature.id =20
        self.registeredDevices.append(TerrasseTemperature)
        
        TerrasseHumidite = CapteurMesure()
        TerrasseHumidite.stateCanBeRefresh = False
        TerrasseHumidite.description="capteur humidite terrasse"
        TerrasseHumidite.OutPossibleCmd ={"38" : "recoit Nouvelle L"}
        TerrasseHumidite.InPossibleCmd ={"38" : "recoit Nouvelle L"}
        TerrasseHumidite.InActionsCommands ={"38" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 31 to USB port and sending back to sender")
fd.write(chr(38))"""}
        TerrasseHumidite.OutActionsCommands ={"38" : "self.UpdateValue(aData)"}
        TerrasseHumidite.id =26
        self.registeredDevices.append(TerrasseHumidite)
        
        DetecteurPresenceCharles = InterupteurStable()
        DetecteurPresenceCharles.id =9
        DetecteurPresenceCharles.description="detecteur presence Charles"
        DetecteurPresenceCharles.OutPossibleCmd ={ "2" : "unstable position"}
        DetecteurPresenceCharles.OutActionsCommands={ "2" : "self.detectionEventReceived()"}
        DetecteurPresenceCharles.Reset = "self.currentStatus=\"stable\""
        self.registeredDevices.append(DetecteurPresenceCharles)
        
        DetecteurPresenceSalon = InterupteurStable()
        DetecteurPresenceSalon.id =13
        DetecteurPresenceSalon.description="detecteur presence salon"
        DetecteurPresenceSalon.OutPossibleCmd ={ "17" : "unstable position"}
        DetecteurPresenceSalon.OutActionsCommands={ "17" : "self.detectionEventReceived()"}
        DetecteurPresenceSalon.Reset = "self.currentStatus=\"stable\""
        self.registeredDevices.append(DetecteurPresenceSalon)
        
        DetecteurFumeeCuisine = InterupteurStable()
        DetecteurFumeeCuisine.id =2
        DetecteurFumeeCuisine.OutPossibleCmd ={ "1" : "unstable position"}
        DetecteurFumeeCuisine.OutActionsCommands={ "1" : "self.detectionEventReceived()"}
        DetecteurFumeeCuisine.Reset = "self.currentStatus=\"stable\""
        #self.registeredDevices.append(DetecteurFumeeCuisine)
        
        DetecteurPresenceEntree = InterupteurStable()
        DetecteurPresenceEntree.id =10
        DetecteurPresenceEntree.description="detecteur presence entree"
        DetecteurPresenceEntree.OutPossibleCmd ={ "50" : "unstable position"}
        DetecteurPresenceEntree.OutActionsCommands={ "50" : "self.detectionEventReceived()"}
        DetecteurPresenceEntree.Reset = "self.currentStatus=\"stable\""
        self.registeredDevices.append(DetecteurPresenceEntree)
        
        DetecteurPresenceCuisine = InterupteurStable()
        DetecteurPresenceCuisine.id =27
        DetecteurPresenceCuisine.description="detecteur presence cuisine"
        DetecteurPresenceCuisine.OutPossibleCmd ={ "51" : "unstable position"}
        DetecteurPresenceCuisine.OutActionsCommands={ "51" : "self.detectionEventReceived()"}
        DetecteurPresenceCuisine.Reset = "self.currentStatus=\"stable\""
        self.registeredDevices.append(DetecteurPresenceCuisine)
        
        Freebox = Complex()
        Freebox.id = 28
        Freebox.description="freebox television TV tele"
        Freebox.InPossibleCmd ={ "63" : "chaine+1 chaine augmenter augmente","64" : "chaine-1 diminuer diminue","65" : "off allumer allume on","20" : "chaine 1 un","21" : "chaine 6 six","22" : "chaine 9 neuf","23" : "ok"}
        Freebox.InActionsCommands={ "64" : "self.sendMsgToFreebox(\"prgm_inc\")","63" : "self.sendMsgToFreebox(\"prgm_dec\")","65" : "self.sendMsgToFreebox(\"power\")","20" : "self.sendMsgToFreebox(\"1\")","21" : "self.sendMsgToFreebox(\"6\")","22" : "self.sendMsgToFreebox(\"9\")","23" : "self.sendMsgToFreebox(\"ok\")"}
        self.registeredDevices.append(Freebox)
        #http://hd1.freebox.fr/pub/remote_control?code=59999459&key=2
        
    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + "self.registeredDevices : " + str(self.registeredDevices) + "\n"
        aRetString = aRetString + "self.config : " + str(self.config) + "\n"
        return aRetString
        
    def listDevices(self):
        aRetString = ""
        for aOneDevice in self.registeredDevices:
            aRetString = aRetString + "Device : " + str(aOneDevice.id) + "\n"
        return aRetString
