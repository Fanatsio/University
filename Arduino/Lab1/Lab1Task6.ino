// Светодиод подключенный к пину D0 меняет яркость при повороте потенциометра подключенного к пину A0 с частотой 120Гц (ШИМ-сигнал)
int sensorValue = 0;

void setup() {
  analogWriteFreq(120);
}

void loop() {
  sensorValue = analogRead(A0);
  analogWrite(D0, map(sensorValue, 0, 4095, 0, 255));
}