int potPin = A0; //A0
int potPin2 = A8; //A0
int potVal = 0;
int potVal2 = 0;
bool pose = false;
int nummer = 1;
int poseNr = 1;

void setup() {
  Serial.begin(9600);
}

void loop() {
  /*!
  *Mapper potensiometerene fra 0 til 200.
  *Sjekker om verdien på de er over 1, hvis ja printes det sammen med henholdsvis "inn" og "ut" for å skille mellom de.
  *Dette fjernes senere i Python-programmet.
  *"PoseI" og "PoseU" printes hvis de ikke måler noe og trigger en if-løkke i Python-programmet om at posen ikke lenger måles.
  */
  potVal = analogRead(potPin);
  potVal2 = analogRead(potPin2);
  byte mappedValue = map(potVal, 0, 1023, 200, 0);
  byte mappedValue2 = map(potVal2, 0, 1023, 200, 0);
  
  if(mappedValue >= 43){
    pose = true;
    nummer += 1;
    Serial.print("Inn");
    Serial.println(mappedValue);
  }
  else{
    Serial.println("PoseI");
  }
  if(mappedValue2 >= 49){
    Serial.print("Ut");
    Serial.println(mappedValue2);
  }
  else{
    Serial.println("PoseU");
  }
  
}
