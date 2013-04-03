#!/usr/bin/python

#my python modules
import Deipara_Brain
import Deipara_Objects

#twisted python modules
from twisted.internet import reactor 
from twisted.internet.protocol import Factory 
from twisted.internet.protocol import Protocol 
from twisted.internet.task import LoopingCall
from twisted.protocols.basic import LineReceiver 
from twisted.internet.serialport import SerialPort 
from twisted.python import log

#other modules
import sys
import logging
import datetime

class UsbHandler(LineReceiver):
    """protocol handling class for USB """

    def __init__(self,iBrain,iRegisteredDevice):
        self.brain = iBrain
        self.registeredDevices = iRegisteredDevice
        
    def lineReceived(self, line):
        logging.info("USB Handler created to process : " + str(line))
        self.brain.HandleUsbInput(line,self.registeredDevices)
            
class TcpHandlerFactory(Factory):
    """my factory class. The buildProtocol method of the Factory is used to create a Protocol for each new connection"""
    
    def __init__(self,iBrain,iRegisteredDevice):
        self.brain = iBrain
        self.registeredDevices = iRegisteredDevice
        
    def buildProtocol(self, addr):
        logging.info("We received something for TCP protocol")
        return TcpHandler(self.brain,self.registeredDevices)
        
class TcpHandler(Protocol):
    """protocol handling class for TCP """
    
    def __init__(self,iBrain,iRegisteredDevice):
        self.brain = iBrain
        self.registeredDevices = iRegisteredDevice
    
    def dataReceived(self, data):
        logging.info("Tcp Handler created to process : " + str(data))
        if "READ" in str(data):
            logging.info("READ command")
            aRest = aBrain.ReadDeviceStatus(data,aRegisterDevices)
            logging.info("READ command res " + str(aRest))
            self.transport.write(str(aRest))
        else:
            logging.info("Write command")
            aBrain.SendMessage(data,aRegisterDevices)
            self.transport.write("ACK")
        
def tired_task(iBrain):
    #logging.info("I want to run slowly" + str (datetime.datetime.now()))
    iBrain.smartProcessing2(aRegisterDevices)
    
#The loading API 
logging.basicConfig(filename='PythonWrapperWebArduinoUsbD.log',level=logging.INFO)
logging.info('Daemon starting...')

#The brain
aBrain = Deipara_Brain.Brain()
#Object that handle all devices present on the networl
aRegisterDevices =Deipara_Objects.DevicesHandler()
aRegisterDevices.loadDevices()

reactor.listenTCP(50007, TcpHandlerFactory(aBrain,aRegisterDevices))
SerialPort(UsbHandler(aBrain,aRegisterDevices), '/dev/ttyACM0', reactor, 9600)

lc2 = LoopingCall(tired_task, aBrain)
lc2.start(1)

reactor.run()
