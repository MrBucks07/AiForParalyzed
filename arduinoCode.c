//string coming from python through serial data.
String pyInput;

void setup() {
  //starting serial communication.
  Serial.begin(9600);

  //declaring output pins.
  pinMode(13, OUTPUT);
  pinMode(7, OUTPUT);

}

void loop() {

  if(Serial.available() > 0){
    //reading string coming from python.
    pyInput = Serial.readString();


    if(pyInput == "ON"){
      //if input is on turn on led.
      digitalWrite(13, HIGH);
    }
    else if(pyInput == "OFF"){
      //if input is off turn off led.
      digitalWrite(13, LOW);
    }
    else if(pyInput == "BON"){
      //if input is buzzer on turn on buzzer.
      digitalWrite(7, HIGH);
      delay(10000);
      digitalWrite(7,LOW);
    }
  }
  delay(1000);
}