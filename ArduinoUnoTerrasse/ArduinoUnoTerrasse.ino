//Include for Xbee library -> http://code.google.com/p/xbee-arduino/
#include <XBee.h>

//Definition of the pin used in program
const int _OutPinLed4 = 10;
const int _InPinButton4 = 11;

//Global variables
XBee _Xbee = XBee(); //Create Xbee object to control a Xbee
ZBRxResponse _ZbRxResp = ZBRxResponse(); //Create reusable response objects for responses we expect to handle

int _CurrentLightValue = 0;
int _CmdReceived = 0;
int _DataToSend = 0;

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

void setup() 
{
  // start serial port
  Serial.begin(9600);
  // start serial
  _Xbee.begin(9600);
  
  pinMode(_OutPinLed4, OUTPUT);
  pinMode(_InPinButton4,INPUT);
}

// continuously reads packets, looking for ZB Receive or Modem Status
void loop() {
  //Reset command to 0
  _CmdReceived = 0;

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

  //Test if we have an action to do 
  if(_CmdReceived==4)
  {
    flashPin(_OutPinLed4, 1, 250);
  }
  else
  {
    //Serial.print("Nothing to do...");
  }
}
