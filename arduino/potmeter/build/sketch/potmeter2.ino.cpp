#include <Arduino.h>
#line 1 "/home/vidr/dev/bachelor2023/PotmeterBachelor/potmeter2/potmeter2.ino"
int potPin = A0; 
int potPin2 = A8;
int potVal = 0;
int potVal2 = 0;

#line 6 "/home/vidr/dev/bachelor2023/PotmeterBachelor/potmeter2/potmeter2.ino"
void setup();
#line 10 "/home/vidr/dev/bachelor2023/PotmeterBachelor/potmeter2/potmeter2.ino"
void loop();
#line 6 "/home/vidr/dev/bachelor2023/PotmeterBachelor/potmeter2/potmeter2.ino"
void setup() {
  Serial.begin(9600);
}

void loop() {
  potVal = analogRead(potPin);
  potVal2 = analogRead(potPin2);
  byte potInn = map(potVal, 0, 1023, 200, 0);
  byte potUt = map(potVal2, 0, 1023, 200, 0);
  
  if(potInn != 1){
    Serial.print("Inn");
    Serial.println(potInn);
  }
  
  if(potUt != 1){
    Serial.print("Ut");
    Serial.println(potUt);
  }
  
}

