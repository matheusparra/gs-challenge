#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

#define TRIG_PIN 5
#define ECHO_PIN 18
#define RAIN_SENSOR_PIN 34

const char* ssid = "SEU_WIFI";
const char* password = "SENHA_WIFI";
const char* serverUrl = "http://192.168.18.6:5000/dados"; // URL da API Flask

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(RAIN_SENSOR_PIN, INPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi conectado com sucesso!");

  Serial.println("Sistema de monitoramento iniciado");
}

float lerNivelRio() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duracao = pulseIn(ECHO_PIN, HIGH);
  float distancia_cm = duracao * 0.034 / 2;
  float nivel = 100.0 - distancia_cm;
  return max(0.0, nivel / 100.0); // metros
}

void loop() {
  float umidade = dht.readHumidity();
  float temperatura = dht.readTemperature();
  float nivel = lerNivelRio();
  float chuva_raw = analogRead(RAIN_SENSOR_PIN);
  float chuva = map(chuva_raw, 0, 4095, 100, 0);
  float vento = 12.5;

  Serial.println("📊 Dados Ambientais:");
  Serial.printf("🌡️ Temperatura: %.2f °C\n", temperatura);
  Serial.printf("💧 Umidade: %.2f %%\n", umidade);
  Serial.printf("🌊 Nível do Rio: %.2f m\n", nivel);
  Serial.printf("🌧️ Chuva: %.2f %%\n", chuva);
  Serial.printf("💨 Vento: %.2f km/h\n", vento);
  Serial.println("----------------------------");

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    String json = "{\"temperatura\":" + String(temperatura) +
                  ",\"umidade\":" + String(umidade) +
                  ",\"nivel\":" + String(nivel) +
                  ",\"chuva\":" + String(chuva) +
                  ",\"vento\":" + String(vento) + "}";

    int httpResponseCode = http.POST(json);
    Serial.printf("📡 Envio para servidor: código %d\n", httpResponseCode);
    http.end();
  }

  delay(5000);
}
