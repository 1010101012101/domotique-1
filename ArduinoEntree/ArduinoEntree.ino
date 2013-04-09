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
const int _InPinDht22 = 10;

//Xbee objects
//create Xbee object to control a Xbee
XBee _Xbee = XBee(); 
//Create reusable response objects for responses we expect to handle
ZBRxResponse _ZbRxResp = ZBRxResponse(); 
//Global variable used in the program
int _CmdReceived = 0;
int _DataToSend = 0;
bool _TimerExpire = true;
DHT22 _Dht22(_InPinDht22); //Setup a DHT22 instance

void InterruptTimer2() 
{
  _TimerExpire= true;
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
  MsTimer2::set(120000, InterruptTimer2);
  
  //Wait 5 minutes before starting anything
  delay(5000);
}

void loop()
{
  _CmdReceived = 0;
  _DataToSend = 0;
  _Xbee.readPacket();
  //Read button status
  int aInputDigitalValue = digitalRead(_InPinIrDetector);

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
  
  if ((aInputDigitalValue == HIGH)&&(_TimerExpire == true))
  {
    _TimerExpire = false;
    _CmdReceived = 50;
    _DataToSend=440;
    MsTimer2::start(); // active Timer 2 
  }

  //Do the real action
  if(_CmdReceived==34)
  {
    //This command allow the master to turn the light on
    digitalWrite(_OutPinRelay, HIGH);
  }
  else if(_CmdReceived==35)
  {
    //This command allow the master to turn the light off
    digitalWrite(_OutPinRelay, LOW);
  }
  else if(_CmdReceived==33)
  {
  //for debuging; simulate light on event
	 delay(1000);
    _CmdReceived = 50;
    _DataToSend=445;
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
      if (_CmdReceived==30)
      {
        _DataToSend=_Dht22.getTemperatureCAsInt();
      }
      else if(_CmdReceived==31)
      {
        _DataToSend=_Dht22.getHumidityAsInt();
      }
      break;
    case DHT_ERROR_CHECKSUM:
      Serial.print("check sum error ");
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
    sendZigBeeMsg2(_Xbee,_CmdReceived,_DataToSend,COORD_ADDR);
  }
}
