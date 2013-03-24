//Include for Xbee library -> http://code.google.com/p/xbee-arduino/
#include <XBee.h>
//Timer library
#include <MsTimer2.h>
//Deipara includes
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
    uint8_t aPayload[3];

	aPayload[0] = _CmdReceived; //LSB
    Serial.print("Data0: 0x");
    Serial.println(aPayload[0], HEX);
    aPayload[1] = _DataToSend & 0xff; //LSB
    Serial.print("Data1: 0x");
    Serial.println(aPayload[1], HEX);
    aPayload[2] = (_DataToSend >> 8) & 0xff; //MSB
    Serial.print("Data2: 0x");
    Serial.println(aPayload[2], HEX);

    // Specify the address of the remote XBee (this is the SH + SL)
    XBeeAddress64 aAddr64 = XBeeAddress64(COMMON_ADDR, COORD_ADDR);

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
