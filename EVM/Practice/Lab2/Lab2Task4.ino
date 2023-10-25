#include <TroykaIMU.h>
#include <TroykaMeteoSensor.h>

Barometer barometer;
TroykaMeteoSensor meteoSensor;

void setup() {
  Serial.begin(115200);
  while(!Serial) {
  }
  Serial.println("Инициализация последовательного порта в порядке!");
  meteoSensor.begin();
  Serial.println("Метеосенсор инициализируется...");
  delay(1000);
  Serial.begin(9600);
    // Выводим сообщение о начале инициализации
  Serial.println("Начало инициализации...");
    // Инициализируем барометр
  barometer.begin();
    // Выводим сообщение об удачной инициализации
  Serial.println("Инициализация завершена!");
}

void loop() {
  int stateSensor = meteoSensor.read();
  float pressureMillimetersHg = barometer.readPressureMillimetersHg();
  float temperature = barometer.readTemperatureC();
  switch (stateSensor) {
    case SHT_OK:
      Serial.println("Сенсор подключен");
      Serial.print("Температура = ");
      Serial.print(meteoSensor.getTemperatureC());
      Serial.println(" C \t");
      Serial.print("Влажность = ");
      Serial.print(meteoSensor.getHumidity());
      Serial.println(" %\r\n");
      Serial.print(pressureMillimetersHg);
      Serial.print(" mmHg\t");
      Serial.print("Температура: ");
      Serial.print(temperature);
      Serial.println(" C");
      break;
    case SHT_ERROR_DATA:
      Serial.println("Ошибка данных или датчик не подключен!");
      break; 
    case SHT_ERROR_CHECKSUM:
      Serial.println("Ошибка контрольной суммы!");
      break;
  }
  delay(1000);
}