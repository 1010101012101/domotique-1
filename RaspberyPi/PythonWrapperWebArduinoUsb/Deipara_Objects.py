#!/usr/bin/python

import logging
import datetime
import os
import serial

class Function:
    '''Une classe generique qui decrit une fonctionalite (temperature, lampe, volet, ...)''' 
    
    def __init__(self):
        self.id =0
        self.type=""
        
        self.physicalLocation =""
        self.currentStatus =""
        self.LastTMeaureDate=datetime.datetime.now()
        self.LastRefreshDate=datetime.datetime.now()
        self.refreshRatemin = 60
        self.description =""
        self.stateCanBeRefresh = False
        self.refreshOngoing = False
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
        self.refreshOngoing = False
        
    def RequestNewValue(self):
        self.refreshOngoing = True
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
        self.refreshOngoing = True
        logging.info ("Using "+ str(self.OutPossibleCmd.keys()[0]) + " to refresh")
        exec(self.OutActionsCommands[str(self.OutPossibleCmd.keys()[0])])
        
    def turnOn(self,iDataToSend):
        self.currentStatus="on"
        fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
        logging.info ("Writting "+ str(iDataToSend) + " to USB port and sending back to sender")
        fd.write(chr(iDataToSend))
        
    def turnOff(self,iDataToSend):
        self.currentStatus="off"
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
        charlesT.InPossibleCmd ={"15" : "recoit Nouvelle T"}
        charlesT.OutActionsCommands ={"15" : "self.UpdateValue(aData)"}
        charlesT.InActionsCommands ={"15" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 15 to USB port and sending back to sender")
fd.write(chr(15))"""}
        charlesT.id =15
        charlesT.refreshRatemin = 3
        self.registeredDevices.append(charlesT)
        
        charlesH = CapteurMesure()
        charlesH.OutPossibleCmd ={"16" : "recoit Nouvelle H"}
        charlesH.InPossibleCmd ={"16" : "recoit Nouvelle H"}
        charlesH.InActionsCommands ={"16" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 16 to USB port and sending back to sender")
fd.write(chr(16))"""}
        charlesH.OutActionsCommands ={"16" : "self.UpdateValue(aData)"}
        charlesH.id =16
        charlesH.refreshRatemin = 4
        self.registeredDevices.append(charlesH)
        
        entreeT = CapteurMesure()
        entreeT.OutPossibleCmd ={"30" : "recoit Nouvelle T"}
        entreeT.InPossibleCmd ={"30" : "recoit Nouvelle T"}
        entreeT.InActionsCommands ={"30" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 30 to USB port and sending back to sender")
fd.write(chr(30))"""}
        entreeT.OutActionsCommands ={"30" : "self.UpdateValue(aData)"}
        entreeT.id =17
        entreeT.refreshRatemin = 5
        self.registeredDevices.append(entreeT)
        
        CuisineT = CapteurMesure()
        CuisineT.OutPossibleCmd ={"39" : "recoit Nouvelle T"}
        CuisineT.InPossibleCmd ={"39" : "recoit Nouvelle T"}
        CuisineT.InActionsCommands ={"39" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 39 to USB port and sending back to sender")
fd.write(chr(39))"""}
        CuisineT.OutActionsCommands ={"39" : "self.UpdateValue(aData)"}
        CuisineT.id =21
        CuisineT.refreshRatemin = 9
        self.registeredDevices.append(CuisineT)
        
        CuisineH = CapteurMesure()
        CuisineH.OutPossibleCmd ={"40" : "recoit Nouvelle T"}
        CuisineH.refreshRatemin = 7
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
        entreeH.InPossibleCmd ={"31" : "recoit Nouvelle H"}
        entreeH.InActionsCommands ={"31" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 31 to USB port and sending back to sender")
fd.write(chr(31))"""}
        entreeH.OutActionsCommands ={"31" : "self.UpdateValue(aData)"}
        entreeH.id =18
        entreeH.refreshRatemin = 6
        self.registeredDevices.append(entreeH)
        
        lumiereCharles = InterupteurBiStable()
        lumiereCharles.id =1
        lumiereCharles.InPossibleCmd ={ "5" : "on","6" : "off"}
        lumiereCharles.InActionsCommands={ "5" : "self.turnOn(5)","6" : "self.turnOff(6)"}
        self.registeredDevices.append(lumiereCharles)
        
        PcCharles = InterupteurBiStable()
        PcCharles.id =19
        PcCharles.stateCanBeRefresh = True
        PcCharles.OutPossibleCmd ={"61" : "checkStatus"}
        PcCharles.InPossibleCmd ={ "60" : "on", "62" : "off"}
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
        PcCharles.refreshRatemin = 1
        self.registeredDevices.append(PcCharles)
        
        lumiere2Charles = InterupteurBiStable()
        lumiere2Charles.id =3
        lumiere2Charles.InPossibleCmd ={ "11" : "on","12" : "off"}
        lumiere2Charles.InActionsCommands={ "11" : "self.turnOn(11)","12" : "self.turnOff(12)"}
        self.registeredDevices.append(lumiere2Charles)
        
        VoletCharles = InterupteurBiStable()
        VoletCharles.id =4
        VoletCharles.InPossibleCmd ={ "7" : "off","8" : "on"}
        VoletCharles.InActionsCommands={ "7" : "self.turnOff(7)","8" : "self.turnOn(8)"}
        self.registeredDevices.append(VoletCharles)
        
        VoletSalon = InterupteurBiStable()
        VoletSalon.id =5
        VoletSalon.InPossibleCmd ={ "9" : "off","10" : "on"}
        VoletSalon.InActionsCommands={ "9" : "self.turnOff(9)","10" : "self.turnOn(10)"}
        self.registeredDevices.append(VoletSalon)
        
        LumiereSalonHalogene = InterupteurBiStable()
        LumiereSalonHalogene.id =6
        LumiereSalonHalogene.InPossibleCmd ={ "13" : "off","14" : "on"}
        LumiereSalonHalogene.InActionsCommands={ "13" : "self.turnOff(13)","14" : "self.turnOn(14)"}
        self.registeredDevices.append(LumiereSalonHalogene)
        
        ChaffageSdb = InterupteurBiStable()
        ChaffageSdb.id =7
        ChaffageSdb.InPossibleCmd ={ "42" : "off","43" : "on"}
        ChaffageSdb.InActionsCommands={ "42" : "self.turnOff(42)","43" : "self.turnOn(43)"}
        self.registeredDevices.append(ChaffageSdb)
        
        Lumiereentree = InterupteurBiStable()
        Lumiereentree.id =8
        Lumiereentree.InPossibleCmd ={ "34" : "on","35" : "off"}
        Lumiereentree.InActionsCommands={ "34" : "self.turnOn(34)","35" : "self.turnOff(35)"}
        self.registeredDevices.append(Lumiereentree)
        
        luminoTersa = CapteurMesure()
        luminoTersa.OutPossibleCmd ={"36" : "recoit Nouvelle L"}
        luminoTersa.InPossibleCmd ={"36" : "recoit Nouvelle L"}
        luminoTersa.InActionsCommands ={"36" : """logging.warn("Refreshing capteur : " + str(self.id))
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 31 to USB port and sending back to sender")
fd.write(chr(36))"""}
        luminoTersa.OutActionsCommands ={"36" : "self.UpdateValue(aData)"}
        luminoTersa.id =22
        self.registeredDevices.append(luminoTersa)
        
        DetecteurPresenceCharles = InterupteurStable()
        DetecteurPresenceCharles.id =9
        DetecteurPresenceCharles.OutPossibleCmd ={ "2" : "unstable position"}
        DetecteurPresenceCharles.OutActionsCommands={ "2" : "self.detectionEventReceived()"}
        DetecteurPresenceCharles.Reset = "self.currentStatus=\"stable\""
        self.registeredDevices.append(DetecteurPresenceCharles)
        
        DetecteurPresenceEntree = InterupteurStable()
        DetecteurPresenceEntree.id =10
        DetecteurPresenceEntree.OutPossibleCmd ={ "50" : "unstable position"}
        DetecteurPresenceEntree.OutActionsCommands={ "50" : "self.detectionEventReceived()"}
        DetecteurPresenceEntree.Reset = "self.currentStatus=\"stable\""
        self.registeredDevices.append(DetecteurPresenceEntree)
        
        DetecteurPresenceCuisine = InterupteurStable()
        DetecteurPresenceCuisine.id =27
        DetecteurPresenceCuisine.OutPossibleCmd ={ "51" : "unstable position"}
        DetecteurPresenceCuisine.OutActionsCommands={ "51" : "self.detectionEventReceived()"}
        DetecteurPresenceCuisine.Reset = "self.currentStatus=\"stable\""
        self.registeredDevices.append(DetecteurPresenceCuisine)
        
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