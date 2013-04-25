//Libraries definitions
//Xbee library
#include <XBee.h>
//Deipara library
#include <Deipara.h>

//Pin definition
//pin guirlande led
const int _OutPinLedBlue = 9;
const int _OutPinLedGreen = 10;
const int _OutPinLedRed = 11;

//Xbee objects
//create Xbee object to control a Xbee
XBee _Xbee = XBee(); 
//Create reusable response objects for responses we expect to handle
ZBRxResponse _ZbRxResp = ZBRxResponse(); 
//Global variable used in the program
int _CmdReceived = 0;

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
  // start serial
  _Xbee.begin(XBEE_SPEED);
  Serial.begin(XBEE_SPEED);
  //defined IO
  
  pinMode(_OutPinLedBlue, OUTPUT);
  pinMode(_OutPinLedGreen, OUTPUT);
  pinMode(_OutPinLedRed, OUTPUT);
  
  digitalWrite(_OutPinLedBlue, LOW);
  digitalWrite(_OutPinLedGreen, LOW);
  digitalWrite(_OutPinLedRed, LOW);
  
  
  delay(5000);
}

void loop()
{
  _CmdReceived = 0;
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
    }  
  }
  
  //Do the real action
  if(_CmdReceived==3)
  {
    //This command allow the master to turn the light on
    RandomLedColor();
  }
  else if(_CmdReceived==4)
  {
    //This command allow the master to turn the light off
    digitalWrite(_OutPinLedBlue, LOW);
    digitalWrite(_OutPinLedGreen, LOW);
    digitalWrite(_OutPinLedRed, LOW);
  }
}
