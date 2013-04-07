#!/usr/bin/python

import logging
import datetime
import os


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
        self.LastRefreshDate=datetime.datetime.now()
        self.type=""
        self.refreshRatemin = 60
        self.description =""
        self.porteuse = "GATEWAY"
        self.stateCanBeRefresh = False
        self.refreshOngoing = False
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
        self.type="CapteurMesure"
        self.stateCanBeRefresh = True

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
        aRetString = aRetString + Object.__repr__(self)
        aRetString = aRetString + "self.stateForceByUser : " + str(self.stateForceByUser) + "\n"
        aRetString = aRetString + "self.DateTimeStateForce : " + str(self.DateTimeStateForce) + "\n"
        return aRetString 
        
class DevicesHandler:
    "Gere un ensemble de devices"
    
    def __init__(self):
        self.registeredDevices =[]
        
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
        charlesT.InPossibleCmd ={"15" : "recoit Nouvelle T"}
        charlesT.ActionsCommands ={"15" : """self.currentStatus=aData
self.LastTMeaureDate=datetime.datetime.now()
self.refreshOngoing = False"""}
        charlesT.id =15
        self.registeredDevices.append(charlesT)
        
        charlesH = CapteurMesure()
        charlesH.OutPossibleCmd ={"16" : "recoit Nouvelle H"}
        charlesH.InPossibleCmd ={"16" : "recoit Nouvelle H"}
        charlesH.ActionsCommands ={"16" : """self.currentStatus=aData
self.LastTMeaureDate=datetime.datetime.now()
self.refreshOngoing = False"""}
        charlesH.id =16
        self.registeredDevices.append(charlesH)
        
        entreeT = CapteurMesure()
        entreeT.OutPossibleCmd ={"30" : "recoit Nouvelle T"}
        entreeT.InPossibleCmd ={"30" : "recoit Nouvelle T"}
        entreeT.ActionsCommands ={"30" : """self.currentStatus=aData
self.LastTMeaureDate=datetime.datetime.now()
self.refreshOngoing = False"""}
        entreeT.id =17
        self.registeredDevices.append(entreeT)
        
        CuisineT = CapteurMesure()
        CuisineT.OutPossibleCmd ={"39" : "recoit Nouvelle T"}
        CuisineT.InPossibleCmd ={"39" : "recoit Nouvelle T"}
        CuisineT.ActionsCommands ={"39" : """self.currentStatus=aData
self.LastTMeaureDate=datetime.datetime.now()
self.refreshOngoing = False"""}
        CuisineT.id =21
        self.registeredDevices.append(CuisineT)
        
        CuisineH = CapteurMesure()
        CuisineH.OutPossibleCmd ={"40" : "recoit Nouvelle T"}
        CuisineH.InPossibleCmd ={"40" : "recoit Nouvelle T"}
        CuisineH.ActionsCommands ={"40" : """self.currentStatus=aData
self.LastTMeaureDate=datetime.datetime.now()
self.refreshOngoing = False"""}
        CuisineH.id =23
        self.registeredDevices.append(CuisineH)
        
        entreeH = CapteurMesure()
        entreeH.OutPossibleCmd ={"31" : "recoit Nouvelle H"}
        entreeH.InPossibleCmd ={"31" : "recoit Nouvelle H"}
        entreeH.ActionsCommands ={"31" : """self.currentStatus=aData
self.LastTMeaureDate=datetime.datetime.now()
self.refreshOngoing = False"""}
        entreeH.id =18
        self.registeredDevices.append(entreeH)
        
        Montre = CapteurMesure()
        Montre.OutPossibleCmd ={"37" : "recoit Nouvelle H"}
        Montre.InPossibleCmd ={"37" : "recoit Nouvelle H"}
        Montre.ActionsCommands ={"37" : """self.currentStatus=aData
self.refreshOngoing = False
self.LastTMeaureDate=datetime.datetime.now()"""}
        Montre.id =2
        Montre.refreshRatemin = 60
        self.registeredDevices.append(Montre)
        
        lumiereCharles = InterupteurBiStable()
        lumiereCharles.PossibleStates=[ "unstable","stable"]
        lumiereCharles.id =1
        lumiereCharles.InPossibleCmd ={ "5" : "unstable","6" : "stable"}
        lumiereCharles.ActionsCommands={ "5" : "self.currentStatus=\"unstable\"","6" : "self.currentStatus=\"stable\""}
        self.registeredDevices.append(lumiereCharles)
        
        PcCharles = InterupteurBiStable()
        PcCharles.PossibleStates=[ "unstable","off"]
        PcCharles.id =19
        PcCharles.porteuse = "PYTHON"
        PcCharles.stateCanBeRefresh = True
        PcCharles.InPossibleCmd ={ "5" : "unstable" , "6" : "verify state by pooling"}
        PcCharles.ActionsCommands={ "5" : "self.currentStatus=\"unstable\"", "6" : """if os.system('ping -c 1 -W 2 192.168.0.7'):
    self.currentStatus="on"
else:
    self.currentStatus="off" """}
        #self.registeredDevices.append(PcCharles)
        
        lumiere2Charles = InterupteurBiStable()
        lumiere2Charles.PossibleStates=[ "unstable","stable"]
        lumiere2Charles.id =3
        lumiere2Charles.InPossibleCmd ={ "11" : "unstable","12" : "stable"}
        lumiere2Charles.ActionsCommands={ "11" : "self.currentStatus=\"unstable\"","12" : "self.currentStatus=\"stable\""}
        self.registeredDevices.append(lumiere2Charles)
        
        VoletCharles = InterupteurBiStable()
        VoletCharles.PossibleStates=[ "unstable","stable"]
        VoletCharles.id =4
        VoletCharles.InPossibleCmd ={ "7" : "unstable","8" : "stable"}
        VoletCharles.ActionsCommands={ "7" : "self.currentStatus=\"unstable\"","8" : "self.currentStatus=\"stable\""}
        self.registeredDevices.append(VoletCharles)
        
        VoletSalon = InterupteurBiStable()
        VoletSalon.PossibleStates=[ "unstable","stable"]
        VoletSalon.id =5
        VoletSalon.InPossibleCmd ={ "9" : "unstable","10" : "stable"}
        VoletSalon.ActionsCommands={ "9" : "self.currentStatus=\"unstable\"","10" : "self.currentStatus=\"stable\""}
        self.registeredDevices.append(VoletSalon)
        
        LumiereSalonHalogene = InterupteurBiStable()
        LumiereSalonHalogene.PossibleStates=[ "unstable","stable"]
        LumiereSalonHalogene.id =6
        LumiereSalonHalogene.InPossibleCmd ={ "13" : "unstable","14" : "stable"}
        LumiereSalonHalogene.ActionsCommands={ "13" : "self.currentStatus=\"unstable\"","14" : "self.currentStatus=\"stable\""}
        self.registeredDevices.append(LumiereSalonHalogene)
        
        ChaffageSdb = InterupteurBiStable()
        ChaffageSdb.PossibleStates=[ "unstable","stable"]
        ChaffageSdb.id =7
        ChaffageSdb.InPossibleCmd ={ "42" : "unstable","43" : "stable"}
        ChaffageSdb.ActionsCommands={ "42" : "self.currentStatus=\"unstable\"","43" : "self.currentStatus=\"stable\""}
        self.registeredDevices.append(ChaffageSdb)
        
        Lumiereentree = InterupteurBiStable()
        Lumiereentree.PossibleStates=[ "unstable","stable"]
        Lumiereentree.id =8
        Lumiereentree.InPossibleCmd ={ "34" : "unstable","35" : "stable"}
        Lumiereentree.ActionsCommands={ "34" : "self.currentStatus=\"unstable\"","35" : "self.currentStatus=\"stable\""}
        self.registeredDevices.append(Lumiereentree)
        
        luminoTersa = CapteurMesure()
        luminoTersa.OutPossibleCmd ={"36" : "recoit Nouvelle L"}
        luminoTersa.InPossibleCmd ={"36" : "recoit Nouvelle L"}
        luminoTersa.ActionsCommands ={"36" : "self.currentStatus=aData"}
        luminoTersa.id =22
        self.registeredDevices.append(luminoTersa)
        
        DetecteurPresenceCharles = InterupteurStable()
        DetecteurPresenceCharles.PossibleStates=[ "unstable","stable"]
        DetecteurPresenceCharles.id =9
        DetecteurPresenceCharles.OutPossibleCmd ={ "2" : "unstable position"}
        DetecteurPresenceCharles.ActionsCommands={ "2" : """self.currentStatus=\"unstable\"
self.LastTMeaureDate=datetime.datetime.now()"""}
        DetecteurPresenceCharles.Reset = "self.currentStatus=\"stable\""
        self.registeredDevices.append(DetecteurPresenceCharles)
        
        DetecteurPresenceEntree = InterupteurStable()
        DetecteurPresenceEntree.PossibleStates=[ "unstable","stable"]
        DetecteurPresenceEntree.id =10
        DetecteurPresenceEntree.OutPossibleCmd ={ "50" : "unstable position"}
        DetecteurPresenceEntree.ActionsCommands={ "50" : """self.currentStatus=\"unstable\"
self.LastTMeaureDate=datetime.datetime.now()"""}
        DetecteurPresenceEntree.Reset = "self.currentStatus=\"stable\""
        self.registeredDevices.append(DetecteurPresenceEntree)
        
    def __repr__(self):
        aRetString = ""
        aRetString = aRetString + "self.registeredDevices : " + str(self.registeredDevices) + "\n"
        return aRetString