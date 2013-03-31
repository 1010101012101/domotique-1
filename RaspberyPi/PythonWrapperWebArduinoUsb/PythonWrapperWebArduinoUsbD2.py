#!/usr/bin/python

import sys
import Deipara2
import logging
import datetime


from twisted.internet import reactor 
from twisted.internet.protocol import Factory 
from twisted.internet.protocol import Protocol 

from twisted.protocols.basic import LineReceiver 
from twisted.internet.serialport import SerialPort 
from twisted.python import log

from twisted.internet.task import LoopingCall
from twisted.internet import reactor

def hyper_task():
    print ("I like to run fast" + str(datetime.datetime.now()))

def tired_task(iBrain):
    print ("I want to run slowly" + str (datetime.datetime.now()))
    iBrain.smartProcessing2(aRegisterDevices)

class UsbHandler(LineReceiver):
    """protocol handling class for USB """

    def __init__(self,iBrain,iRegisteredDevice):
        self.brain = iBrain
        self.registeredDevices = iRegisteredDevice
    
    #def connectionFailed(self):
        #print "Connection Failed:", self
        #reactor.stop()
        
    def lineReceived(self, line):
        print("USB Handler created to process : " + str(line))
        self.brain.HandleUsbInput(line,self.registeredDevices)
    
    #def connectionMade(self):
        #self.usb_list.append(self)
        #print 'Connected to USB modem'
        #USBClient.sendLine(self, 'AT\r\n')
    
    #def dataReceived(self, data):
        #print("USB Handler created to process : " + str(data))
        #self.brain.HandleUsbInput(data,self.registeredDevices)
    
        #for cli in client_list:
            #cli.transport.write(data)
        #self.network.notifyAll(data)# !!AArgh..!Could not get this to work
        #pass
    
    #def sendLine(self, cmd):
        #print cmd
        #self.transport.write(cmd + "\r\n")
    
    #def outReceived(self, data):
        #print "outReceived! with %d bytes!" % len(data)
        #self.data = self.data + data



            
class TcpHandlerFactory(Factory):
    """my factory class. The buildProtocol method of the Factory is used to create a Protocol for each new connection"""
    
    def __init__(self,iBrain,iRegisteredDevice):
        self.brain = iBrain
        self.registeredDevices = iRegisteredDevice
        
    def buildProtocol(self, addr):
        print("We received something for TCP protocol")
        return TcpHandler(self.brain,self.registeredDevices)
        
class TcpHandler(Protocol):
    """protocol handling class for TCP """
    
    def __init__(self,iBrain,iRegisteredDevice):
        self.brain = iBrain
        self.registeredDevices = iRegisteredDevice
    
    def dataReceived(self, data):
        print("Tcp Handler created to process : " + str(data))
        aBrain.SendMessage(data,aRegisterDevices)
        

#The loading API 
logging.basicConfig(filename='PythonWrapperWebArduinoUsbD.log',level=logging.INFO)
logging.info('Daemon starting...')

#The brain
aBrain = Deipara2.Brain()
#Object that handle all devices present on the networl
aRegisterDevices =Deipara2.DevicesHandler()
aRegisterDevices.loadDevices()

reactor.listenTCP(50007, TcpHandlerFactory(aBrain,aRegisterDevices))
SerialPort(UsbHandler(aBrain,aRegisterDevices), '/dev/ttyACM0', reactor, 9600)

#lc = LoopingCall(hyper_task)
#lc.start(0.1)

lc2 = LoopingCall(tired_task, aBrain)
lc2.start(10)

reactor.run()
