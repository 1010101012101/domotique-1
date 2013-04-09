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
        self.porteuse = "GATEWAY"
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
        self.DateTimeStateForce = datetime.datetime.now()

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
        charlesT.OutActionsCommands ={"15" : """self.currentStatus=aData
self.LastTMeaureDate=datetime.datetime.now()
self.refreshOngoing = False"""}
        charlesT.InActionsCommands ={"15" : """fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 15 to USB port and sending back to sender")
fd.write(chr(15))"""}
        charlesT.id =15
        charlesT.refreshRatemin = 3
        self.registeredDevices.append(charlesT)
        
        charlesH = CapteurMesure()
        charlesH.OutPossibleCmd ={"16" : "recoit Nouvelle H"}
        charlesH.InPossibleCmd ={"16" : "recoit Nouvelle H"}
        charlesH.InActionsCommands ={"16" : """fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 16 to USB port and sending back to sender")
fd.write(chr(16))"""}
        charlesH.OutActionsCommands ={"16" : """self.currentStatus=aData
self.LastTMeaureDate=datetime.datetime.now()
self.refreshOngoing = False"""}
        charlesH.id =16
        charlesH.refreshRatemin = 4
        self.registeredDevices.append(charlesH)
        
        entreeT = CapteurMesure()
        entreeT.OutPossibleCmd ={"30" : "recoit Nouvelle T"}
        entreeT.InPossibleCmd ={"30" : "recoit Nouvelle T"}
        entreeT.InActionsCommands ={"30" : """fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting 30 to USB port and sending back to sender")
fd.write(chr(30))"""}
        entreeT.OutActionsCommands ={"30" : """self.currentStatus=aData
self.LastTMeaureDate=datetime.datetime.now()
self.refreshOngoing = False"""}
        entreeT.id =17
        entreeT.refreshRatemin = 5
        self.registeredDevices.append(entreeT)
        
        CuisineT = CapteurMesure()
        CuisineT.OutPossibleCmd ={"39" : "recoit Nouvelle T"}
        CuisineT.InPossibleCmd ={"39" : "recoit Nouvelle T"}
        CuisineT.InActionsCommands ={"39" : """fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(39))"""}
        CuisineT.OutActionsCommands ={"39" : """self.currentStatus=aData
self.LastTMeaureDate=datetime.datetime.now()
self.refreshOngoing = False"""}
        CuisineT.id =21
        self.registeredDevices.append(CuisineT)
        
        CuisineH = CapteurMesure()
        CuisineH.OutPossibleCmd ={"40" : "recoit Nouvelle T"}
        CuisineH.InPossibleCmd ={"40" : "recoit Nouvelle T"}
        CuisineH.InActionsCommands ={"40" : """fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(40))"""}
        CuisineH.OutActionsCommands ={"40" : """self.currentStatus=aData
self.LastTMeaureDate=datetime.datetime.now()
self.refreshOngoing = False"""}
        CuisineH.id =23
        self.registeredDevices.append(CuisineH)
        
        entreeH = CapteurMesure()
        entreeH.OutPossibleCmd ={"31" : "recoit Nouvelle H"}
        entreeH.InPossibleCmd ={"31" : "recoit Nouvelle H"}
        entreeH.InActionsCommands ={"31" : """fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(31))"""}
        entreeH.OutActionsCommands ={"31" : """self.currentStatus=aData
self.LastTMeaureDate=datetime.datetime.now()
self.refreshOngoing = False"""}
        entreeH.id =18
        entreeH.refreshRatemin = 6
        self.registeredDevices.append(entreeH)
        
        lumiereCharles = InterupteurBiStable()
        lumiereCharles.PossibleStates=[ "off","on"]
        lumiereCharles.id =1
        lumiereCharles.InPossibleCmd ={ "5" : "on","6" : "off"}
        lumiereCharles.InActionsCommands={ "5" : """self.currentStatus=\"on\"
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(5))""","6" : """self.currentStatus=\"off\"
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(6))"""}
        self.registeredDevices.append(lumiereCharles)
        
        PcCharles = InterupteurBiStable()
        PcCharles.PossibleStates=[ "on","off"]
        PcCharles.id =19
        PcCharles.porteuse = "PYTHON"
        PcCharles.stateCanBeRefresh = True
        PcCharles.InPossibleCmd ={ "60" : "on" , "61" : "verify state by pooling", "62" : "off"}
        PcCharles.InActionsCommands={ "60" : """self.currentStatus=\"on\"
sudo /usr/sbin/etherwake 20:cf:30:ca:8a:50""", "61" : """if os.system('ping -c 1 -W 2 192.168.0.7'):
    self.currentStatus="on"
else:
    self.currentStatus="off" """, "62" : "net rpc shutdown -f -I 192.168.0.7 -U charles%"+Config["WinPasswdRpcShutdown"]"}
        #self.registeredDevices.append(PcCharles)
        
        lumiere2Charles = InterupteurBiStable()
        lumiere2Charles.PossibleStates=[ "off","on"]
        lumiere2Charles.id =3
        lumiere2Charles.InPossibleCmd ={ "11" : "on","12" : "off"}
        lumiere2Charles.InActionsCommands={ "11" : """self.currentStatus=\"on\"
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(11))""","12" : """self.currentStatus=\"off\"
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(12))"""}
        self.registeredDevices.append(lumiere2Charles)
        
        VoletCharles = InterupteurBiStable()
        VoletCharles.PossibleStates=[ "off","on"]
        VoletCharles.id =4
        VoletCharles.InPossibleCmd ={ "7" : "off","8" : "on"}
        VoletCharles.InActionsCommands={ "7" : """self.currentStatus=\"off\"
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(7))""","8" : """self.currentStatus=\"on\"
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(8))"""}
        self.registeredDevices.append(VoletCharles)
        
        VoletSalon = InterupteurBiStable()
        VoletSalon.PossibleStates=[ "off","on"]
        VoletSalon.id =5
        VoletSalon.InPossibleCmd ={ "9" : "off","10" : "on"}
        VoletSalon.InActionsCommands={ "9" : """self.currentStatus=\"off\"
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(9))""","10" : """self.currentStatus=\"on\"
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(10))"""}
        self.registeredDevices.append(VoletSalon)
        
        LumiereSalonHalogene = InterupteurBiStable()
        LumiereSalonHalogene.PossibleStates=[ "off","on"]
        LumiereSalonHalogene.id =6
        LumiereSalonHalogene.InPossibleCmd ={ "13" : "off","14" : "on"}
        LumiereSalonHalogene.InActionsCommands={ "13" : """self.currentStatus=\"off\"
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(13))""","14" : """self.currentStatus=\"on\"
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(14))"""}
        self.registeredDevices.append(LumiereSalonHalogene)
        
        ChaffageSdb = InterupteurBiStable()
        ChaffageSdb.PossibleStates=[ "off","on"]
        ChaffageSdb.id =7
        ChaffageSdb.InPossibleCmd ={ "42" : "off","43" : "on"}
        ChaffageSdb.InActionsCommands={ "42" : """self.currentStatus=\"off\"
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(42))""","43" : """self.currentStatus=\"on\"
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(43))"""}
        self.registeredDevices.append(ChaffageSdb)
        
        Lumiereentree = InterupteurBiStable()
        Lumiereentree.PossibleStates=[ "off","on"]
        Lumiereentree.id =8
        Lumiereentree.InPossibleCmd ={ "34" : "on","35" : "off"}
        Lumiereentree.InActionsCommands={ "34" : """self.currentStatus=\"on\"
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(34))""","35" : """self.currentStatus=\"off\"
fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(35))"""}
        self.registeredDevices.append(Lumiereentree)
        
        luminoTersa = CapteurMesure()
        luminoTersa.OutPossibleCmd ={"36" : "recoit Nouvelle L"}
        luminoTersa.InPossibleCmd ={"36" : "recoit Nouvelle L"}
        luminoTersa.InActionsCommands ={"36" : """fd = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
logging.info ("Writting input to USB port and sending back to sender")
fd.write(chr(36))"""}
        luminoTersa.OutActionsCommands ={"36" : "self.currentStatus=aData"}
        luminoTersa.id =22
        self.registeredDevices.append(luminoTersa)
        
        DetecteurPresenceCharles = InterupteurStable()
        DetecteurPresenceCharles.PossibleStates=[ "unstable","stable"]
        DetecteurPresenceCharles.id =9
        DetecteurPresenceCharles.OutPossibleCmd ={ "2" : "unstable position"}
        DetecteurPresenceCharles.OutActionsCommands={ "2" : """self.currentStatus=\"unstable\"
self.LastTMeaureDate=datetime.datetime.now()"""}
        DetecteurPresenceCharles.Reset = "self.currentStatus=\"stable\""
        self.registeredDevices.append(DetecteurPresenceCharles)
        
        DetecteurPresenceEntree = InterupteurStable()
        DetecteurPresenceEntree.PossibleStates=[ "unstable","stable"]
        DetecteurPresenceEntree.id =10
        DetecteurPresenceEntree.OutPossibleCmd ={ "50" : "unstable position"}
        DetecteurPresenceEntree.OutActionsCommands={ "50" : """self.currentStatus=\"unstable\"
self.LastTMeaureDate=datetime.datetime.now()"""}
        DetecteurPresenceEntree.Reset = "self.currentStatus=\"stable\""
        self.registeredDevices.append(DetecteurPresenceEntree)
        
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