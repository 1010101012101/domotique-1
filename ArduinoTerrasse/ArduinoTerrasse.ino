//Libraries definitions
//Xbee library
#include <XBee.h>
//Deipara library
#include <Deipara.h>

//pin guirlande led
const int _OutDebugLed = 8;
const int _OutXbeeWakeUp = 7;
const int _InLightPin = 4;

//Xbee objects
//create Xbee object to control a Xbee
XBee _Xbee = XBee(); 
//Create reusable response objects for responses we expect to handle
ZBRxResponse _ZbRxResp = ZBRxResponse(); 
//Global variable used in the program
int _CmdReceived = 0;
int _DataToSend = 0;



void setup()
{
  // start serial
  _Xbee.begin(XBEE_SPEED); 
  Serial.begin(XBEE_SPEED);
  //defined IO
  pinMode(_OutDebugLed, OUTPUT);
  pinMode(_OutXbeeWakeUp, OUTPUT);
  pinMode(_InLightPin, INPUT);
  
  digitalWrite(_OutDebugLed, LOW);
  
  delay(2000);
}

void loop()
{
  //digitalWrite(_OutDebugLed, HIGH);
  digitalWrite(_OutXbeeWakeUp, LOW);
  delay(5000);
  unsigned int val = analogRead(_InLightPin);    // read the input pin
  sendZigBeeMsg2(_Xbee,36,val,COORD_ADDR);
  //digitalWrite(_OutDebugLed, LOW);
  digitalWrite(_OutXbeeWakeUp, HIGH);
  delay(300000);

}
