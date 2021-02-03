#include <CMRI.h>
#include "ir_cmri_config.h"

// Node Configuration
#define CMRI_NODE_ADDR 1
#define CMRI_NODE_INPUTS 24
#define CMRI_NODE_OUTPUTS 48


// Node TURNOUT bits
const byte BIT_MASK_CT1001 = B1000000;
const byte BIT_MASK_CT1002 = B0100000;
const byte BIT_MASK_CL1004 = B0010000;

// NODE BLOCK DETECTION bits
const byte BIT_MASK_CS1001 = B1000000;
const byte BIT_MASK_CS1002 = B0100000;
const byte BIT_MASK_CS1003 = B0010000;
const byte BIT_MASK_CS1004 = B0001000;


uint8_t sensor = 0;

CMRI cmri(CMRI_NODE_ADDR, CMRI_NODE_INPUTS, CMRI_NODE_OUTPUTS);

void setup() {
  // put your setup code here, to run once:
  //Serial.begin(IR_CMRI_CFG_CMRI_NODE_BAUD);
  pinMode(IR_CMRI_CFG_ARDUINO_DEBUG_PIN, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  //cmri.process();

}
