//Libraries definitions
//Xbee library
#include <XBee.h>
//Timer library
#include <MsTimer2.h>
//RHT03 library
#include <DHT22.h>
//Deipara library
#include <Deipara.h>

//Definition of the pin used in program
const int _InPinIrDetector = 6;
const int _InPinFireDetection = 8;
const int _InPinDht22 = 5;
//pin guirlande led
const int _OutPinLedBlue = 9;
const int _OutPinLedGreen = 10;
const int _OutPinLedRed = 11;

//Global variables
XBee _Xbee = XBee(); //Create Xbee object to control a Xbee
ZBRxResponse _ZbRxResp = ZBRxResponse(); //Create reusable response objects for responses we expect to handle
int _CurrentLightValue = 0;
int _CmdReceived = 0;
int _DataToSend = 0;
bool _TimerExpire = true;
bool _LedGuirlandeIsOn = false;
DHT22 _Dht22(_InPinDht22); //Setup a DHT22 instance

void InterruptTimer2() 
{
  _TimerExpire= true;
  MsTimer2::stop();
}

void RandomLedColor() 
{
  int randNumberGreen = random(0, 255);
  int randNumberRed = random(0, 255);
  int randNumberBlue = random(0, 255);
  
  analogWrite(_OutPinLedBlue, randNumberBlue); // impulsion largeur voulue sur la broche 0 = 0% et 255 = 100% haut
  analogWrite(_OutPinLedGreen, randNumberGreen); // impulsion largeur voulue sur la broche 0 = 0% et 255 = 100% haut
  analogWrite(_OutPinLedRed, randNumberRed); // impulsion largeur voulue sur la broche 0 = 0% et 255 = 100% haut
}

void setup() 
{
  // start serial port
  Serial.begin(XBEE_SPEED);
  _Xbee.begin(XBEE_SPEED);
  
  pinMode(_InPinIrDetector,INPUT);
  pinMode(_InPinFireDetection,INPUT);
  pinMode(_OutPinLedBlue, OUTPUT);
  pinMode(_OutPinLedGreen, OUTPUT);
  pinMode(_OutPinLedRed, OUTPUT);
  
  digitalWrite(_OutPinLedBlue, LOW);
  digitalWrite(_OutPinLedGreen, LOW);
  digitalWrite(_OutPinLedRed, LOW);
  
  //Set timer to 10seconds
  MsTimer2::set(30000, InterruptTimer2);
}

// continuously reads packets, looking for ZB Receive or Modem Status
void loop() {
  //Reset command to 0
  _CmdReceived = 0;
  _DataToSend = 0;

  //Read if we received an inoming message
  _Xbee.readPacket();
  if (_Xbee.getResponse().isAvailable()) {
    Serial.println("We have something on the serial");
    Serial.print("ApiId: 0x");
    Serial.println(_Xbee.getResponse().getApiId(), HEX);

    if (_Xbee.getResponse().getApiId() == ZB_RX_RESPONSE) {
      Serial.println("This is a ZB response");
      _Xbee.getResponse().getZBRxResponse(_ZbRxResp);
      _CmdReceived = _ZbRxResp.getData(0);
      Serial.print("Data0: 0x");
      Serial.println(_CmdReceived, HEX);
    }  
  }
  
  int aInputDigitalValue = digitalRead(_InPinFireDetection);
  if ((aInputDigitalValue == HIGH)&&(_TimerExpire == true))
  {
  _TimerExpire = false;
  _CmdReceived=1;
  _DataToSend=444;
  MsTimer2::start(); // active Timer 2 
  }
  
  aInputDigitalValue = digitalRead(_InPinIrDetector);
  if ((aInputDigitalValue == HIGH)&&(_TimerExpire == true))
  {
    _TimerExpire = false;
    _CmdReceived = 51;
    _DataToSend=448;
    MsTimer2::start(); // active Timer 2 
  }

  //Test if we have an action to do 
  if((_CmdReceived==39)||(_CmdReceived==40))
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
      if (_CmdReceived==39)
      {
        _DataToSend=_Dht22.getTemperatureCAsInt();
      }
      else if(_CmdReceived==40)
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
  else if(_CmdReceived==47)
  {
    //turn led off
    Serial.println("turn led off");
    digitalWrite(_OutPinLedBlue, LOW);
    digitalWrite(_OutPinLedGreen, LOW);
    digitalWrite(_OutPinLedRed, LOW);
  }
  else if(_CmdReceived==46)
  {
    //random led color
    Serial.println("random led color");
    RandomLedColor();
  }
  else
  {
    //Serial.print("Nothing to do...");
  }
    if(_DataToSend!=0)
  {
    sendZigBeeMsg2(_Xbee,_CmdReceived,_DataToSend,COORD_ADDR);
  }
}
