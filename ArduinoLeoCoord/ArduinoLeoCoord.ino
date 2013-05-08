//Libraries definitions
//Xbee library
#include <XBee.h>
//Timer library
#include <MsTimer2.h>
//X10 library
#include <X10ex.h>
//Deipara library
#include <Deipara.h>
//RHT03 library
#include <DHT22.h>

#define POWER_LINE_MSG "PL:"
#define POWER_LINE_BUFFER_ERROR "PL:_ExBuffer"
#define SERIAL_DATA_MSG "SD:"
#define SERIAL_DATA_THRESHOLD 1000
#define SERIAL_DATA_TIMEOUT "SD:_ExTimOut"
#define MODULE_STATE_MSG "MS:"
#define MSG_DATA_ERROR "_ExSyntax"

//Define the pin number
const int _InPinIrDetector = 8;
const int _InPinButtonOn = 4;
const int _InPinDht22 = 7;
//Define other consts

XBee _Xbee = XBee(); // create Xbee object to control a Xbee
ZBRxResponse _ZbRxResp = ZBRxResponse(); //Create reusable response objects for responses we expect to handle
// Fields used for serial and byte message reception
unsigned long sdReceived;
char bmHouse;
byte bmUnit;
byte bmCommand;
byte bmExtCommand;
int _CmdReceived = 0;
bool _TimerExpire = true;
int _UsbCmdReceived = 0;
int _DataToSend = 0;
int _SenderId = 0;
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
DHT22 _Dht22(_InPinDht22); //Setup a DHT22 instance

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

void InterruptTimer2() 
{
  _TimerExpire= true;
  MsTimer2::stop();
}

void setup()
{
  //defined input button
  pinMode(_InPinButtonOn,INPUT);
  pinMode(_InPinIrDetector,INPUT);
  
  //Active resistor as pull up
  digitalWrite(_InPinButtonOn,HIGH);

  // start serial
  _Xbee.begin(XBEE_SPEED);
  Serial.begin(XBEE_SPEED);
  // Start the Power Line Communication library
  x10ex.begin();
  MsTimer2::set(30000, InterruptTimer2);
}

void processCommandReceivedFromUsb(int iCommande) 
{
}

void loop()
{
  _Xbee.readPacket();
  //Reset command to 0
  _CmdReceived = 0;
  _UsbCmdReceived = 0;
  _DataToSend = 0;
  _SenderId = 0;
  uint8_t aPayload[] = { 0, 0 , 0};

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
	  if(_ZbRxResp.getDataLength()>2)
	  {
	  aPayload[0]=_ZbRxResp.getData(0);
	  aPayload[1]=_ZbRxResp.getData(1);
	  aPayload[2]=_ZbRxResp.getData(2);
      _SenderId=aPayload[0];
	  _DataToSend=word(_ZbRxResp.getData(2),_ZbRxResp.getData(1));
	  }
      
    }  
  }
  
  // check for incoming serial data:
  if (Serial.available() > 0) 
  {
    // read incoming serial data:
    _UsbCmdReceived = Serial.read();
    _CmdReceived = _UsbCmdReceived;

  }
  
  int aInputDigitalValue = digitalRead(_InPinIrDetector);
  if ((aInputDigitalValue == HIGH)&&(_TimerExpire == true))
  {
  _TimerExpire = false;
    _CmdReceived=45;
    _DataToSend=444;
    _SenderId=2;
    MsTimer2::start(); // active Timer 2 
  }
 
 //Read button status
  aInputDigitalValue = digitalRead(_InPinButtonOn);
  //Reset the counter if button is press
  if ((aInputDigitalValue == LOW))
  {
    _CmdReceived=20;
    //flashPin(_OutPinLedTest, 3, 200);
    //x10ex.sendCmd('A', 5, CMD_OFF, 1);
    //x10ex.sendExtDim('A', 5, 40, 0, 1);
    //x10ex.sendExt('A',  5, CMD_EXTENDED_CODE,5, EXC_PRE_SET_DIM,1);
    //KO x10ex.sendExtDim('A', 5, 40, EXC_DIM_TIME_30, 1);
    //KO x10ex.sendExtDim('A', 5, 40, EXC_DIM_TIME_60, 1);
    //x10ex.sendExtDim('A', 5, 40, EXC_DIM_TIME_300, 1);
    //x10ex.sendCmd('A', 5, CMD_DIM, 1);
    delay(1000);
    //OK x10ex.sendCmd('A', 5, CMD_BRIGHT, 1);
    
  }
  
  //Process the command
  //Test des commandes pour le X10
  if(_CmdReceived==5) //Charles lumiere principlae
  {
    x10ex.sendCmd('A', 4, CMD_ON, 1);
  }
  else if(_CmdReceived==6) //Charles lumiere principlae
  {
    x10ex.sendCmd('A', 4, CMD_OFF, 1);
  }
  else if(_CmdReceived==7) //Volet charles
  {
    x10ex.sendCmd('A', 5, CMD_BRIGHT, 1);
  }
  else if(_CmdReceived==8) //Volet charles
  {
    x10ex.sendCmd('A', 5, CMD_DIM, 1);
  }
  else if(_CmdReceived==9) //Volet Salon
  {
    x10ex.sendCmd('A', 7, CMD_BRIGHT, 1);
  }
  else if(_CmdReceived==10) //Volet Salon
  {
    x10ex.sendCmd('A', 7, CMD_DIM, 1);
  }
  else if(_CmdReceived==11) //Charles lumiere secondaire
  {
    x10ex.sendCmd('A', 13, CMD_ON, 1);
  }
  else if(_CmdReceived==12) //Charles lumiere secondaire
  {
    x10ex.sendCmd('A', 13, CMD_OFF, 1);
  }
  else if(_CmdReceived==13) //Lampe halogene salon
  {
    x10ex.sendCmd('A', 6, CMD_ON, 1);
  }
  else if(_CmdReceived==14) //Lampe halogene salon
  {
    x10ex.sendCmd('A', 6, CMD_OFF, 1);
  }
  else if(_CmdReceived==42) //Allumer le chauffage de la SDB
  {
    x10ex.sendCmd('A', 8, CMD_ON, 1); 
  }
  else if(_CmdReceived==43) //Eteindre le chauffage de la SDB
  {
    x10ex.sendCmd('A', 8, CMD_OFF, 1); 
  }
  //commande pour le coord lui meme
  else if((_CmdReceived==15)||(_CmdReceived==16)) //temperature
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
      if (_CmdReceived==15)
      {
        _DataToSend=_Dht22.getTemperatureCAsInt();
        _SenderId=15;
      }
      else if(_CmdReceived==16)
      {
        _DataToSend=_Dht22.getHumidityAsInt();
        _SenderId=16;
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
  //Debut des commandes pour ENTREE
  else if((_CmdReceived==30)||(_CmdReceived==31)||(_CmdReceived==32)||(_CmdReceived==33)||(_CmdReceived==34)||(_CmdReceived==35)||(_CmdReceived==36)||(_CmdReceived==37)||(_CmdReceived==38))
  {
    sendZigBeeMsg(_Xbee,_CmdReceived,ENTREE_ADDR);
  }
  //Debut des commandes TERRASSE
  else if((_CmdReceived==39)||(_CmdReceived==40)||(_CmdReceived==46)||(_CmdReceived==47))
  {
    sendZigBeeMsg(_Xbee,_CmdReceived,TERRASSE_ADDR);
  }
  else if((_CmdReceived==3)||(_CmdReceived==4)||(_CmdReceived==18)||(_CmdReceived==19))
  {
    sendZigBeeMsg(_Xbee,_CmdReceived,SALON_ADDR);
  }
  else if((_CmdReceived==20)||(_CmdReceived==21)||(_CmdReceived==36))
  {
    sendZigBeeMsg(_Xbee,_CmdReceived,TERRASSE_ADDR2);
  }
  

  
  //Si on doit renvoyer qq chose sur le port USB (une reponse d un capteur)
  if (_DataToSend!=0)
  {
    delay(10);
	if(_SenderId != 0)
	{
	Serial.print("ID:");
	Serial.print(_SenderId);
	Serial.print("_OUTPUT:");
	Serial.println(_DataToSend);
	}
	else
	{
    Serial.println(_DataToSend);
	}
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
