// Светодиод подключенный к пину D0 мигает каждые 5 секунд
void setup() {
  pinMode(D0, OUTPUT);
}

void loop() {
  digitalWrite(D0, HIGH);
  delay(5000);
  digitalWrite(D0, LOW);
  delay(5000);
}
