int potPin = A0; 
int potPin2 = A8;
int potVal = 0;
int potVal2 = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  potVal = analogRead(potPin);
  potVal2 = analogRead(potPin2);
  byte mappedValue = map(potVal, 0, 1023, 200, 0);
  byte mappedValue2 = map(potVal2, 0, 1023, 200, 0);
  
  if(mappedValue >= 1){
    Serial.print("Inn");
    Serial.println(mappedValue);
  }
  
  if(mappedValue2 >= 1){
    Serial.print("Ut");
    Serial.println(mappedValue2);
  }
  
}
