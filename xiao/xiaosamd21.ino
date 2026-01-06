
// RavensPi, 2025-2026
// External Module/File: xiaosamd21.ino

// Soil Moisture Serial Output
// Run on XIAO SAMD21
// Continuously prints soil moisture sensor values to Serial for Raspberry Pi


const int soilPin = A10;  // Analog pin connected to the soil sensor

void setup() {
  Serial.begin(115200);
  while (!Serial);  // Wait for USB serial connection
  pinMode(soilPin, INPUT);
  Serial.println("Starting soil moisture readings...");
}

void loop() {
  int value = analogRead(soilPin);
  Serial.println(value);
  delay(1000);  // every second
}