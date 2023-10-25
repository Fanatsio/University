// Светодиод подключенный к пину D0 загорается при нажатии на кнопку подключенную к пину D1
void setup() {
  pinMode(D0, OUTPUT);
  pinMode(D1, INPUT);
}

void loop() {
  digitalWrite(D0, !digitalRead(D1));
}
