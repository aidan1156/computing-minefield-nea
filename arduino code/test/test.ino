//import the software serial port and define the pins
#include <SoftwareSerial.h>
#define rxPin 2
#define txPin 3
#define ledPin 4
#define buttonpin 5

//setup the software serial port
SoftwareSerial mySerial(rxPin, txPin); // RX, TX

//define the variables
bool senddata = false;
char s[50];
char command;
int tick_time = millis();
int button_tick_time = millis();
int button_states[64];

void setup() {
    //setup the pins
    pinMode(rxPin, INPUT);
    pinMode(txPin, OUTPUT);
    pinMode(ledPin, OUTPUT);
    pinMode(buttonpin, INPUT_PULLUP);
  
    digitalWrite(ledPin, LOW);

    //start the serial connections
    mySerial.begin(115200); 
    mySerial.println ("Hello");

    Serial.begin(9600);
}

void loop() {
    //if 700 miliseconds have passed since we last checked for messages/sent messages
    if (millis()-tick_time > 700){
        //check for updates
        while (mySerial.available()>0) {
            command=mySerial.read ();
            if (command == 'g'){
            senddata = true;
            }
            if (command == 's'){
            senddata = false;
            }
        }
        //send data
        if (senddata){
            sprintf (s,"%d,%d,%d\r",1,1,3);
            mySerial.println (s); 
        }
        tick_time = millis();
    }

    //read the button for input changes
    if (millis()-button_tick_time > 50){
        if (digitalRead(buttonpin) == true){
            button_states[0] += 1; 
        }
        else if (button_states[0] != 0){
            button_states[0] = 0;
            Serial.println(0);
        }
        if (button_states[0] == 4){
            Serial.println(1);
        }

        button_tick_time = millis();
    }
}
