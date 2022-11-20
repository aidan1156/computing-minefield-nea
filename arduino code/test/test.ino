
#define rxPin 0
#define txPin 1
#define ledPin 4
#define inpin 5

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

  Serial.begin(115200); 
  Serial.println ("Hello");
}

void loop() {
  // put your main code here, to run repeatedly:
   while (Serial.available()>0) {
  command=Serial.read ();
  if (command == 'g'){
    senddata = true;
  }
  if (command == 's'){
    senddata = false;
  }
 }
//send data
if (senddata){
sprintf (s,"%d,%d,%d\r",digitalRead(inpin),1,3);
 Serial.println (s); 
}
}
