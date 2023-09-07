void setup() {
  pinMode(D1, OUTPUT);
}

void loop() {
  int buttonState = digitalRead(D1);

  if(buttonState == HIGH) {
      digitalWrite(D1, HIGH);
  } else {
      digitalWrite(D1, LOW);
  }
}
