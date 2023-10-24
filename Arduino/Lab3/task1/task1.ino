#include <WiFi.h>
#include <string>
 
String ssid = "ASOIU";
String password = "kaf.asoiu.48";
 
void setup() {
  Serial.begin();
  while (!Serial) continue;

  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("Wifi shield not present");
    while (true) continue;;
  }

  WiFi.begin(ssid.c_str(), password.c_str());
  Serial.print("WiFi connected. Local IP = ");
  Serial.println(WiFi.localIP());
}
 
void loop() {
  if (!Serial.available()) return;

  if (WiFi.status() != WL_CONNECTED) WiFi.begin(ssid.c_str(), password.c_str());

  String host = String(Serial.readString().c_str());
  host.trim();

  if (!host.length()) return;
  
  int pingResult = WiFi.ping(host.c_str());

  Serial.print("Ping Host: ");
  Serial.print(host.c_str());
  Serial.print(pingResult >= 0 ? " succesful. RTT = " : " failed. Error Code = ");
  Serial.println(pingResult);
}