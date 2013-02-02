//Xbee library
#include <XBee.h>
//X10
#include <X10ex.h>

#define POWER_LINE_MSG "PL:"
#define POWER_LINE_BUFFER_ERROR "PL:_ExBuffer"
#define SERIAL_DATA_MSG "SD:"
#define SERIAL_DATA_THRESHOLD 1000
#define SERIAL_DATA_TIMEOUT "SD:_ExTimOut"
#define MODULE_STATE_MSG "MS:"
#define MSG_DATA_ERROR "_ExSyntax"
//Next

XBee _Xbee = XBee(); // create Xbee object to control a Xbee
ZBRxResponse _ZbRxResp = ZBRxResponse(); //Create reusable response objects for responses we expect to handle



//Define the pin number
const int _OutPinLedTest = 7;
const int PIN_BOUTON_ON = 4;
const int PIN_BOUTON_OFF = 3;

// Fields used for serial and byte message reception
unsigned long sdReceived;
char bmHouse;
byte bmUnit;
byte bmCommand;
byte bmExtCommand;
int _CmdReceived = 0;
int _UsbCmdReceived = 0;
int _DataToSend = 0;

//Config cable XM10:
// 1 2 3 4
// -------
// |     |
// |     |
//  |   | 
//   |_|
// Dans mon cas : 
//1 : jaune : zero crossing : output
//2 : vert : GND
//3 : rouge : : output
//4 : noir : : input
//Config Arduino
// Zero crossing sur pin 2
// 3rouge vers 10
// 4noir vers 9

// X10 Power Line Communication Library
X10ex x10ex = X10ex(
  1, // Zero Cross Interrupt Number (2 = "Custom" Pin Change Interrupt)
  2, // Zero Cross Interrupt Pin (Pin 4-7 can be used with interrupt 2)
  9, // Power Line Transmit Pin 
  10, // Power Line Receive Pin
  true, // Enable this to see echo of what is transmitted on the power line
  powerLineEvent, // Event triggered when power line message is received
  1, // Number of phases (1 = No Phase Repeat/Coupling)
  50 // The power line AC frequency (e.g. 50Hz in Europe, 60Hz in North America)
);

void setup()
{
  //defined input button
  pinMode(_OutPinLedTest,OUTPUT);
  pinMode(PIN_BOUTON_ON,INPUT);
  pinMode(PIN_BOUTON_OFF,INPUT);
  
  //Active resistor as pull up
  digitalWrite(PIN_BOUTON_ON,HIGH);
  digitalWrite(PIN_BOUTON_OFF,HIGH);

  // start serial
  _Xbee.begin(9600);
    // Remember to set baud rate in Serial Monitor or lower this to 9600 (default value)
  Serial.begin(9600);
  // Start the Power Line Communication library
  x10ex.begin();
  //while (! Serial);
}

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
  XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, iAddrToTarget);

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
        //Serial.println("Warning : The Trx was KO");
      }
    } 
    else{
      //Serial.print("It was not a Trx status. ApiId:");
      //Serial.println(_Xbee.getResponse().getApiId());
    }   
  } 
  else {
    //Serial.println("Warning : This should never happen");
  }
}

void loop()
{
  _Xbee.readPacket();
  //Reset command to 0
  _CmdReceived = 0;
  _UsbCmdReceived = 0;
  _DataToSend = 0;

  if (_Xbee.getResponse().isAvailable()) {
    // got something
    //Serial.println("b");
    //Serial.print("ApiId: 0x");
    //flashPin(_OutPinLedTest, 3, 200);
    //Serial.println(_Xbee.getResponse().getApiId(), HEX);

    if (_Xbee.getResponse().getApiId() == ZB_RX_RESPONSE) {
      //Serial.write(45);
      
      // now fill our zb rx class
      _Xbee.getResponse().getZBRxResponse(_ZbRxResp);
      //flashPin(_OutPinLedTest, 3, 200);
	  _DataToSend=word(_ZbRxResp.getData(1),_ZbRxResp.getData(0));
      
    }  
  }
  
  // check for incoming serial data:
  if (Serial.available() > 0) {
    // read incoming serial data:
    _UsbCmdReceived = Serial.read();
    _CmdReceived = _UsbCmdReceived - 48;
    // Type the next ASCII value from what you received:
    //flashPin(_OutPinLedTest, 3, 200);
  }
 
 //Read button status
 int aInputDigitalValue = digitalRead(PIN_BOUTON_ON);
  //Reset the counter if button is press
  if ((aInputDigitalValue == LOW))
  {
    _CmdReceived=20;
   // flashPin(_OutPinLedTest, 3, 200);
    //x10ex.sendCmd('A', 5, CMD_OFF, 1);
    //x10ex.sendExtDim('A', 5, 40, 0, 1);
    //x10ex.sendExt('A',  5, CMD_EXTENDED_CODE,5, EXC_PRE_SET_DIM,1);
    //KO x10ex.sendExtDim('A', 5, 40, EXC_DIM_TIME_30, 1);
    //KO x10ex.sendExtDim('A', 5, 40, EXC_DIM_TIME_60, 1);
    //x10ex.sendExtDim('A', 5, 40, EXC_DIM_TIME_300, 1);
  //  x10ex.sendCmd('A', 5, CMD_DIM, 1);
    delay(1000);
   // OK x10ex.sendCmd('A', 5, CMD_BRIGHT, 1);
    
  }
  //aInputDigitalValue = digitalRead(PIN_BOUTON_OFF);
  //Reset the counter if button is press
  //if ((aInputDigitalValue == LOW))
  //{
  //  _CmdReceived=8;
  //}
  
  //Process the command
  //Test if we have an action to do 
  if(_CmdReceived==2)
  {
    unsigned int aCmd=5;
    unsigned long aAdrr=0x400a3e5d;
    sendZigBeeMsg(aCmd,aAdrr);
  }
  else if(_CmdReceived==3)
  {
    flashPin(_OutPinLedTest, 3, 200);
    delay(10);
    Serial.println("ACK_1");
    //Serial.flush();
    //if(Serial)
    //{
    //  flashPin(_OutPinLedTest, 5, 200);
    //}
    //else
    //{
    //  flashPin(_OutPinLedTest, 2, 200);
    //}
  }
  else if(_CmdReceived==4)
  {
    unsigned int aCmd=4;
    unsigned long aAdrr=0x400a3e5d;
    sendZigBeeMsg(aCmd,aAdrr);
  }
  else if(_CmdReceived==5)
  {
    x10ex.sendCmd('A', 4, CMD_ON, 1);
  }
  else if(_CmdReceived==6)
  {
    x10ex.sendCmd('A', 4, CMD_OFF, 1);
  }
  else if(_CmdReceived==7)
  {
    //flashPin(_OutPinLedTest, 2, 200);
    x10ex.sendCmd('A', 5, CMD_BRIGHT, 1);
  }
  else if(_CmdReceived==8)
  {
    //flashPin(_OutPinLedTest, 6, 200);
    x10ex.sendCmd('A', 5, CMD_DIM, 1);
  }
  else if(_CmdReceived==9)
  {
    x10ex.sendCmd('A', 7, CMD_BRIGHT, 1);
  }
  else if(_CmdReceived==10)
  {
    x10ex.sendCmd('A', 7, CMD_DIM, 1);
  }
  else if(_CmdReceived==11)
  {
    x10ex.sendCmd('A', 13, CMD_ON, 1);
  }
  else if(_CmdReceived==12)
  {
    x10ex.sendCmd('A', 13, CMD_OFF, 1);
  }
  else if(_CmdReceived==13)
  {
    x10ex.sendCmd('A', 6, CMD_ON, 1);
  }
  else if(_CmdReceived==14)
  {
    x10ex.sendCmd('A', 6, CMD_OFF, 1);
  }
  else if(_CmdReceived==15)
  {
    unsigned int aCmd=6;
    unsigned long aAdrr=0x400a3e5d;
    sendZigBeeMsg(aCmd,aAdrr);
  }
  else if(_CmdReceived==16)
  {
    unsigned int aCmd=7;
    unsigned long aAdrr=0x400a3e5d;
    sendZigBeeMsg(aCmd,aAdrr);
  }
  else if(_CmdReceived==17)
  {
    unsigned int aCmd=8;
    unsigned long aAdrr=0x400a3e5d;
    sendZigBeeMsg(aCmd,aAdrr);
  }
  else if(_CmdReceived==18)
  {
    x10ex.sendCmd('A', 8, CMD_ON, 1);
  }
  else if(_CmdReceived==19)
  {
    x10ex.sendCmd('A', 8, CMD_OFF, 1);
  }
  else if(_CmdReceived==20)
  {
    unsigned int aCmd=9;
    unsigned long aAdrr=0x400a3e5d;
    sendZigBeeMsg(aCmd,aAdrr);
  }
  else if(_CmdReceived==21)
  {
    unsigned int aCmd=2;
    //unsigned long aAdrr=0x406b7b64;
    unsigned long aAdrr=0x408CCB53;
    sendZigBeeMsg(aCmd,aAdrr);
  }
  else if(_CmdReceived==22)
  {
    unsigned int aCmd=3;
    //unsigned long aAdrr=0x406b7b64;
    unsigned long aAdrr=0x408CCB53;
    sendZigBeeMsg(aCmd,aAdrr);
  }
  else if(_CmdReceived==23)
  {
    unsigned int aCmd=1;
    //unsigned long aAdrr=0x406b7b64;
    unsigned long aAdrr=0x408CCB53;
    sendZigBeeMsg(aCmd,aAdrr);
  }
  else if(_CmdReceived==24)
  {
    unsigned int aCmd=4;
    //unsigned long aAdrr=0x406b7b64;
    unsigned long aAdrr=0x408CCB53;
    sendZigBeeMsg(aCmd,aAdrr);
  }
  if (_DataToSend!=0)
  {
    delay(10);
    Serial.println(_DataToSend);
  }

}

void printX10Message(const char type[], char house, byte unit, byte command, byte extData, byte extCommand, int remainingBits)
{
  printX10TypeHouseUnit(type, house, unit, command);
  // Ignore non X10 commands like the CMD_ADDRESS command used by the IR library
  if(command <= 0xF)
  {
    Serial.print(command, HEX);
    if(extCommand || (extData && (command == CMD_STATUS_ON || command == CMD_STATUS_OFF)))
    {
      printX10ByteAsHex(extCommand);
      printX10ByteAsHex(extCommand == EXC_PRE_SET_DIM ? extData & B111111 : extData);
    }
  }
  else
  {
    Serial.print("_");
  }
  Serial.println();
}

void printX10TypeHouseUnit(const char type[], char house, byte unit, byte command)
{
  Serial.print(type);
  Serial.print(house);
  if(
    unit &&
    unit != DATA_UNKNOWN/* &&
    command != CMD_ALL_UNITS_OFF &&
    command != CMD_ALL_LIGHTS_ON &&
    command != CMD_ALL_LIGHTS_OFF &&
    command != CMD_HAIL_REQUEST*/)
  {
    Serial.print(unit - 1, HEX);
  }
  else
  {
    Serial.print("_");
  }
}

void printX10ByteAsHex(byte data)
{
  Serial.print("x");
  if(data <= 0xF) { Serial.print("0"); }
  Serial.print(data, HEX);
}

byte charHexToDecimal(byte input)
{
  // 0123456789  =>  0-15
  if(input >= 0x30 && input <= 0x39) input -= 0x30;
  // ABCDEF  =>  10-15
  else if(input >= 0x41 && input <= 0x46) input -= 0x37;
  // Return converted byte
  return input;
}

// Process messages received from X10 modules over the power line
void powerLineEvent(char house, byte unit, byte command, byte extData, byte extCommand, byte remainingBits)
{
  printX10Message(POWER_LINE_MSG, house, unit, command, extData, extCommand, remainingBits);
}

// Process serial data messages received from computer over USB, Bluetooth, e.g.
//
// Serial messages are 3 or 9 bytes long. Use hex 0-F to address units and send commands.
// Bytes must be sent within one second (defined threshold) from the first to the last
// Below are some examples:
//
// Standard Messages examples:
// A12 (House=A, Unit=2, Command=On)
// AB3 (House=A, Unit=12, Command=Off)
// A_5 (House=A, Unit=N/A, Command=Bright)
// |||
// ||+-- Command 0-F or _  Example: 2 = On, 7 = ExtendedCode and _ = No Command
// |+--- Unit 0-F or _     Example: 0 = Unit 1, F = Unit 16 and _ = No unit
// +---- House code A-P    Example: A = House A and P = House P :)
//
// Extended Message examples:
// A37x31x21 (House=A, Unit=4, Command=ExtendedCode, Extended Command=PreSetDim, Extended Data=33)
// B87x01x0D (House=B, Unit=9, Command=ExtendedCode, Extended Command=ShutterOpen, Extended Data=13)
//     |/ |/
//     |  +-- Extended Data byte in hex     Example: 01 = 1%, 1F = 50% and 3E = 100% brightness (range is decimal 0-62)
//     +----- Extended Command byte in hex  Example: 31 = PreSetDim, for more examples check the X10 ExtendedCode spec.
//
// Scenario Execute examples:
// S03 (Execute scenario 3)
// S14 (Execute scenario 20)
// ||/
// |+--- Scenario byte in hex (Hex: 00-FF, Dec: 0-255)
// +---- Scenario Execute Character
//
// Request Module State examples:
// R** (Request buffered state of all modules)
// RG* (Request buffered state of modules using house code G)
// RA2 (Request buffered state of module A3)
// |||
// ||+-- Unit 0-F or *        Example: 0 = Unit 1, A = Unit 10 and * = All units
// |+--- House code A-P or *  Example: A = House A, P = House P and * = All house codes
// +---- Request Module State Character
//
// Wipe Module State examples:
// RW* (Wipe state data for all modules)
// RWB (Wipe state data for all modules using house code B)
// |||
// ||+-- House code A-P or *  Example: A = House A, P = House P and * = All house codes
// |+--- Wipe Module State Character
// +---- Request Module State Character
//

//This is useless for me and leqd to issue when I use Xbee so i comment it
//void serialEvent()
//{
//  // Read 3 bytes from serial buffer
//  if(Serial.available() >= 3)
//  {
//    byte byte1 = toupper(Serial.read());
//    byte byte2 = toupper(Serial.read());
//    byte byte3 = toupper(Serial.read());
//    if(process3BMessage(SERIAL_DATA_MSG, byte1, byte2, byte3))
//    {
//      // Return error message if message sent to X10ex was not buffered successfully
//      Serial.println(POWER_LINE_BUFFER_ERROR);
//    }
//    sdReceived = 0;
//  }
//  // If partial message was received
//  if(Serial.available() && Serial.available() < 3)
//  {
//    // Store received time
//    if(!sdReceived)
//    {
//      sdReceived = millis();
//    }
//    // Clear message if all bytes were not received within threshold
//    else if(sdReceived > millis() || millis() - sdReceived > SERIAL_DATA_THRESHOLD)
//    {
//      bmHouse = 0;
//      bmExtCommand = 0;
//      sdReceived = 0;
//      Serial.println(SERIAL_DATA_TIMEOUT);
//      // Clear serial input buffer
//      while(Serial.read() != -1);
//    }
//  }
//}

//This is useless for me and leqd to issue when I use Xbee so i comment it
// Processes and executes 3 byte serial and ethernet messages.
//bool process3BMessage(const char type[], byte byte1, byte byte2, byte byte3)
//{
//  bool x10exBufferError = 0;
//  // Convert byte2 from hex to decimal unless command is request module state
//  if(byte1 != 'R') byte2 = charHexToDecimal(byte2);
//  // Convert byte3 from hex to decimal unless command is wipe module state
//  if(byte1 != 'R' || byte2 != 'W') byte3 = charHexToDecimal(byte3);
//  // Check if standard message was received (byte1 = House, byte2 = Unit, byte3 = Command)
//  if(byte1 >= 'A' && byte1 <= 'P' && (byte2 <= 0xF || byte2 == '_') && (byte3 <= 0xF || byte3 == '_') && (byte2 != '_' || byte3 != '_'))
//  {
//    // Store first 3 bytes of message to make it possible to process 9 byte serial messages
//    bmHouse = byte1;
//    bmUnit = byte2 == '_' ? 0 : byte2 + 1;
//    bmCommand = byte3 == '_' ? CMD_STATUS_REQUEST : byte3;
//    bmExtCommand = 0;
//    // Send standard message if command type is not extended
//    if(bmCommand != CMD_EXTENDED_CODE && bmCommand != CMD_EXTENDED_DATA)
//    {
//      printX10Message(type, bmHouse, bmUnit, byte3, 0, 0, 8 * Serial.available());
//      x10exBufferError = x10ex.sendCmd(bmHouse, bmUnit, bmCommand, bmCommand == CMD_BRIGHT || bmCommand == CMD_DIM ? 2 : 1);
//      bmHouse = 0;
//    }
//  }
//  // Check if extended message was received (byte1 = Hex Seperator, byte2 = Hex 1, byte3 = Hex 2)
//  else if(byte1 == 'X' && bmHouse)
//  {
//    byte data = byte2 * 16 + byte3;
//    // No extended command set, assume that we are receiving command
//    if(!bmExtCommand)
//    {
//      bmExtCommand = data;
//    }
//    // Extended command set, we must be receiving extended data
//    else
//    {
//      printX10Message(type, bmHouse, bmUnit, bmCommand, data, bmExtCommand, 8 * Serial.available());
//      x10exBufferError = x10ex.sendExt(bmHouse, bmUnit, bmCommand, data, bmExtCommand, 1);
//      bmHouse = 0;
//    }
//  }
//  // Check if scenario execute command was received (byte1 = Scenario Character, byte2 = Hex 1, byte3 = Hex 2)
//  else if(byte1 == 'S')
//  {
//    byte scenario = byte2 * 16 + byte3;
//    Serial.print(type);
//    Serial.print("S");
//    if(scenario <= 0xF) { Serial.print("0"); }
//    Serial.println(scenario, HEX);
//    handleSdScenario(scenario);
//  }
//  // Check if request module state command was received (byte1 = Request State Character, byte2 = House, byte3 = Unit)
//  else if(byte1 == 'R' && ((byte2 >= 'A' && byte2 <= 'P') || byte2 == '*'))
//  {
//    Serial.print(type);
//    Serial.print("R");
//    Serial.print(byte2);
//    // All modules
//    if(byte2 == '*')
//    {
//      Serial.println('*');
//      for(short i = 0; i < 256; i++)
//      {
//        sdPrintModuleState((i >> 4) + 0x41, i & 0xF);
//      }
//    }
//    else
//    {
//      if(byte3 <= 0xF)
//      {
//        Serial.println(byte3, HEX);
//        sdPrintModuleState(byte2, byte3);
//      }
//      // All units using specified house code
//      else
//      {
//        Serial.println('*');
//        for(byte i = 0; i < 16; i++)
//        {
//          sdPrintModuleState(byte2, i);
//        }
//      }
//    }
//  }
//  // Check if request wipe module state command was received (byte1 = Request State Character, byte2 = Wipe Character, byte3 = House)
//  else if(byte1 == 'R' && byte2 == 'W' && ((byte3 >= 'A' && byte3 <= 'P') || byte3 == '*'))
//  {
//    Serial.print(type);
//    Serial.print("RW");
//    Serial.println((char)byte3);
//    x10ex.wipeModuleState(byte3);
//    Serial.print(MODULE_STATE_MSG);
//    Serial.print(byte3 >= 'A' && byte3 <= 'P' ? (char)byte3 : '*');
//    Serial.println("__");
//  }
//  // Unknown command/data
//  else
//  {
//    Serial.print(type);
//    Serial.println(MSG_DATA_ERROR);
//  }
//  return x10exBufferError;
//}

//This methode was only needed by the one I comment for Xbee interference so i comment it too
//void sdPrintModuleState(char house, byte unit)
//{
//  unit++;
//  X10state state = x10ex.getModuleState(house, unit);
//  if(state.isSeen)
//  {
//    printX10Message(
//      MODULE_STATE_MSG, house, unit,
//      state.isKnown ? state.isOn ? CMD_STATUS_ON : CMD_STATUS_OFF : DATA_UNKNOWN,
//      state.data,
//      0, 0);
//  }
//}
