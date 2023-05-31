int potPin = A0; 
int potPin2 = A7;

int potVal = 0;
int potVal2 = 0;

int lavesteVerdiInn = 1024;
int potInn = 0;

int lavesteVerdiUt = 1024;
int potUt = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  potInn = analogRead(potPin);
  potUt = analogRead(potPin2);
  
  if(potInn < lavesteVerdiInn){
    Serial.print("Inn:\n");
    Serial.println(potInn);
    lavesteVerdiInn = potInn;
  }
  
  if(potUt < lavesteVerdiUt){
    Serial.print("Ut:\n");
    Serial.println(potUt);
    lavesteVerdiUt = potUt;
  }
}
