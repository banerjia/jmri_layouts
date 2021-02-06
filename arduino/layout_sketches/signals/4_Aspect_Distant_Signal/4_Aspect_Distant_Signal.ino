#include <CMRI.h>

#define RED 3
#define Y1 5
#define GREEN 9
#define Y2 11

CMRI cmri(1, 24, 48);
uint8_t last_aspect = 0;

void setup() {
    // put your setup code here, to run once:
    pinMode(RED, OUTPUT);
    pinMode(Y1, OUTPUT);
    pinMode(GREEN, OUTPUT);
    pinMode(Y2, OUTPUT);

    Serial.begin(9600);

}

void loop() {
    // put your main code here, to run repeatedly:


    cmri.process();

    byte current_aspect = cmri.get_byte(0);

    current_aspect = current_aspect >> 4;

    


    if (current_aspect != last_aspect) {



        // switch off last aspect
        switch (last_aspect) {
            case B00000101:
                for (uint8_t i = 254; i; i--)
                {
                    analogWrite(Y2, i);
                    analogWrite(Y1, i);
                    delay(1);
                }
                    analogWrite(Y2, 0);
                    analogWrite(Y1, 0);
                break;
            case B00000010:
                for (uint8_t i = 254; i; i--)
                {
                    analogWrite(GREEN, i);
                    delay(1);
                }
                    analogWrite(GREEN, 0);
                break;
            case B00000100:
                for (uint8_t i = 254; i; i--)
                {
                    analogWrite(Y1, i);
                    delay(1);
                }
                    analogWrite(Y1, 0);
                break;
            case B00001000:
                for (uint8_t i = 254; i; i--)
                {
                    
                    analogWrite(RED, i);
                    
                    delay(1);
                }
                    analogWrite(RED, 0);
                break;
        }

        // switch off last aspect
        switch (current_aspect) {
            case B00000101:
                for (uint8_t i = 100; i < 255; i++)
                {
                    analogWrite(Y2, i);
                    analogWrite(Y1, i);
                    delay(1);
                }
                break;
            case B00000010:
                for (uint8_t i = 100; i < 255; i++)
                {
                    analogWrite(GREEN, i);
                    delay(1);
                }
                break;
            case B00000100:
                for (uint8_t i = 100; i < 255; i++)
                {
                    analogWrite(Y1, i);
                    delay(1);
                }
                break;
            case B00001000:
                for (uint8_t i = 100; i < 255; i++)
                {
                    analogWrite(RED, i);
                    delay(1);
                }
                break;
        }

        last_aspect = current_aspect;

    }
}
