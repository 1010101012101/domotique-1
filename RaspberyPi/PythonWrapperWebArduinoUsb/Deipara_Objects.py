#!/usr/bin/python

import logging
import datetime

###################################################################################
########## Classes used to store datas    #########################################
###################################################################################


        
class Object:
    "Une classe generique qui decrit un capteur/actioneur"
    
    def __init__(self):
        self.id =0
        self.physicalLocation =""
        self.currentStatus =""
        self.LastTMeaureDate=datetime.datetime.now()
        self.type=""
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
        aRetString = aRetString + "self.LastTMeaureDate : " + str(self.LastTMeaureDate) + "\n"
        aRetString = aRetString + "self.currentStatus : " + str(self.currentStatus) + "\n"
        aRetString = aRetString + "self.description : " + str(self.description) + "\n"
        aRetString = aRetString + "self.Reset : " + str(self.Reset) + "\n"
        aRetString = aRetString + "self.InPossibleCmd : " + str(self.InPossibleCmd) + "\n"
        aRetString = aRetString + "self.OutPossibleCmd : " + str(self.OutPossibleCmd) + "\n"
        aRetString = aRetString + "self.ActionsCommands : " + str(self.ActionsCommands) + "\n"
        aRetString = aRetString + "self.PossibleStates : " + str(self.PossibleStates) + "\n"
        return aRetString
        
class CapteurMesure(Object):
    "Une classe qui decrit un capteur de mesure (temperature, lumiere, humidite, ...)"
    
    def __init__(self):
        Object.__init__(self)
        self.refreshRatemin = 60
        self.type="CapteurMesure"
        
    def refreshIfNeeded(self):
        if (datetime.datetime.now() - self.LastTMeaureDate > datetime.timedelta (minutes = self.refreshRatemin)):
            logging.debug("refresh needed")

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + Object.__repr__(self) + "\n"
        aRetString = aRetString + "self.refreshRatemin : " + str(self.refreshRatemin) + "\n"
        return aRetString
        
class InterupteurBiStable(Object):
    "Une classe qui decrit un capteur"
    
    def __init__(self):
        Object.__init__(self)
        self.type="InterupteurBiStable"

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + Object.__repr__(self) + "\n"
        return aRetString 

class InterupteurStable(Object):
    "Une classe qui decrit un capteur"
    
    def __init__(self):
        Object.__init__(self)
        self.stateForceByUser = False
        self.type="InterupteurStable"
        self.DateTimeStateForce = datetime.datetime.now()

    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + Object.__repr__(self) + "\n"
        aRetString = aRetString + "self.stateForceByUser : " + str(self.stateForceByUser) + "\n"
        aRetString = aRetString + "self.DateTimeStateForce : " + str(self.DateTimeStateForce) + "\n"
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
            
        charlesT = CapteurMesure()
        charlesT.OutPossibleCmd ={"15" : "recoit Nouvelle T"}
        charlesT.ActionsCommands ={"15" : """self.currentStatus=aData
self.LastTMeaureDate=datetime.datetime.now()"""}
        charlesT.id =15
        self.registeredDevices.append(charlesT)
        
        charlesH = CapteurMesure()
        charlesH.OutPossibleCmd ={"16" : "recoit Nouvelle H"}
        charlesH.ActionsCommands ={"16" : "self.currentStatus=aData"}
        charlesH.id =16
        self.registeredDevices.append(charlesH)
        
        entreeT = CapteurMesure()
        entreeT.OutPossibleCmd ={"30" : "recoit Nouvelle T"}
        entreeT.ActionsCommands ={"30" : "self.currentStatus=aData"}
        entreeT.id =17
        self.registeredDevices.append(entreeT)
        
        entreeH = CapteurMesure()
        entreeH.OutPossibleCmd ={"31" : "recoit Nouvelle H"}
        entreeH.ActionsCommands ={"31" : "self.currentStatus=aData"}
        entreeH.id =18
        self.registeredDevices.append(entreeH)
        
        Montre = CapteurMesure()
        Montre.OutPossibleCmd ={"37" : "recoit Nouvelle H"}
        Montre.ActionsCommands ={"37" : "self.currentStatus=aData"}
        Montre.id =2
        Montre.refreshRatemin = 1
        self.registeredDevices.append(Montre)
        
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
        
        VoletSalon = InterupteurBiStable()
        VoletSalon.PossibleStates=[ "on","off"]
        VoletSalon.id =5
        VoletSalon.InPossibleCmd ={ "9" : "on","10" : "off"}
        VoletSalon.ActionsCommands={ "9" : "self.currentStatus=\"on\"","10" : "self.currentStatus=\"off\""}
        self.registeredDevices.append(VoletSalon)
        
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
        Lumiereentree.id =8
        Lumiereentree.InPossibleCmd ={ "34" : "on","35" : "off"}
        Lumiereentree.ActionsCommands={ "34" : "self.currentStatus=\"on\"","35" : "self.currentStatus=\"off\""}
        self.registeredDevices.append(Lumiereentree)
        
        luminoTersa = CapteurMesure()
        luminoTersa.OutPossibleCmd ={"36" : "recoit Nouvelle L"}
        luminoTersa.ActionsCommands ={"36" : "self.currentStatus=aData"}
        luminoTersa.id =22
        self.registeredDevices.append(luminoTersa)
        
        DetecteurPresenceCharles = InterupteurStable()
        DetecteurPresenceCharles.PossibleStates=[ "unstable","stable"]
        DetecteurPresenceCharles.id =9
        DetecteurPresenceCharles.OutPossibleCmd ={ "2" : "unstable position"}
        DetecteurPresenceCharles.ActionsCommands={ "2" : "self.currentStatus=\"unstable\""}
        DetecteurPresenceCharles.Reset = "self.currentStatus=\"stable\""
        self.registeredDevices.append(DetecteurPresenceCharles)
        
        DetecteurPresenceEntree = InterupteurStable()
        DetecteurPresenceEntree.PossibleStates=[ "unstable","stable"]
        DetecteurPresenceEntree.id =10
        DetecteurPresenceEntree.OutPossibleCmd ={ "50" : "unstable position"}
        DetecteurPresenceEntree.ActionsCommands={ "50" : "self.currentStatus=\"unstable\""}
        DetecteurPresenceEntree.Reset = "self.currentStatus=\"stable\""
        self.registeredDevices.append(DetecteurPresenceEntree)
        
    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + "self.registeredDevices : " + str(self.registeredDevices) + "\n"
        return aRetString