//Libraries definitions
//Xbee library
#include <XBee.h>
//Deipara library
#include <Deipara.h>

//Pin definition
const int _OutPinLed = 9;

//Xbee objects
//create Xbee object to control a Xbee
XBee _Xbee = XBee(); 
//Create reusable response objects for responses we expect to handle
ZBRxResponse _ZbRxResp = ZBRxResponse(); 
//Global variable used in the program
int _CmdReceived = 0;

void setup()
{
  // start serial
  _Xbee.begin(XBEE_SPEED);
  Serial.begin(XBEE_SPEED);
  //defined IO
  pinMode(_OutPinLed, OUTPUT);
  
  digitalWrite(_OutPinLed, LOW);
  
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
    digitalWrite(_OutPinLed, HIGH);
  }
  else if(_CmdReceived==4)
  {
    //This command allow the master to turn the light off
    digitalWrite(_OutPinLed, LOW);
  }
}
