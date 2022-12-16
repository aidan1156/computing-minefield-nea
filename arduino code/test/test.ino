//import the software serial port and define the pins
#include <SoftwareSerial.h>
#include <stdlib.h>
#define rxPin 2
#define txPin 3
#define ledPin 4
#define buttonpin 5

#define message_max_length 30//the max length of a message 
#define bluetooth_tick_speed 100//how often (in ms) we should send the currently pressed buttons
#define button_tick_speed 50//how often we should check if the buttons are clicked

//setup the software serial port
SoftwareSerial mySerial(rxPin, txPin); // RX, TX

//define the variables
int i;
int n;

bool senddata = false;
char command;
unsigned long tick_time = millis();
unsigned long button_tick_time = millis();
int button_states[64];//state of all 64 buttons
char bluetooth_message[message_max_length];//string which is sent to app
int message_buffer_pos;

void setup() {
    //setup the pins
    pinMode(rxPin, INPUT);
    pinMode(txPin, OUTPUT);
    pinMode(ledPin, OUTPUT);
    pinMode(buttonpin, INPUT_PULLUP);
  
    digitalWrite(ledPin, LOW);

    //start the serial connections
    mySerial.begin(115200); 
    Serial.begin(9600);
}

void loop() {
    //if 700 miliseconds have passed since we last checked for messages/sent messages
    if (millis()-tick_time > bluetooth_tick_speed){
        tick_time = millis();
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

        if (senddata){
            //loop through the 'bluetooth_message' array and clear it ready for next input
            for (i=0;i<message_max_length;i++){
                bluetooth_message[i] = 0;
            }

            button_states[1] = 5;

            message_buffer_pos = 0;//reset the pos variable
            for (i=0;i<64;i++){//loop over each button
                //if the current pos is less than the max pos-3 (due to us using a max of 3 buffer points in 1 loop)
                if (message_buffer_pos < message_max_length-3){
                    if (button_states[i] > 0){//if the button has been pressed for more than 3 ticks
                        char button_id[4];//convert i into a string 
                        itoa(i,button_id,10);
                        for (n=0;n<strlen(button_id);n++){//then loop over each char in the button id
                            bluetooth_message[message_buffer_pos] = button_id[n];//and add it to the message string
                            message_buffer_pos += 1;
                        }
                        bluetooth_message[message_buffer_pos] = ',';//comma separate it
                        message_buffer_pos += 1;
                    }
                }
            }
            if (message_buffer_pos != 0){
                bluetooth_message[message_buffer_pos-1] = 0;//add the string terminator character
                Serial.println(bluetooth_message);//send the message
                mySerial.println(bluetooth_message);
            }      
            else{//if nothing is pressed print nothing
                Serial.println("nothing");
                mySerial.println("nothing");
            }
        }
    }

    //read the button for input changes
    if (millis()-button_tick_time > button_tick_speed){
        if (digitalRead(buttonpin) == false){
            button_states[0] += 1; 
        }
        else{
            button_states[0] = 0;
        }
        button_tick_time = millis();
    }

//    delay(500);
}
