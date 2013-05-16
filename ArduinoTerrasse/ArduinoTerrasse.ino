//Xbee library
#include <XBee.h>
//Deipara library
#include <Deipara.h>
// This library contains functions to set various low-power states for the ATmega328
#include <avr/sleep.h>


// This variable is made volatile because it is changed inside an interrupt function
// Keep track of how many sleep cycles have been completed.
volatile int sleep_count = 0; 
// 75 loop needed since ze sleep for 8s and want to wait 10 minutes
//const int sleep_total = 75; 
const int sleep_total = 40; 

//pin
const int _OutXbeeWakeUp = 7;
const int _OutDebugLed = 8;
const int _OutXbeePower = 9;
const int _InLightPin = 4;


//Xbee objects
//create Xbee object to control a Xbee
XBee _Xbee = XBee(); 
//Create reusable response objects for responses we expect to handle
ZBRxResponse _ZbRxResp = ZBRxResponse(); 
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
  pinMode(_OutDebugLed, OUTPUT);
  pinMode(_OutXbeePower, OUTPUT);
  pinMode(_OutXbeeWakeUp, OUTPUT);
  pinMode(_InLightPin, INPUT);
  
  digitalWrite(_OutXbeeWakeUp, HIGH);
  digitalWrite(_OutXbeePower, HIGH);
  digitalWrite(_OutDebugLed, HIGH);

  // start serial
  _Xbee.begin(XBEE_SPEED); 
  Serial.begin(XBEE_SPEED);
  
  delay(1000);
  
  watchdogOn(); // Turn on the watch dog timer.
}

void loop(void) 
{
  goToSleep(); // ATmega328 goes to sleep for about 8 seconds and continues to execute code when it wakes up

  if (sleep_count > sleep_total) 
    {
    sleep_count = 0;
    // CODE TO BE EXECUTED PERIODICALLY
    //digitalWrite(_OutDebugLed, HIGH);
    digitalWrite(_OutDebugLed, HIGH);
    digitalWrite(_OutXbeePower, HIGH);
    digitalWrite(_OutXbeeWakeUp, HIGH);
    delay(10000);
    unsigned int val = analogRead(_InLightPin);    // read the input pin
    sendZigBeeMsg2(_Xbee,36,val,COORD_ADDR);
    digitalWrite(_OutDebugLed, LOW);
    digitalWrite(_OutXbeePower, LOW);
    digitalWrite(_OutXbeeWakeUp, LOW);
  }
}