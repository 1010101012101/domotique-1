//Libraries definitions
//Xbee library
#include <XBee.h>
//Timer library
#include <MsTimer2.h>
//RHT03 library
#include <DHT22.h>
//Deipara library
#include <Deipara.h>

//Pin definition
const int _InPinIrDetector = 7;
const int _OutPinRelay = 11;
const int _InPinLedMeasure = A0;
const int _InPinMoistureMeasure = A1;
const int _InPinDht22 = 10;
const int _OutPinBuz1 = 9;

//Xbee objects
//create Xbee object to control a Xbee
XBee _Xbee = XBee(); 
//Create reusable response objects for responses we expect to handle
ZBRxResponse _ZbRxResp = ZBRxResponse(); 
//Global variable used in the program
int _CmdReceived = 0;
int _AllowAutoLight = 1;
int _DataToSend = 0;
bool _TimerExpire = true;
DHT22 _Dht22(_InPinDht22); //Setup a DHT22 instance

void InterruptTimer2() 
{
  _TimerExpire= true;
  digitalWrite(_OutPinRelay, LOW);
  MsTimer2::stop();
}

void setup()
{
  // start serial
  _Xbee.begin(XBEE_SPEED);
  Serial.begin(XBEE_SPEED);

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

  if (aInputDigitalValue == HIGH)
  {
    if (_AllowAutoLight == 1)
    {
      _TimerExpire = false;
      digitalWrite(_OutPinRelay, HIGH);
      MsTimer2::start(); // active Timer 2 
    }
    if (_TimerExpire == true)
    {
        //2/Send the detection info to central
        unsigned int aCommand = 3;
        //sendZigBeeMsg(aCommand, COORD_ADDR);
    }
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
  if(_CmdReceived==34)
  {
    //This command allow the master to turn the light on
    //flashPin(_OutPinRelay, _CmdReceived, 400);
    digitalWrite(_OutPinRelay, HIGH);
  }
  else if(_CmdReceived==35)
  {
    
    //This command allow the master to turn the light off
    digitalWrite(_OutPinRelay, LOW);
  }
  else if(_CmdReceived==36)
  {
    //This command allow to trig the "user detected" even
    digitalWrite(_OutPinRelay, HIGH);
    MsTimer2::start(); // active Timer 2 
  }
  else if(_CmdReceived==37)
  {
     _AllowAutoLight=1;
  }
  else if(_CmdReceived==38)
  {
     _AllowAutoLight=0;
  }
  else if(_CmdReceived==33)
  {
  //for debuging; simulate light on event
     //2/Send the detection info to central
	 delay(1000);
    unsigned int aCommand = 3;
    sendZigBeeMsg(aCommand, COORD_ADDR);
  }
  else if(_CmdReceived==32)
  {
     _DataToSend=analogRead(_InPinLedMeasure);
    Serial.print("Light Value : ");
    Serial.println(_DataToSend);
  }
  else if((_CmdReceived==30)||(_CmdReceived==31))
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
      if ((_CmdReceived==2)||(_CmdReceived==30))
      {
        _DataToSend=_Dht22.getTemperatureCAsInt();
      }
      else if((_CmdReceived==3)||(_CmdReceived==31))
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
    sendZigBeeMsg2(_CmdReceived,_DataToSend,COORD_ADDR);
  }
}
