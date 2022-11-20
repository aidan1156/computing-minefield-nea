#include <SoftwareSerial.h>
#define rxPin 2
#define txPin 3
#define ledPin LED_BUILTIN


SoftwareSerial mySerial(rxPin, txPin); // RX, TX

void setup() {
//  pinMode(rxPin, INPUT);
//  pinMode(txPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  
//    digitalWrite(ledPin, HIGH);
  delay (1000);
 digitalWrite(ledPin, HIGH); delay (500);digitalWrite(ledPin, LOW);
  mySerial.begin (9600);
  delay (3000);
  digitalWrite(ledPin, HIGH); delay (500);digitalWrite(ledPin, LOW);
 mySerial.print ("AT+NAMEMinefield");
 delay(3000);
 digitalWrite(ledPin, HIGH); delay (500);digitalWrite(ledPin, LOW);
 mySerial.print ("AT+BAUD4");
  delay (1000);
 
 delay (1000);
 digitalWrite(ledPin, HIGH); 

}

void loop() {
  // put your main code here, to run repeatedly:

}
