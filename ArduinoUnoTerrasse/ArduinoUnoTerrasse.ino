//Libraries definitions
//Xbee library
#include <XBee.h>
//Timer library
#include <MsTimer2.h>
//Deipara library
#include <Deipara.h>

//Definition of the pin used in program
const int _OutPinBuz = 9;
const int _OutPinLed4 = 10;
const int _InPinButton4 = 11;
const int _InPinFireDetection = 8;
const int _InPinLedMeasure = A0;

//Global variables
XBee _Xbee = XBee(); //Create Xbee object to control a Xbee
ZBRxResponse _ZbRxResp = ZBRxResponse(); //Create reusable response objects for responses we expect to handle
int _CurrentLightValue = 0;
int _CmdReceived = 0;
int _DataToSend = 0;
bool _TimerExpire = true;

void InterruptTimer2() 
{
  _TimerExpire= true;
  MsTimer2::stop();
}

void setup() 
{
  // start serial port
  Serial.begin(XBEE_SPEED);
  _Xbee.begin(XBEE_SPEED);
  
  pinMode(_OutPinLed4, OUTPUT);
  pinMode(_OutPinBuz, OUTPUT);
  pinMode(_InPinButton4,INPUT);
  pinMode(_InPinFireDetection,INPUT);
  
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
  
  int aInputDigitalValue = digitalRead(_InPinButton4);

  if ((aInputDigitalValue == LOW)&&(_TimerExpire == true))
  {
  _TimerExpire = false;
  flashPin(_OutPinBuz, 1, 250);
  _CmdReceived=1;
  _DataToSend=444;
  MsTimer2::start(); // active Timer 2 
  }

  //Test if we have an action to do 
  if(_CmdReceived==40)
  {
    flashPin(_OutPinBuz, 1, 250);
  }
  else if(_CmdReceived==39)
  {
    //_DataToSend=analogRead(_InPinLedMeasure);
	_DataToSend=456;
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
