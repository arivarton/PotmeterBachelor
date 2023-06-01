int potPin = A0; 
int potPin2 = A7;

int potVal = 0;
int potVal2 = 0;

int potInn = 0;

int potUt = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  potInn = analogRead(potPin);
  potUt = analogRead(potPin2);
  
  Serial.print("Inn:\n");
  Serial.println(potInn);
  
  Serial.print("Ut:\n");
  Serial.println(potUt);
}
