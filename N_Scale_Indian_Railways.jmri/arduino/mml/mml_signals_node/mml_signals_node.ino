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
  
  byte data_recd[3];

  // Gather all the data from CMRI transmission
  data_recd[0] = cmri.get_byte(0);
  data_recd[1] = cmri.get_byte(1);
  data_recd[2] = cmri.get_byte(2);

/***************************************************************
 * 
 *  CMRI Address  Get_Byte  Arduino Pin   Port Register
 *  ************************************************************
 *  3001          0          2           D
 *  3002          0          3           
 *  3003          0          4
 *  3004          0          5
 *  3005          0          6
 *  3006          0          7           D
 *                           ********************************** 
 *  3007          0          8           B
 *  3008          0          9
 *  ****************
 *  3009          1          10
 *  3010          1          11
 *  3011          1          12
 *  3012          1          13
 *                           **********************************  
 *  3013          1          A0
 *  3014          1          A1
 *  3015          1          A2
 *  3016          1          A3
 *  ****************
 *  3017          2          A4
 *  3018          2          A5 
 * 
 ***************************************************************/


  // Set the pins from D2 - D7
  // Data received is shifted 2 bits to the left so that the 
  // first bit coincides with PIN 2; Refer to OUTPUT BIT to PIN Map
  PORTD = data_recd[0] << 2;

  // Set pins D8 - D13
  // data_recd[0] >> 6 shifts the left two bits for the first byte to 
  //                    to the very right
  // data_recd[1] << 4 shifts the right 4 bits of the second byte all
  //                    the way to the left and the >> 2 then shifts
  //                    them back to the right by 2 so that the two leftmost
  //                    bits coming out from the resulting operation are set 
  //                    to 0. PORTB doesn't have an assignment for the left
  //                    1 bits (PB7). This operation leaves the the right 2 bits 
  //                    to 0 so that the left 2 bits of data_recd[1] can be
  //                    inserted in there using a bitwise OR operation. 
  PORTB = (data_recd[0] >> 6) | ((data_recd[1] << 4) >>  2);

  // Bits to set for A0-A5 spans the last two bits of byte[1] and first 2 bits of byte[2]
  byte PORTC_bits = (data_recd[1] >> 3) | (data_recd[2] << 4);
  PORTC = PORTC_bits;
}
