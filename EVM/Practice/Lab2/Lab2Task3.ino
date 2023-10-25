#include <SPI.h>
#include <AmperkaFET.h>
#include <sstream>
#include <iostream>

FET mosfet(D17, 2);
 
void setup() {
  mosfet.begin();
}
 
void loop() {
  if (Serial.available())
  {
    std::stringstream ss;
    ss << Serial.readString().c_str();
    uint32_t d, e, i;
    int val;
    ss >> d >> e >> i;
    if (i > 0)
      val = HIGH;
    else
      val = LOW;
    if (d > 1)
      d = 255;
    if (e > 7)
      e = 255;
    mosfet.digitalWrite(d, e, val);
  }
}