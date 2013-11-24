#!/usr/bin/python
# -*- coding: utf-8 -*-

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
from twisted.web import xmlrpc, server, twcgi, resource, static
from twisted.python import log
from twisted.web.twcgi import FilteredScript

#other modules
import sys
import logging
import json
import datetime

class Example(xmlrpc.XMLRPC):
    """
    An example object to be published.
    """

    def __init__(self,iBrain,iRegisteredDevice):
        self.brain = iBrain
        self.registeredDevices = iRegisteredDevice

    def xmlrpc_sendCommand(self, aCommandToExecute, aOriginator):
        """
        Return all passed args.
        """
        logging.info("Write command")
        aBrain.SendMessage(aCommandToExecute,aOriginator,aRegisterDevices)
        self.brain.smartProcessing2(self.registeredDevices)
        return "ACK"

    def xmlrpc_readDeviceStatus(self, aDeviceId):
        logging.info("READ command")
        aRest = aBrain.ReadDeviceStatus2(aDeviceId,aRegisterDevices)
        logging.info("READ command res " + str(aRest))
        return str(aRest)
        
    def xmlrpc_translateVocalAction(self, aSpeach):
        logging.warning("SPEAK command for " + aSpeach)
        (aRest,aCommandId) = aBrain.TranslateVocalAction(aSpeach,aRegisterDevices)
        return ("Matching Device Description : "+aRest+" and matching command : "+str(aCommandId))

    def xmlrpc_fault(self):
        """
        Raise a Fault indicating that the procedure should not be used.
        """
        raise xmlrpc.Fault(123, "The fault procedure is faulty.")

class PhpScript(twcgi.FilteredScript):
    """
    Twisted wrapping class to execute PHP code.
    """
    filter = '/usr/bin/php-cgi' # Points to the perl parser

    def runProcess(self, env, request, qargs=[]):
        env['REDIRECT_STATUS'] = ''
        return FilteredScript.runProcess(self, env, request, qargs)

class FormPage(resource.Resource):
    """
    Handle JSON call from website.
    """
    isLeaf = True
    allowedMethods = ('GET', 'POST')
  
    def __init__(self,iDevices):
        resource.Resource.__init__(self)
        self.aDevice=iDevices
    
    def render_GET(self, request):
        return self.render_POST(request)
        
    def render_POST(self, request):
        logging.debug("Rendering a web page with requests args : " + str(request.args))
        if( (request.args["action"])[0] == '3'):
            self.aDevice.startAutoDeploy()
            self.aDevice.AutoDeployStarted=True
        elif( (request.args["action"])[0] == '4'):
            aRes = jsonpickle.encode(self.aDevice)
            return aRes
        elif( (request.args["action"])[0] == 'u4'):
            aRes = jsonpickle.encode(self.aDevice.uid)
            return aRes
        elif( (request.args["action"])[0] == '6'):
            aRes = self.aDevice.getDevicepick("NGI_BOX_NGI")
            return aRes
        elif( (request.args["action"])[0] == '19'):
            self.aDevice.AdminEmail=(request.args["iRboxAdminEmail"])[0]
            self.aDevice.rGridIp=(request.args["iRgridIp"])[0]
            self.aDevice.loadTemplate((request.args["iTemplate"])[0])
            return "OK"
        elif( (request.args["action"])[0] == 'register_agent'):
            aIp=(request.args["ip"])[0]
            logging.info("I receive a new Rbox registration request from IP : " + str(aIp) )
            aRboxName = self.aDevice.addNewRbox(str(aIp))
            logging.info("Rbox registered with name : " + str(aRboxName) )
            return jsonpickle.encode(aRboxName)
        elif( (request.args["action"])[0] == 'ack_synch'):
            aIp=(request.args["ip"])[0]
            logging.info("I receive a new Rbox registration request from IP : " + str(aIp) )
            aRboxName = self.aDevice.ackSynch(str(aIp))
            return "OK"
        elif( (request.args["action"])[0] == 'register'):
            aIp=str((request.args["admip"])[0])
            aUid=str((request.args["uid"])[0])
            aCbIp=str((request.args["cbip"])[0])
            logging.info("I receive a new Rbox registration request from IP : " + str(aIp) )
            self.aDevice.handleChildRboxRegistration(aIp,aUid,aCbIp)
            return "OK"
        elif( (request.args["action"])[0] == 'ack_instal'):
            aIp=(request.args["ip"])[0]
            logging.info("I receive a new Rbox registration request from IP : " + str(aIp) )
            aRboxName = self.aDevice.ackInstal(str(aIp))
            return "OK"
        elif( (request.args["action"])[0] == 'ping_rt'):
            aFromIp=(request.args["ip_from"])[0]
            aToIp=(request.args["ip_to"])[0]
            aValue=(request.args["value"])[0]
            logging.info("I receive a new pingRt info aFromIp : " + str(aFromIp) +" aToIp:" + str(aToIp) + " aValue:" + str(aValue)   )
            aRboxName = self.aDevice.ackInstal(str(aIp))
            return "OK"
        elif( (request.args["action"])[0] == '17'):
            logging.info('clone' + (request.args["iId"])[0] + '_' + (request.args["iDetails"])[0])
            self.aDevice.CloneDevice((request.args["iDetails"])[0])
            return 'OK'
        elif( (request.args["action"])[0] == '18'):
            aRes = jsonpickle.encode(self.aDevice)
            return aRes
        elif( (request.args["action"])[0] == 'listTemplates'):
            aRboxName = self.aDevice.listAvlTemplate()
            return jsonpickle.encode(aRboxName)
        elif( (request.args["action"])[0] == 'AreYouAlive'):
            return 'YES'
        elif( (request.args["action"])[0] == 'stop'):
            self.devices.stop()
            time.sleep(5)
            reactor.callLater(1, reactor.stop)
            return("bye")
            time.sleep(5)
            sys.exit()
        return 'toto'

class UsbHandler(LineReceiver):
    """protocol handling class for USB """

    def __init__(self,iBrain,iRegisteredDevice):
        self.brain = iBrain
        self.registeredDevices = iRegisteredDevice
        
    def lineReceived(self, line):
        logging.info("USB Handler created to process : " + str(line))
        self.brain.HandleUsbInput(line,self.registeredDevices)
        self.brain.smartProcessing2(self.registeredDevices)
            
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
            aRest = aBrain.ReadDeviceStatus2(data,aRegisterDevices)
            logging.info("READ command res " + str(aRest))
            self.transport.write(str(aRest))
        elif str(data) == "STOP": 
            logging.info("STOP command")
            aBrain.stop()
            reactor.stop()
        else:
            logging.info("Write command")
            aBrain.SendMessage(data,"DUM",aRegisterDevices)
            self.transport.write("ACK")
            self.brain.smartProcessing2(self.registeredDevices)
        
def tired_task(iBrain):
    #logging.info("I want to run slowly" + str (datetime.datetime.now()))
    iBrain.smartProcessing2(aRegisterDevices)
    
#The logging API 
logging.basicConfig(filename='PythonWrapperWebArduinoUsbD.log',level=logging.WARNING,format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Daemon starting...')

#The config API (contains non shared data like google API key or password)
with open('ConfigFiles') as json_data:
    Config = json.load(json_data)

#The brain
aBrain = Deipara_Brain.Brain(Config)
logging.info('aBrain : ' + str(aBrain))
#Object that handle all devices present on the networl
aRegisterDevices =Deipara_Objects.DevicesHandler(Config)
aRegisterDevices.loadDevices()
logging.info('aRegisterDevices : ' + str(aRegisterDevices))

root = static.File("./Web")
indexPage = resource.Resource()
root.processors = {".php": PhpScript}
formHandler = FormPage(aRegisterDevices)
root.putChild('index.html', indexPage)
root.putChild('handler.html', formHandler)
reactor.listenTCP(80, server.Site(root))

r = Example(aBrain,aRegisterDevices)
reactor.listenTCP(49007, server.Site(r))

reactor.listenTCP(50007, TcpHandlerFactory(aBrain,aRegisterDevices))
SerialPort(UsbHandler(aBrain,aRegisterDevices), '/dev/ttyACM0', reactor, 9600)

lc2 = LoopingCall(tired_task, aBrain)
lc2.start(10)

reactor.run()
