#include <SoftwareSerial.h>
#define rxPin 2
#define txPin 3
#define ledPin 4
#define inpin 5

SoftwareSerial mySerial(rxPin, txPin); // RX, TX

bool senddata = false;
char s[50];
char command;

void setup() {
  // put your setup code here, to run once:
  
pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(inpin, INPUT_PULLUP);
  digitalWrite(ledPin, LOW);

  mySerial.begin(115200); 
  mySerial.println ("Hello");
}

void loop() {
    // put your main code here, to run repeatedly:
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
  delay(700);
}
