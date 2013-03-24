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

#endif