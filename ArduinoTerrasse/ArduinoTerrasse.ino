//Xbee library
#include <XBee.h>
//Deipara library
#include <Deipara.h>
// This library contains functions to set various low-power states for the ATmega328
#include <avr/sleep.h>
//RHT03 library
#include <DHT22.h>


// This variable is made volatile because it is changed inside an interrupt function
// Keep track of how many sleep cycles have been completed.
volatile int sleep_count = 0; 
// 75 loop needed since ze sleep for 8s and want to wait 10 minutes
//const int sleep_total = 60; 
const int sleep_total = 60; 

//pin
const int _InPinDht22 = 6;
const int _OutPowerLightSensor = 7;
const int _OutXbeePower1 = 8;
const int _OutXbeePower2 = 9;
const int _OutPowerDHT22 = 10;
const int _InLightPin = 4;



//Xbee objects
//create Xbee object to control a Xbee
XBee _Xbee = XBee(); 
//Create reusable response objects for responses we expect to handle
ZBRxResponse _ZbRxResp = ZBRxResponse();
//Setup a DHT22 instance
DHT22 _Dht22(_InPinDht22); //Setup a DHT22 instance 
//Global variable used in the program
int _CmdReceived = 0;
int _DataToSend = 0;

void goToSleep()   
{
  // The ATmega328 has five different sleep states.
  // See the ATmega 328 datasheet for more information.
  // SLEEP_MODE_IDLE -the least power savings 
  // SLEEP_MODE_ADC
  // SLEEP_MODE_PWR_SAVE
  // SLEEP_MODE_STANDBY
  // SLEEP_MODE_PWR_DOWN -the most power savings
  // I am using the deepest sleep mode from which a
  // watchdog timer interrupt can wake the ATMega328
  //digitalWrite(_OutDebugLed, HIGH);

  set_sleep_mode(SLEEP_MODE_PWR_DOWN); // Set sleep mode.
  sleep_enable(); // Enable sleep mode.
  sleep_mode(); // Enter sleep mode.
  // After waking from watchdog interrupt the code continues
  // to execute from this point.

  sleep_disable(); // Disable sleep mode after waking.
  //digitalWrite(_OutDebugLed, LOW);                   
}

void watchdogOn() 
{ 
  // Clear the reset flag, the WDRF bit (bit 3) of MCUSR.
  MCUSR = MCUSR & B11110111;
  
  // Set the WDCE bit (bit 4) and the WDE bit (bit 3) 
  // of WDTCSR. The WDCE bit must be set in order to 
  // change WDE or the watchdog prescalers. Setting the 
  // WDCE bit will allow updtaes to the prescalers and 
  // WDE for 4 clock cycles then it will be reset by 
  // hardware.
  WDTCSR = WDTCSR | B00011000; 

  // Set the watchdog timeout prescaler value to 1024 K 
  // which will yeild a time-out interval of about 8.0 s.
  WDTCSR = B00100001;

  // Enable the watchdog timer interupt.
  WDTCSR = WDTCSR | B01000000;
  MCUSR = MCUSR & B11110111;
}

ISR(WDT_vect)
{
  sleep_count ++; // keep track of how many sleep cycles have been completed.
}

void setup(void) 
{
  pinMode(_OutPowerLightSensor, OUTPUT);
  pinMode(_OutPowerDHT22, OUTPUT);
  pinMode(_OutXbeePower1, OUTPUT);
  pinMode(_OutXbeePower2, OUTPUT);
  pinMode(_InLightPin, INPUT);
  
  digitalWrite(_OutPowerLightSensor, LOW);
  digitalWrite(_OutPowerDHT22, LOW);
  digitalWrite(_OutXbeePower1, LOW);
  digitalWrite(_OutXbeePower2, LOW);

  // start serial
  _Xbee.begin(XBEE_SPEED); 
  Serial.begin(XBEE_SPEED);
  
  delay(500);
  
  watchdogOn(); // Turn on the watch dog timer.
}

void loop(void) 
{
  goToSleep(); // ATmega328 goes to sleep for about 8 seconds and continues to execute code when it wakes up

  if (sleep_count > sleep_total) 
    {
    sleep_count = 0;
    //First we power the Xbee so it has time to reach the network and the other captor
    digitalWrite(_OutXbeePower1, HIGH);
    digitalWrite(_OutXbeePower2, HIGH);
    digitalWrite(_OutPowerDHT22, HIGH);
    digitalWrite(_OutPowerLightSensor, HIGH);
    //Then wait 0.5s to be ready 
    delay(1000);
    //we read the light sensor value
    unsigned int aLightValue = analogRead(_InLightPin);
    //we turn it off
    digitalWrite(_OutPowerLightSensor, LOW);
    delay(3000);
    //Then read T
    DHT22_ERROR_t errorCode;
    int aTempValue=0;
    int aHumidityValue=0;
    errorCode = _Dht22.readData();
    
    switch(errorCode)
    {
    case DHT_ERROR_NONE:
        aTempValue=_Dht22.getTemperatureCAsInt();
        aHumidityValue=_Dht22.getHumidityAsInt();
        //Serial.print("data read OK ");
        //Serial.print("aTempValue");
        //Serial.print(aTempValue);
        //Serial.print("aHumidityValue");
        //Serial.print(aHumidityValue);
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
    
    //digitalWrite(_OutPowerDHT22, LOW);

    //we wait few second to be sure Xbee reach the network
    delay(2000);
    //we send the info
    sendZigBeeMsg2(_Xbee,36,aLightValue,COORD_ADDR);
    delay(250);
    //Serial.println("aTempValue2 : ");
    //Serial.println(aTempValue);
    sendZigBeeMsg2(_Xbee,37,aTempValue,COORD_ADDR);
    delay(250);
    sendZigBeeMsg2(_Xbee,38,aHumidityValue,COORD_ADDR);
    //we turn off the xbee module
    digitalWrite(_OutXbeePower1, LOW);
    digitalWrite(_OutXbeePower2, LOW);
  }
}
