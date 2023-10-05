// Реализовать задание из пункта №3, но с использованием аппаратного прерывания при нажатии на кнопку вместо использования функции digitalRead
const int ledPins[] = {D0, D1, D2};
const int buttonPin = D3;
int valitale currentLED = 0;

void setup() {
  for (int i = 0; i < 3; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
  pinMode(buttonPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(buttonPin), handleButtonPress, FALLING);
}

void loop() {
  // Пустой цикл, светодиоды управляются через прерывание
}

void handleButtonPress() {
  digitalWrite(ledPins[currentLED], LOW);
  currentLED = (currentLED + 1) % 3;
  digitalWrite(ledPins[currentLED], HIGH);
}

