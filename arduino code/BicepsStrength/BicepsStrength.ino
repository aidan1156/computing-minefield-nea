#include <Wire.h>
#include <TimerOne.h>

#define rxPin 0
#define txPin 1
#define ledPin 4

int state = 0;
int flash,count,n;
unsigned int x,x1;
char s[30];
char buf[100];
int outbuf[256];
int curouti,outi;
int lastbuf;
unsigned int contdata,datareq;
char *ptr;
int isline;

void setup() {
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

////code used to write AT commands
//// ends with an endless loop
//  digitalWrite(ledPin, HIGH);
//  delay (1000);
// digitalWrite(ledPin, HIGH); delay (50);digitalWrite(ledPin, LOW);
//  Serial.begin (38400);
//  delay (3000);
// digitalWrite(ledPin, HIGH); delay (50);digitalWrite(ledPin, LOW);
// Serial.println ("AT+BAUD=115200,1,0");
//  delay (1000);
// digitalWrite(ledPin, HIGH); delay (50);digitalWrite(ledPin, LOW);
// Serial.println ("AT+NAME=ArmTrainer2");
// delay (1000);
// digitalWrite(ledPin, HIGH); 
// 
// while (1) {};
//
// /////////////////////////


  
  Serial.begin(115200); 
  //Serial.println ("Hello");
  Wire.begin();
  Timer1.initialize(5000);
  Timer1.attachInterrupt(doadc);
  count=0;
  lastbuf=-1;
  datareq=0;
  contdata=0;
  outi=0;
  curouti=0;
}

void doadc (void) {
unsigned int x,n;
unsigned int xx[32];
count++;
digitalWrite (ledPin,HIGH);

//for (n=0;n<32;n++) x+=analogRead (1);
for (n=0;n<32;n++) xx[n]=analogRead (1);
x=QuickMedian<int>::GetMedian(xx,32);

if ((datareq>0)||(contdata==1)) {
  outi=(outi+1)&0xff;
  outbuf[outi]=x;
  datareq--;
  }
digitalWrite (ledPin,LOW);
}

void writedac (int x) {
   Wire.beginTransmission(MCP4725_ADDR);
  Wire.write(64);                     // cmd to update the DAC
  Wire.write(x >> 4);        // the 8 most significant bits...
  Wire.write((x & 15) << 4); // the 4 least significant bits...
  Wire.endTransmission();
}

void loop() {

 if (outi!=curouti) {
  curouti=(curouti+1)&0xff;;
  sprintf (s,"%d",outbuf[curouti]);
  Serial.println (s);
 }

 isline=0;
 while (Serial.available()>0) {
  lastbuf++;
  buf[lastbuf]=Serial.read ();
  if (buf[lastbuf]==10) isline=lastbuf;
 }
  
  if  (isline>0) {
    if (buf[0]>'Z') buf[0]=buf[0]-32; //convert to upper case
    if (buf[0]=='Z') { //Z zero force
     x=0;
     Timer1.stop();
     for (n=0;n<16;n++) x+=analogRead (0);
     Timer1.start();
     x=x>>2;
     writedac (x);
     sprintf (s,"%d",x);
     Serial.println (s);
  
     }
   if (buf[0]=='G') {  //command G followed by number captures this number of samples
     if ((buf[1]>'0')&&(buf[1]<='9')) datareq=(buf[1]-'0')*200;
     if ((buf[1]>='A')&&(buf[1]<='F')) datareq=(buf[1]-'A'+10)*200;
     if ((buf[1]>='a')&&(buf[1]<='f')) datareq=(buf[1]-'a'+10)*200;
     sprintf (s,"%d",datareq);
     Serial.println (s);
     contdata=0;
     }
   if (buf[0]=='C') {  // C continuous data capture
     contdata=1;
     }
   if (buf[0]=='Q') {  //Q quite continuous data capture
     contdata=0;
     datareq=0;
     }
   for (n=isline+1;n<=lastbuf;n++) buf[n-isline-1]=buf[n];
   lastbuf=lastbuf-isline-1;
   }

if (count>=250) {
    //digitalWrite(ledPin,HIGH);
    }
if (count>=500) {
  //digitalWrite(ledPin,LOW);
  count=0;
  }
}
