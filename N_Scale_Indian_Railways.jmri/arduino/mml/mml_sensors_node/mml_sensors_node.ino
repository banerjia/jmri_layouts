#include <CMRI.h>
#include <Auto485.h>
#include "/home/banerjia/jmri_layouts/N_Scale_Indian_Railways.jmri/arduino/node_def.h"




//Auto485 cmri_bus(MML_SENSORS_ARDUINO_AUTO485_PIN);
// CMRI cmri(MML_SENSORS_NODE_ADDR, MML_SENSORS_NODE_BITS_IN, MML_SENSORS_NODE_BITS_OUT, cmri_bus);
CMRI cmri(MML_SENSORS_NODE_ADDR, MML_SENSORS_NODE_BITS_IN, MML_SENSORS_NODE_BITS_OUT);

void setup(){
    Serial.begin(CMRI_BAUD_RATE);
}

void loop(){
    int resist_val = analogRead(A0);
    Serial.println(resist_val);
}
