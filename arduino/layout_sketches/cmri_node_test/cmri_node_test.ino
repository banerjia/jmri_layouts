#include <CMRI.h>

#define CMRI_NODE_ADDR 1
#define CMRI_NODE_INPUTS 32
#define CMRI_NODE_OUTPUTS 64
#define CMRI_BAUD 9600
#define DEBUG_OUTPUT_PIN 13

CMRI cmri(CMRI_NODE_ADDR, CMRI_NODE_INPUTS, CMRI_NODE_OUTPUTS);

void setup() {
  Serial.begin(CMRI_BAUD, SERIAL_8N2);
  pinMode(DEBUG_OUTPUT_PIN, OUTPUT);
}

void loop() {
  cmri.process();

  digitalWrite(DEBUG_OUTPUT_PIN, cmri.get_bit(63));
}
