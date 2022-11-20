#define rxPin 0
#define txPin 1
#define ledPin 4

void setup() {
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  
    digitalWrite(ledPin, HIGH);
  delay (1000);
 digitalWrite(ledPin, HIGH); delay (50);digitalWrite(ledPin, LOW);
  Serial.begin (38400);
  delay (3000);
 digitalWrite(ledPin, HIGH); delay (50);digitalWrite(ledPin, LOW);
 Serial.println ("AT+BAUD=115200,1,0");
  delay (1000);
 digitalWrite(ledPin, HIGH); delay (50);digitalWrite(ledPin, LOW);
 Serial.println ("AT+NAME=Minefield");
 delay (1000);
 digitalWrite(ledPin, HIGH); 

}

void loop() {
  // put your main code here, to run repeatedly:

}
