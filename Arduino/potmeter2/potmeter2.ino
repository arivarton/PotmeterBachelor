int potPin = A8; //A0
int potPin2 = A0; //A0
int potVal = 0;
int potVal2 = 0;
bool pose = false;
int nummer = 1;
int poseNr = 1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  potVal = analogRead(potPin);
  potVal2 = analogRead(potPin2);
  byte mappedValue = map(potVal, 0, 1023, 200, 0);
  byte mappedValue2 = map(potVal2, 0, 1023, 200, 0);
  /*Serial.print("Verdi:");
  Serial.println(mappedValue);*/
  //Serial.println(potVal);

  if(mappedValue >= 5){
    pose = true;
    nummer += 1;
    Serial.print("Inn");
    Serial.println(mappedValue);
  }
  else{
    Serial.println("PoseI");
  }
  if(mappedValue2 >= 5){
    Serial.print("Ut");
    Serial.println(mappedValue2);
  }
  else{
    Serial.println("PoseU");
  }
  
}

/*int printNy(){
  if(nummer >= 1){
    Serial.println("Ny pose");
    nummer = 0;
    poseNr += 1;
  }
}*/

int skrivFil() {}
