/********************************
 * Layout 
 * *****************************/
#define CMRI_BAUD_RATE 9600

/********************************
 * Station Code: MML 
 * *****************************/

// Sensor Node
#define MML_SENSORS_NODE_ADDR 1
#define MML_SENSORS_NODE_BITS_IN 24
#define MML_SENSORS_NODE_BITS_OUT 48
#define MML_SENSORS_ARDUINO_AUTO485_PIN 2

// Turnouts Node
#define MML_TURNOUTS_NODE_ADDR 2
#define MML_TURNOUTS_ARDUINO_AUTO485_PIN 2

// Panel Node
#define MML_PANELS_NODE_ADDR 3
#define MML_PANELS_ARDUINO_AUTO485_PIN 2

// Signals Node
#define MML_SIGNALS_NODE_ADDR 4
#define MML_SIGNALS_NODE_BITS_IN 24
#define MML_SIGNALS_NODE_BITS_OUT 48
#define MML_SIGNALS_ARDUINO_AUTO485_PIN 2