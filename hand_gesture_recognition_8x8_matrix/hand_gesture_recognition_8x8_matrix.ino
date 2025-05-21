#include <LedControl.h>

// DIN, CLK, CS, # of devices
LedControl lc = LedControl(11, 13, 10, 1);

// Digits 0–5 and smiley face
byte symbols[7][8] = {
  // 0
  {0x3C, 0x66, 0x6E, 0x76, 0x66, 0x66, 0x3C, 0x00},
  // 1
  {0x18, 0x38, 0x18, 0x18, 0x18, 0x18, 0x7E, 0x00},
  // 2
  {0x3C, 0x66, 0x06, 0x0C, 0x30, 0x60, 0x7E, 0x00},
  // 3
  {0x3C, 0x66, 0x06, 0x1C, 0x06, 0x66, 0x3C, 0x00},
  // 4
  {0x0C, 0x1C, 0x3C, 0x6C, 0x7E, 0x0C, 0x0C, 0x00},
  // 5
  {0x7E, 0x60, 0x7C, 0x06, 0x06, 0x66, 0x3C, 0x00},
  // 😊 Smiley Face
  {0x3C, 0x42, 0xA5, 0x81, 0xA5, 0x99, 0x42, 0x3C}
};

String input;

void setup() {
  Serial.begin(9600);
  lc.shutdown(0, false);
  lc.setIntensity(0, 8);
  lc.clearDisplay(0);
}

void loop() {
  if (Serial.available()) {
    input = Serial.readStringUntil('\n');
    input.trim();

    if (input == "MIDDLE") {
      showSymbol(symbols[6]);  // Smiley
    } else {
      int num = input.toInt();
      if (num >= 0 && num <= 5) {
        showSymbol(symbols[num]);
      } else {
        lc.clearDisplay(0);  // Invalid input → clear
      }
    }
  }
}

void showSymbol(byte symbol[8]) {
  for (int row = 0; row < 8; row++) {
    lc.setRow(0, row, symbol[row]);
  }
}
