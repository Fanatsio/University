// Реализовать управление сервоприводом подключенным к пину D0. Задача угла поворота сервопривода производиться поворотом потенциометра подключенного к пину A0
#include <Servo.h>

Servo myservo;

int potVal;

void setup() 
{
  myservo.attach(D0, 600, 2600);
}

void loop() 
{
  potVal = analogRead(A0);
  potVal = map(potVal, 0, 4095, 0, 180);
  myservo.write(potVal);
  delay(25);
}