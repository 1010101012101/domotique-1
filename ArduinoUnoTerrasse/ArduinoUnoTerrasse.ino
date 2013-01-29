//Include for Xbee library -> http://code.google.com/p/xbee-arduino/
#include <XBee.h>

//Include for RHT03 library -> https://github.com/nethoncho/Arduino-DHT22
#include <DHT22.h>

//Definition of the pin used in program
const int _InPinLedMeasure = A0;
const int _InPinMoistureMeasure = A1;
const int _InPinDht22 = 10;
const int _OutPinBuz1 = 9;
const int _InPinButton4 = 7;

//Global variables
XBee _Xbee = XBee(); //Create Xbee object to control a Xbee
ZBRxResponse _ZbRxResp = ZBRxResponse(); //Create reusable response objects for responses we expect to handle
DHT22 _Dht22(_InPinDht22); //Setup a DHT22 instance
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
  
  pinMode(_OutPinBuz1, OUTPUT);
  pinMode(_InPinButton4,INPUT);
  
  flashPin(_OutPinBuz1, 1, 250);
}

// continuously reads packets, looking for ZB Receive or Modem Status
void loop() {

  //Reset command to 0
  _CmdReceived = 0;
  _DataToSend=0;
  
  int aSendMsgToEd4 = digitalRead(_InPinButton4);
  if (aSendMsgToEd4 == LOW)
  {
  flashPin(_OutPinBuz1, 1, 250);
  }

  //Read if we received an inoming message
  _Xbee.readPacket();
  if (_Xbee.getResponse().isAvailable()) {
    // got something
    Serial.println("We have something on the serial");
    Serial.print("ApiId: 0x");
    Serial.println(_Xbee.getResponse().getApiId(), HEX);

    if (_Xbee.getResponse().getApiId() == ZB_RX_RESPONSE) {
      Serial.println("This is a ZB response");
      // got a zb rx packet

      // now fill our zb rx class
      _Xbee.getResponse().getZBRxResponse(_ZbRxResp);
      _CmdReceived = _ZbRxResp.getData(0);
      Serial.print("Data0: 0x");
      Serial.println(_CmdReceived, HEX);
    }  
  }

  //Test if we have an action to do 
  if(_CmdReceived==1)
  {
    _DataToSend=analogRead(_InPinLedMeasure);
    Serial.print("Light Value : ");
    Serial.println(_DataToSend);
  }
  else if((_CmdReceived==2)||(_CmdReceived==3))
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
      if (_CmdReceived==2)
      {
        _DataToSend=_Dht22.getTemperatureCAsInt();
      }
      else if(_CmdReceived==3)
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
  else if(_CmdReceived==4)
  {
    _DataToSend=analogRead(_InPinMoistureMeasure);
    Serial.print("Moisture Value : ");
    Serial.println(_DataToSend);
  }
  else
  {
    //Serial.print("Nothing to do...");
  }


  //Send the response if necessary
  if(_CmdReceived!=0)
  {
    uint8_t aPayload[2];

    aPayload[0] = _DataToSend & 0xff; //LSB
    Serial.print("Data0: 0x");
    Serial.println(aPayload[0], HEX);
    aPayload[1] = (_DataToSend >> 8) & 0xff; //MSB
    Serial.print("Data1: 0x");
    Serial.println(aPayload[1], HEX);

    // Specify the address of the remote XBee (this is the SH + SL)
    XBeeAddress64 aAddr64 = XBeeAddress64(0x0013a200, 0x400a3e5e);

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







