//Xbee library
#include <XBee.h>

//Timer library
#include <MsTimer2.h>

//Include for RHT03 library -> https://github.com/nethoncho/Arduino-DHT22
#include <DHT22.h>

//Xbee objects
//create Xbee object to control a Xbee
XBee _Xbee = XBee(); 
//Create reusable response objects for responses we expect to handle
ZBRxResponse _ZbRxResp = ZBRxResponse(); 

//Pin definition
const int _InPinIrDetector = 7;
const int _OutPinRelay = 11;
const int _InPinLedMeasure = A0;
const int _InPinMoistureMeasure = A1;
const int _InPinDht22 = 10;
const int _OutPinBuz1 = 9;

//Global variable used in the program
int _CmdReceived = 0;
int _AllowAutoLight = 1;
int _DataToSend = 0;

DHT22 _Dht22(_InPinDht22); //Setup a DHT22 instance

void InterruptTimer2() 
{
  digitalWrite(_OutPinRelay, LOW);
}

void flashPin(int pin, int times, int wait) 
{
  for (int i = 0; i < times; i++) {
    digitalWrite(pin, HIGH);
    delay(wait);
    digitalWrite(pin, LOW);

    if (i + 1 < times) {
      delay(wait);
    }
  }
}

void sendZigBeeMsg(unsigned int iPayLoad, unsigned long iAddrToTarget)
{
  Serial.println("We are going to send a ZigBee message");
  // Create an array for holding the data you want to send.
  uint8_t aPayload[1];
  // Fill it with the data
  aPayload[0] = iPayLoad;

  // Specify the address of the remote XBee (this is the SH + SL)
  XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, iAddrToTarget);

  // Create a TX Request
  ZBTxRequest zbTx = ZBTxRequest(addr64, aPayload, sizeof(aPayload));

  // Send your request
  _Xbee.send(zbTx);
  Serial.println("Message Sent - Waiting for the ACK");

  if (_Xbee.readPacket(5000)) {
    Serial.println("We got a response to the message");

    // should be a znet tx status  
    ZBTxStatusResponse aZbTxStatus = ZBTxStatusResponse();        
    if (_Xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE) {
      _Xbee.getResponse().getZBTxStatusResponse(aZbTxStatus);

      // get the delivery status, the fifth byte
      if (aZbTxStatus.getDeliveryStatus() == SUCCESS) {
        Serial.println("The Trx was OK");
      } 
      else {
        Serial.println("Warning : The Trx was KO");
      }
    } 
    else{
      Serial.print("It was not a Trx status. ApiId:");
      Serial.println(_Xbee.getResponse().getApiId());
    }   
  } 
  else {
    Serial.println("Warning : This should never happen");
  }
}

void setup()
{
  // start serial
  _Xbee.begin(9600);
  // Remember to set baud rate in Serial Monitor or lower this to 9600 (default value)
  Serial.begin(9600);

  //defined IO
  pinMode(_InPinIrDetector,INPUT);
  pinMode(_OutPinRelay, OUTPUT);
  
  digitalWrite(_OutPinRelay, LOW);
  
  //Set timer to 10seconds
  MsTimer2::set(60000, InterruptTimer2);
  delay(1000);
}

void loop()
{
  _CmdReceived = 0;
  _DataToSend = 0;
  _Xbee.readPacket();
  //Read button status
  int aInputDigitalValue = digitalRead(_InPinIrDetector);

  if (aInputDigitalValue == LOW)
  {
    if (_AllowAutoLight == 1)
    {
      digitalWrite(_OutPinRelay, HIGH);
      MsTimer2::start(); // active Timer 2 
    }
    
    //2/Send the detection info to central
    unsigned long aReceiver = 0x400a3e5e;
    unsigned int aCommand = 3;
    sendZigBeeMsg(aCommand, aReceiver);
  }

  if (_Xbee.getResponse().isAvailable()) 
  {
    // got something
    if (_Xbee.getResponse().getApiId() == ZB_RX_RESPONSE) 
    {
      // now fill our zb rx class
      _Xbee.getResponse().getZBRxResponse(_ZbRxResp);
      _CmdReceived = _ZbRxResp.getData(0);
    }  
  }

  //Do the real action
  if(_CmdReceived==4)
  {
    //This command allow the master to turn the light on
    //flashPin(_OutPinRelay, _CmdReceived, 400);
    digitalWrite(_OutPinRelay, HIGH);
  }
  else if(_CmdReceived==5)
  {
    
    //This command allow the master to turn the light off
    digitalWrite(_OutPinRelay, LOW);
  }
  else if(_CmdReceived==6)
  {
    //This command allow to trig the "user detected" even
    digitalWrite(_OutPinRelay, HIGH);
    MsTimer2::start(); // active Timer 2 
  }
  else if(_CmdReceived==7)
  {
     _AllowAutoLight=1;
  }
  else if(_CmdReceived==8)
  {
     _AllowAutoLight=0;
  }
  else if(_CmdReceived==9)
  {
  //for debuging; simulate light on event
     //2/Send the detection info to central
	 delay(1000);
    unsigned long aReceiver = 0x400a3e5e;
    unsigned int aCommand = 3;
    sendZigBeeMsg(aCommand, aReceiver);
  }
  else if(_CmdReceived==1)
  {
     _DataToSend=analogRead(_InPinLedMeasure);
    Serial.print("Light Value : ");
    Serial.println(_DataToSend);
  }
  else if((_CmdReceived==2)||(_CmdReceived==3))
  {
    delay(50);
    DHT22_ERROR_t errorCode;
    Serial.print("Requesting data...");
    errorCode = _Dht22.readData();
    
    switch(errorCode)
    {
    case DHT_ERROR_NONE:
      Serial.print("Got Data ");
      Serial.print(_Dht22.getTemperatureCAsFloat());
      Serial.print("/");
      Serial.print(_Dht22.getTemperatureCAsInt());
      Serial.print("C ");
      Serial.print(_Dht22.getHumidityAsFloat());
      Serial.print("/");
      Serial.print(_Dht22.getHumidityAsInt());
      Serial.println("%");
      if (_CmdReceived==2)
      {
        _DataToSend=_Dht22.getTemperatureCAsInt();
      }
      else if(_CmdReceived==3)
      {
        _DataToSend=_Dht22.getHumidityAsInt();
      }
      break;
    case DHT_ERROR_CHECKSUM:
      Serial.print("check sum error ");
      Serial.print(_Dht22.getTemperatureCAsFloat());
      Serial.print("C ");
      Serial.print(_Dht22.getHumidityAsFloat());
      Serial.println("%");
      break;
    case DHT_BUS_HUNG:
      Serial.println("BUS Hung ");
      break;
    case DHT_ERROR_NOT_PRESENT:
      Serial.println("Not Present ");
      break;
    case DHT_ERROR_ACK_TOO_LONG:
      Serial.println("ACK time out ");
      break;
    case DHT_ERROR_SYNC_TIMEOUT:
      Serial.println("Sync Timeout ");
      break;
    case DHT_ERROR_DATA_TIMEOUT:
      Serial.println("Data Timeout ");
      break;
    case DHT_ERROR_TOOQUICK:
      Serial.println("Polled to quick ");
      break;
    }
  }
  
    //Send the response if necessary
  if(_DataToSend!=0)
  {
    uint8_t aPayload[2];

    aPayload[0] = _DataToSend & 0xff; //LSB
    Serial.print("Data0: 0x");
    Serial.println(aPayload[0], HEX);
    aPayload[1] = (_DataToSend >> 8) & 0xff; //MSB
    Serial.print("Data1: 0x");
    Serial.println(aPayload[1], HEX);

    // Specify the address of the remote XBee (this is the SH + SL)
    XBeeAddress64 aAddr64 = XBeeAddress64(0x0013a200, 0x400a3e5e);

    // Create a TX Request
    ZBTxRequest aZbTx = ZBTxRequest(aAddr64, aPayload, sizeof(aPayload));

    // Send your request
    _Xbee.send(aZbTx);

    Serial.println("Message has been sent");

    if (_Xbee.readPacket(5000)) {
      Serial.println("We got a response to the message");

      // should be a znet tx status  

      ZBTxStatusResponse aZbTxStatus = ZBTxStatusResponse();        
      if (_Xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE) {
        Serial.println("It is a transmition status");
        _Xbee.getResponse().getZBTxStatusResponse(aZbTxStatus);

        // get the delivery status, the fifth byte
        if (aZbTxStatus.getDeliveryStatus() == SUCCESS) {
          Serial.println("The Trx was OK");
        } 
        else {
          Serial.println("Warning : The Trx was KO");
        }
      } 
      else{
        Serial.print("It was not a Trx status. ApiId:");
        Serial.println(_Xbee.getResponse().getApiId());
      }   
    } 
    else {
      Serial.println("Warning : This should never happen");
    }
  }
}


