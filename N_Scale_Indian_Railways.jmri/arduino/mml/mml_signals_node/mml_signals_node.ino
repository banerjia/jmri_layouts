#include <CMRI.h>
#include <Auto485.h>

#define NODE_ADDR 4
#define NODE_BITS_IN 24
#define NODE_BITS_OUT 48
#define CMRI_BAUD_RATE 9600
#define ARDUINO_AUTO485_PIN 2

Auto485 cmri_bus(ARDUINO_AUTO485_PIN);
CMRI cmri(NODE_ADDR, NODE_BITS_IN, NODE_BITS_OUT, cmri_bus);

void setup() {
  // Cofigure port registers for input/output setup

  // Set pins D2 - D7 as output
  DDRD |= B11111100;

  // Set pins D8 - D13 as output
  DDRB |= B00111111;

  // Set pins A0 - A3 as output
  DDRC |= B00001111;

  // Set these individually, cannot locate the registers for these
  pinMode(A6,OUTPUT);
  pinMode(A7,OUTPUT);

  /*********************
   * TO DO: Set all RED LEDs to HIGH
   **********************/


   // Setup for CMRI communications

   // For use with MAX485
   cmri_bus.begin(CMRI_BAUD_RATE);

   // For use with regular USB
   //Serial.begin(CMRI_BAUD_RATE, SERIAL_8N2);

}

void loop() {
  // Part of the CMRI process
  cmri.process();


  /*****************************
   * Get CMRI data
   * 
   * There primary focus of the logic here is to arrange the bits
   * received from CMRI in such a way so that they can be assigned 
   * to the pins directly using PORT registers. To that end the following 
   * logic is applied:
   * 
   * 1. Get the first byte as is and then shift it two bits to the right before 
   *    the bit sequence is flipped.  
   * 2. During the first iteration the bit_offset is set
   *    to 0 so the bits from the beginning are fetched.
   * 3. Flip the sequence of bits received so that it matches pin to port 
   *    mapping.
   * 4. At the end of the while loop the bit offset is set to 2 
   *    so that subsequent get_byte operation properly stagger
   *    the bit fetches. 
   *****************************/
  uint8_t num_of_bytes = 3;
  byte data_recd[3];
  uint8_t bit_offset = 0;

  while(--num_of_bytes){
    
    uint8_t iteration_index = 2 - num_of_bytes;
    uint8_t getByte_index = (iteration_index * 8 ) - bit_offset;
    
    // Get 1 byte of data
    data_recd[iteration_index] = cmri.get_byte(getByte_index);

    // Adjust the bit sequence in the first byte to 
    // correspond with pins starting at pin 3 (reg 2) instead of pins 1 and pin 2
    // which are reserved for TX/RX operations. 
    if(!iteration_index)
      data_recd[iteration_index] >>= 2;
      
    // Flip the sequence of bits in the byte to facilitate easier bit 
    // math operation in pin manipulations
    data_recd[iteration_index] = (data_recd[iteration_index] & 0xF0) >> 4 | (data_recd[iteration_index] & 0x0F) << 4;
    data_recd[iteration_index] = (data_recd[iteration_index] & 0xCC) >> 2 | (data_recd[iteration_index] & 0x33) << 2;
    data_recd[iteration_index] = (data_recd[iteration_index] & 0xAA) >> 1 | (data_recd[iteration_index] & 0x55) << 1;   

    bit_offset = 2;
  }

  // Set the pins from D2 - D7
  PORTD = data_recd[0];

  // Set pins D8 - D13
  // PORTB >> 6 << 6 : clear the right 6 bits of PORTB; PORTB only hosts 6 pins as opposed to 8
  // data_recd[1] << 2 >> 2: clears the left 2 bits of data_recd[1]
  PORTB = ((PORTB >> 6)<< 6) | ((data_recd[1] << 2) >> 2);

  // Bits to set for A0-A3 spans the last two bits of byte[1] and first 2 bits of byte[2]
  byte PORTC_bits = (data_recd[1] >> 6) | ((data_recd[2] >> 6) << 2);
  PORTC |= PORTC_bits;

  digitalWrite(A6, data_recd[4]);
  digitalWrite(A7, data_recd[3]);
}
