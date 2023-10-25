// Силовой ключ и вентилятор (4-pin) подключены к пинам D0 и D1 управляются ШИМ на частоте 25КГц. Скважность ШИМ регулируется поворотом потенциометра подключенного к пину A0
void setup() {
    analogWriteFreq(25000);
}
void loop() {
    int angle = map(analogRead(A0), 0, 4095, 0, 255);
    analogWrite(D0, angle);
    analogWrite(D1, angle);
}