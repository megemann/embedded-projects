#include <WiFi.h>
#include <PubSubClient.h>
#include <IRremote.hpp>  // Arduino-IRremote v4.x

// ---------- WiFi ----------
const char* SSID = "OP508-2G";
const char* PASS = "LifeSelf0200";

// ---------- MQTT ----------
const char* BROKER   = "10.25.8.130";   // change to your broker IP
const uint16_t PORT  = 1883;
const char* CLIENTID = "esp32-ir-1";
const char* SUB_TOPIC = "austin/ir/cmd";
const char* PUB_TOPIC = "austin/ir/status";

// ---------- IR ----------
#ifndef IR_SEND_PIN
#define IR_SEND_PIN 4      // your output GPIO
#endif
static const uint16_t NEC_ADDRESS = 0x00;
static const uint8_t  TEST_COMMAND = 0x40;

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

// Forward decls
void connectWiFi();
void connectMQTT();
void sendNECCommand(int pin, uint16_t address, uint8_t command);

void onMqttMsg(char* topic, byte* payload, unsigned int length) {
  // Minimal: any payload triggers one NEC send with fixed addr/cmd
  Serial.print("[MQTT] ");
  Serial.print(topic);
  Serial.print(" => ");
  for (unsigned int i = 0; i < length; i++) Serial.print((char)payload[i]);
  Serial.println();

  sendNECCommand(IR_SEND_PIN, NEC_ADDRESS, TEST_COMMAND);
  mqtt.publish(PUB_TOPIC, "sent");
}

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("ESP32 NEC IR + MQTT minimal");

  // IR sender init
  IrSender.begin(IR_SEND_PIN);

  connectWiFi();

  mqtt.setServer(BROKER, PORT);
  mqtt.setCallback(onMqttMsg);
  connectMQTT();

  // Announce online
  mqtt.publish(PUB_TOPIC, "online");
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) connectWiFi();
  if (!mqtt.connected()) connectMQTT();
  mqtt.loop();

  // Periodic RSSI
  static unsigned long last = 0;
  if (millis() - last > 10000) {
    last = millis();
    char buf[32];
    snprintf(buf, sizeof(buf), "rssi=%d", WiFi.RSSI());
    mqtt.publish(PUB_TOPIC, buf);
  }
}

void connectWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;
  Serial.printf("WiFi connecting to %s\n", SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(400);
    Serial.print(".");
  }
  Serial.printf("\nWiFi OK. IP: %s\n", WiFi.localIP().toString().c_str());
}

void connectMQTT() {
  while (!mqtt.connected()) {
    Serial.print("MQTT connecting...");
    if (mqtt.connect(CLIENTID)) {
      Serial.println("OK");
      mqtt.subscribe(SUB_TOPIC, 1);
    } else {
      Serial.printf("fail rc=%d; retry in 2s\n", mqtt.state());
      delay(2000);
    }
  }
}

void sendNECCommand(int pin, uint16_t address, uint8_t command) {
  if (pin != IR_SEND_PIN) {
    IrSender.begin(pin); // only needed if you ever change pins at runtime
  }
  IrSender.sendNEC(address, command, 0);
  Serial.print("Sent NEC cmd 0x");
  Serial.print(command, HEX);
  Serial.print(" addr 0x");
  Serial.print(address, HEX);
  Serial.print(" on pin ");
  Serial.println(pin);
}
