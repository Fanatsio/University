#include <WiFi.h>
#include <string>

const char* ssid = "ASOIU";
const char* password = "kaf.asoiu.48";

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    delay(100);
  }

  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    while (true) {
      delay(1000);
    }
  }

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.print("WiFi connected. Local IP = ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (Serial.available() > 0) {
    String host = Serial.readStringUntil('\n');
    host.trim();

    if (!host.isEmpty()) {
      int pingResult = WiFi.ping(host);

      Serial.print("Ping Host: ");
      Serial.print(host);
      Serial.print(pingResult >= 0 ? " successful. RTT = " : " failed. Error Code = ");
      Serial.println(pingResult);
    }
  }
}
