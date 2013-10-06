#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import logging
import time
import itertools
import json
import os
import sys
import inspect

from hashlib import sha1
import hmac

class WifiUser:
    '''Represents a wifi user'''

    def __init__(self):
        self.user_name=""

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + "self.user_name: " + str(self.user_name)
        return aRetString

class FreeboxApplication:
    '''Represents an application which interact with freebox server
    API doc : http://dev.freebox.fr/sdk/os/'''

    def __init__(self):
        #I kept the same parameter name than the one use in freebox API for more readability
        self.app_id="DomosId"
        self.app_name="DomosApp"
        self.app_version="1"
        self.device_name="DomosDeviceName"
        #To know if the APP is register on freeboxOS side
        self.registerIntoFreeboxServer=False
        #Registration parameters
        self.app_token=""
        self.track_id=""
        self.session_token=""
        self.loadAppTokenFromFile()

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + "self.app_id: " + str(self.app_id)
        aRetString = aRetString + "self.app_name: " + str(self.app_name)
        aRetString = aRetString + "self.app_version: " + str(self.app_version)
        aRetString = aRetString + "self.device_name: " + str(self.device_name)
        aRetString = aRetString + "self.registerIntoFreeboxServer: " + str(self.registerIntoFreeboxServer)
        aRetString = aRetString + "self.app_token: " + str(self.app_token)
        aRetString = aRetString + "self.track_id: " + str(self.track_id)
        return aRetString

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
            sys.exit(1)
        else:
            #Degeu...
            aAppTokenBackupFile = open("AppToken.txt", "w")
            aAppTokenBackupFile.write(self.app_token)
            aAppTokenBackupFile.close()
            #Fin Degeu

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
            return aRequestResult.json()
        logging.debug("Ending " + inspect.stack()[0][3])

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

    def changeWifiState(self,iWifiState):
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
        
    def computePassword(self, iChallenge):
        logging.debug("Starting " + inspect.stack()[0][3])

        hashed = hmac.new(self.app_token, iChallenge, sha1)
        logging.info("Password computed : " + str(hashed.digest().encode('hex')))
        return hashed.digest().encode('hex')
        
    def loginfull(self):
        logging.debug("Starting " + inspect.stack()[0][3])

        aNewChallenge = self.loginProcedure()
        #password = hmac-sha1(app_token, challenge)
        #voir http://stackoverflow.com/questions/8338661/implementaion-hmac-sha1-in-python
        #http://stackoverflow.com/questions/13019598/python-hmac-sha1-vs-java-hmac-sha1-different-results
        aPassword = self.computePassword(aNewChallenge)
        self.logWithPassword(aPassword)
        logging.debug("Ending " + inspect.stack()[0][3])


print ("Starting")

aLogFileToUse='WifiAutoControl.log'

#Clean previous log file
with open(aLogFileToUse, 'w'):
    pass 

logging.basicConfig(filename=aLogFileToUse,level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
#Change log level for REQUEST PYTHON API 
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)

aMyApp = FreeboxApplication()

aMyApp.loginfull()
aMyApp.getWifiConfig()
#aMyApp.changeWifiState(True)
aMyApp.getWifiConfig()

aWifiUsersFromApp = aMyApp.listWifiUser()
for aOneUser in aWifiUsersFromApp['result']:
    aWifiUser = WifiUser()
    aWifiUser.user_name=aOneUser[u'hostname']
    print ("User:" + str(aWifiUser) + "\n")

print ("Ending")
