#include <WiFi.h>
#include <string>
#include <Wire.h>
#include <TroykaMeteoSensor.h>
#include <TroykaIMU.h>

String ssid = "ASOIU";
String password = "kaf.asoiu.48";

WiFiServer server(80);
TroykaMeteoSensor meteoSensor;
Barometer barometer;

void sendHtmlTemplate(WiFiClient client);

void setup() {
  Serial.begin();
  Wire.begin();
  meteoSensor.begin();
  barometer.begin();
  WiFi.mode(WIFI_STA);
  WiFi.setHostname("PicoW2");
  WiFi.begin(ssid.c_str(), password.c.str());

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }

  server.begin();
}

void sendHtmlTemplate(WiFiClient client) {
  delay(50);
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println();
  client.println("<html>");
  client.println("<head><title>Weather and Barometer Data</title></head>");
  client.println("<body>");

  if (meteoSensor.read() != SHT_OK) {
    client.println("<h1>Data error or sensor not connected</h1>");
  } else {
    client.println("<h1>Meteo Sensor Data</h1>");
    client.println("<p>Temperature: " + String(meteoSensor.getTemperatureC()) + "&deg;C</p>");
    client.println("<p>Humidity: " + String(meteoSensor.getHumidity()) + "%</p>");
  }

  client.println("<h1>Barometer Data</h1>");
  client.println("<p>Pressure: " + String(barometer.readPressureMillimetersHg()) + " mmHg</p>");
  client.println("<p>Altitude: " + String(barometer.readAltitude()) + " meters</p>");
  client.println("<p>Temperature: " + String(barometer.readTemperatureC()) + "&deg;C</p>");

  client.println("</body>");
  client.println("</html>");

  client.flush();
}

void loop() {
  WiFiClient client = server.available();
  if (!client) return;

  while (!client.available()) ;

  String req = client.readStringUntil('\n');
  sendHtmlTemplate(client);
}
