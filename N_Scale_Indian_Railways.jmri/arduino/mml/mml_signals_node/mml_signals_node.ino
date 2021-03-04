#include <CMRI.h>
#include <Auto485.h>

#define NODE_ADDR 4
#define NODE_BITS_IN 24
#define NODE_BITS_OUT 48
#define CMRI_BAUD_RATE 9600
#define ARDUINO_AUTO485_PIN 2

//Auto485 cmri_bus(ARDUINO_AUTO485_PIN);
// CMRI cmri(NODE_ADDR, NODE_BITS_IN, NODE_BITS_OUT, cmri_bus);
CMRI cmri(NODE_ADDR, NODE_BITS_IN, NODE_BITS_OUT);

void setup() {
  // Cofigure port registers for input/output setup

  // Set pins D2 - D7 as output
  DDRD = DDRD | B11111100;

  // Set pins D8 - D13 as output
  DDRB |= B00111111;

  // Set pins A0 - A5 as output
  DDRC |= B00111111;
  
   // Setup for CMRI communications

   // For use with MAX485
   //cmri_bus.begin(CMRI_BAUD_RATE);

   // For use with regular USB
   Serial.begin(CMRI_BAUD_RATE, SERIAL_8N2);

}

void loop() {
  // Part of the CMRI process
  cmri.process();

  uint8_t num_of_bytes = 3;
  byte data_recd[3];

  data_recd[0] = cmri.get_byte(0);
  data_recd[1] = cmri.get_byte(1);
  data_recd[2] = cmri.get_byte(2);

  // Set the pins from D2 - D7
  PORTD = data_recd[0] << 2;

  // Set pins D8 - D13
  // PORTB >> 6 << 6 : clear the right 6 bits of PORTB; PORTB only hosts 6 pins as opposed to 8
  // data_recd[1] << 2 >> 2: clears the left 2 bits of data_recd[1]
  PORTB = (data_recd[0] >> 6) | ((data_recd[1] << 4) >>  2);

  // Bits to set for A0-A5 spans the last two bits of byte[1] and first 2 bits of byte[2]
  byte PORTC_bits = (data_recd[1] >> 3) | (data_recd[2] << 4);
  PORTC = PORTC_bits;
}
