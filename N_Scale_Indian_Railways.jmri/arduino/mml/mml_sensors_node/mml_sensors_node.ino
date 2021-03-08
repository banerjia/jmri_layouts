#include <CMRI.h>
#include <Auto485.h>
#include "/home/banerjia/jmri_layouts/N_Scale_Indian_Railways.jmri/arduino/node_def.h"




//Auto485 cmri_bus(MML_SENSORS_ARDUINO_AUTO485_PIN);
//CMRI cmri(MML_SENSORS_NODE_ADDR, MML_SENSORS_NODE_BITS_IN, MML_SENSORS_NODE_BITS_OUT, cmri_bus);
CMRI cmri(MML_SENSORS_NODE_ADDR, MML_SENSORS_NODE_BITS_IN, MML_SENSORS_NODE_BITS_OUT);

void setup(){
    Serial.begin(CMRI_BAUD_RATE);

    DDRB = B00000000;
    DDRC = B00000000;
    DDRD |= B00000000;
}

void loop(){
    cmri.process();

    // Get Sensors 1 - 8
    // PINS 1 - 3 (bits 0 - 2) are used for RX/TX/ and for MAX485
    // So we start reading the sensor values from PIN 3. To that 
    // end shift the PIND register values 3 to right to skip pins 1 - 3
    // This results in 3 slots opening on the left side of the byte. 
    // These are filled in my the first three bits of PINB. This makes for 
    // a byte to send back to CMRI
    // CMRI BYTE = XXX XXXXX
    //             --- -----
    //             PB   PD
    cmri.set_byte(0,((PIND >> 3) | (PINB << 5)));
    
    // Get Sensors 9 - 13
    // CMRI BYTE = XXX XXXXX
    //             --- -----
    //             PC   PB
    cmri.set_byte(1,((PINB >> 3 ) | (PINC << 5)));
}
