/*
  Deipara library
*/

#ifndef TwoWire_h
#define TwoWire_h

const unsigned long COMMON_ADDR=0x0013A200;

const unsigned long COORD_ADDR=0x400A3E5E;
const unsigned long ENTREE_ADDR=0x408CCB53;
const unsigned long TERRASSE_ADDR=0x400A3E5D;

const int XBEE_SPEED = 9600;

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

void sendZigBeeMsg(unsigned int iPayLoad, unsigned long iAddrToTarget)
{
  //Serial.println("We are going to send a ZigBee message");
  // Create an array for holding the data you want to send.
  uint8_t aPayload[1];
  // Fill it with the data
  aPayload[0] = iPayLoad;

  // Specify the address of the remote XBee (this is the SH + SL)
  XBeeAddress64 addr64 = XBeeAddress64(COMMON_ADDR, iAddrToTarget);

  // Create a TX Request
  ZBTxRequest zbTx = ZBTxRequest(addr64, aPayload, sizeof(aPayload));

  // Send your request
  _Xbee.send(zbTx);
  //Serial.println("Message Sent - Waiting for the ACK");

  if (_Xbee.readPacket(5000)) {
    //Serial.println("We got a response to the message");

    // should be a znet tx status  
    ZBTxStatusResponse aZbTxStatus = ZBTxStatusResponse();        
    if (_Xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE) {
      _Xbee.getResponse().getZBTxStatusResponse(aZbTxStatus);

      // get the delivery status, the fifth byte
      if (aZbTxStatus.getDeliveryStatus() == SUCCESS) {
        //Serial.println("The Trx was OK");
      } 
      else {
        Serial.println("Warning : The Trx was KO");
      }
    } 
    else{
      //Serial.print("It was not a Trx status. ApiId:");
      Serial.println(_Xbee.getResponse().getApiId());
    }   
  } 
  else {
    Serial.println("Warning : This should never happen");
  }
}

void sendZigBeeMsg2(int iCommand,int iDataToSend, unsigned long iAddrToTarget)
{
  //Serial.println("We are going to send a ZigBee message");
  // Create an array for holding the data you want to send.
  uint8_t aPayload[3];
  // Fill it with the data
  aPayload[0] = iCommand; //LSB
  Serial.print("Data0: 0x");
  Serial.println(aPayload[0], HEX);
  aPayload[1] = iDataToSend & 0xff; //LSB
  Serial.print("Data1: 0x");
  Serial.println(aPayload[1], HEX);
  aPayload[2] = (iDataToSend >> 8) & 0xff; //MSB
  Serial.print("Data2: 0x");
  Serial.println(aPayload[2], HEX);

  // Specify the address of the remote XBee (this is the SH + SL)
  XBeeAddress64 addr64 = XBeeAddress64(COMMON_ADDR, iAddrToTarget);

  // Create a TX Request
  ZBTxRequest zbTx = ZBTxRequest(addr64, aPayload, sizeof(aPayload));

  // Send your request
  _Xbee.send(zbTx);
  //Serial.println("Message Sent - Waiting for the ACK");

  if (_Xbee.readPacket(5000)) {
    //Serial.println("We got a response to the message");

    // should be a znet tx status  
    ZBTxStatusResponse aZbTxStatus = ZBTxStatusResponse();        
    if (_Xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE) {
      _Xbee.getResponse().getZBTxStatusResponse(aZbTxStatus);

      // get the delivery status, the fifth byte
      if (aZbTxStatus.getDeliveryStatus() == SUCCESS) {
        //Serial.println("The Trx was OK");
      } 
      else {
        Serial.println("Warning : The Trx was KO");
      }
    } 
    else{
      //Serial.print("It was not a Trx status. ApiId:");
      Serial.println(_Xbee.getResponse().getApiId());
    }   
  } 
  else {
    Serial.println("Warning : This should never happen");
  }
}

void sendZigBeeMsg3(int iCommand,int iDataToSend, unsigned long iAddrToTarget)
{
  //Serial.println("We are going to send a ZigBee message");
  // Create an array for holding the data you want to send.
  uint8_t aPayload[3];
  // Fill it with the data
  aPayload[0] = iCommand; //LSB
  Serial.print("Data0: 0x");
  Serial.println(aPayload[0], HEX);
  aPayload[1] = iDataToSend & 0xff; //LSB
  Serial.print("Data1: 0x");
  Serial.println(aPayload[1], HEX);
  aPayload[2] = (iDataToSend >> 8) & 0xff; //MSB
  Serial.print("Data2: 0x");
  Serial.println(aPayload[2], HEX);

  // Specify the address of the remote XBee (this is the SH + SL)
  XBeeAddress64 addr64 = XBeeAddress64(COMMON_ADDR, iAddrToTarget);

  // Create a TX Request
  ZBTxRequest zbTx = ZBTxRequest(addr64, aPayload, sizeof(aPayload));

  // Send your request
  _Xbee.send(zbTx);
  //Serial.println("Message Sent - Waiting for the ACK");

  if (_Xbee.readPacket(5000)) {
    //Serial.println("We got a response to the message");

    // should be a znet tx status  
    ZBTxStatusResponse aZbTxStatus = ZBTxStatusResponse();        
    if (_Xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE) {
      _Xbee.getResponse().getZBTxStatusResponse(aZbTxStatus);

      // get the delivery status, the fifth byte
      if (aZbTxStatus.getDeliveryStatus() == SUCCESS) {
        //Serial.println("The Trx was OK");
      } 
      else {
        Serial.println("Warning : The Trx was KO");
      }
    } 
    else{
      //Serial.print("It was not a Trx status. ApiId:");
      Serial.println(_Xbee.getResponse().getApiId());
    }   
  } 
  else {
    Serial.println("Warning : This should never happen");
  }
}






#endif