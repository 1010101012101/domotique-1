//Libraries definitions
//Xbee library
#include <XBee.h>
//Deipara library
#include <Deipara.h>
//RHT03 library
#include <DHT22.h>
//Timer library
#include <MsTimer2.h>

//Pin definition
const int _InPinIrDetector = 7;
//pin guirlande led
const int _OutPinLedBlue = 9;
const int _OutDebugLed = 8;
const int _OutPinLedGreen = 10;
const int _OutPinLedRed = 11;
const int _InPinDht22 = 6;

//Xbee objects
//create Xbee object to control a Xbee
XBee _Xbee = XBee(); 
//Create reusable response objects for responses we expect to handle
ZBRxResponse _ZbRxResp = ZBRxResponse(); 
//Global variable used in the program
int _CmdReceived = 0;
int _DataToSend = 0;
DHT22 _Dht22(_InPinDht22); //Setup a DHT22 instance
bool _TimerExpire = true;

void InterruptTimer2() 
{
  _TimerExpire= true;
  MsTimer2::stop();
}

void RandomLedColor() 
{
  Serial.println("RandomLedColor");
  int randNumberGreen = random(0, 255);
  int randNumberRed = random(0, 255);
  int randNumberBlue = random(0, 255);
  
  analogWrite(_OutPinLedBlue, randNumberGreen); // impulsion largeur voulue sur la broche 0 = 0% et 255 = 100% haut
  analogWrite(_OutPinLedGreen, randNumberRed); // impulsion largeur voulue sur la broche 0 = 0% et 255 = 100% haut
  analogWrite(_OutPinLedRed, randNumberBlue); // impulsion largeur voulue sur la broche 0 = 0% et 255 = 100% haut
  
  digitalWrite(_OutDebugLed, HIGH);
}

void setup()
{
  // start serial
  _Xbee.begin(XBEE_SPEED);
  Serial.begin(XBEE_SPEED);
  //defined IO
  pinMode(_InPinIrDetector,INPUT);
  pinMode(_OutPinLedBlue, OUTPUT);
  pinMode(_OutPinLedGreen, OUTPUT);
  pinMode(_OutPinLedRed, OUTPUT);
  pinMode(_OutDebugLed, OUTPUT);
  
  digitalWrite(_OutPinLedBlue, LOW);
  digitalWrite(_OutPinLedGreen, LOW);
  digitalWrite(_OutPinLedRed, LOW);
  
  digitalWrite(_OutDebugLed, LOW);
  
  //Set timer to 10seconds
  MsTimer2::set(120000, InterruptTimer2);
  
  delay(5000);
}

void loop()
{
  _CmdReceived = 0;
  _DataToSend = 0;
  _Xbee.readPacket();
  
  if (_Xbee.getResponse().isAvailable()) 
  {
    // got something
    Serial.println("got something");
    if (_Xbee.getResponse().getApiId() == ZB_RX_RESPONSE) 
    {
      // now fill our zb rx class
      _Xbee.getResponse().getZBRxResponse(_ZbRxResp);
      _CmdReceived = _ZbRxResp.getData(0);
      Serial.println(_CmdReceived);
    }  
  }
  
  int aInputDigitalValue = digitalRead(_InPinIrDetector);
  if ((aInputDigitalValue == HIGH)&&(_TimerExpire == true))
  {
    _TimerExpire = false;
    _CmdReceived = 17;
    _DataToSend=328;
    MsTimer2::start(); // active Timer 2 
  }
  
  //Do the real action
  if(_CmdReceived==3)
  {
    //This command allow the master to turn the light on
    RandomLedColor();
    //digitalWrite(_OutPinLedRed, HIGH);
  }
  else if(_CmdReceived==4)
  {
    //This command allow the master to turn the light off
    digitalWrite(_OutPinLedBlue, LOW);
    digitalWrite(_OutPinLedGreen, LOW);
    digitalWrite(_OutPinLedRed, LOW);
  }
    else if((_CmdReceived==18)||(_CmdReceived==19))
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
      if (_CmdReceived==18)
      {
        _DataToSend=_Dht22.getTemperatureCAsInt();
      }
      else if(_CmdReceived==19)
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
    Serial.println("sending");
    Serial.println(_DataToSend);
    Serial.println(_CmdReceived);
    sendZigBeeMsg2(_Xbee,_CmdReceived,_DataToSend,COORD_ADDR);
  }
  
}
