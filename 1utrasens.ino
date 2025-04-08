#include <SoftwareSerial.h>
const int TRIG_PIN=3;
const int ECHO_PIN=4;
const int threshold=50;
SoftwareSerial tts(3,4);

void setup(){
  Serial.begin(9600);
  tts.begin(9600);
  pinMode(TRIG_PIN,OUTPUT);
  pinMode(ECHO_PIN,INPUT);
  Serial.println("Measurement of distance is initialised- far and near condition");
}

void loop(){
  long duration;
  float distance;
  
  digitalWrite(TRIG_PIN,LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN,HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN,LOW);
  
  duration=pulseIn(ECHO_PIN,HIGH);
  distance=(duration*0.034)/2;
  
  if(distance<=threshold){
    Serial.println("Obstacle is near");
    tts.println("Obstacle is detected in 50 centimetres range");
  } else {
    Serial.print("Obstacle is far: ");
    Serial.print(distance);
    Serial.println(" centimeters");
    tts.println("Obstacle is far and not in the range of 50 centimetres");
  }
  delay(500);
}