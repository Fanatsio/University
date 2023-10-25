// Реализовать задание из пункта №3, но с использованием встроенного аппаратного таймера вместо нажатия на кнопку
const int timerInterval = 1000; 
struct repeating_timer timer;

volatile int i = 0;

bool timerISR(struct repeating_timer *timer) {
  digitalWrite(D0, LOW);
  digitalWrite(D1, LOW);
  digitalWrite(D2, LOW);
  i = (i + 1) % 3;
  digitalWrite(i, HIGH);
  return true;
}

void setup() {
  pinMode(D0, OUTPUT);
  pinMode(D1, OUTPUT);
  pinMode(D2, OUTPUT);

  add_repeating_timer_ms(timerInterval, timerISR, nullptr , &timer);
}

void loop() {
  
}