const int RED_PIN = 9;
const int GREEN_PIN = 10;
const int BLUE_PIN = 11;

String readString;

void setup() {
  Serial.begin(9600);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
}

void loop() {


  //reads serial inputs formated 30r,180g,70b, etc
  //buttonState = digitalRead(START_BUTTON);
  //if (buttonState) digitalWrite(GREEN_PIN,HIGH);
  //else digitalWrite(GREEN_PIN,LOW);
  if (Serial.available())  {
    char c = Serial.read();  //gets one byte from serial buffer
    if (c == ',') {  //checks for comma, end of command
      if (readString.length() >1) {
        

        int n = readString.toInt();  //convert readString into a number
          
          if(readString.indexOf('r') >0) analogWrite(RED_PIN,n);
          if(readString.indexOf('g') >0) analogWrite(GREEN_PIN,n);
          if(readString.indexOf('b') >0) analogWrite(BLUE_PIN,n);
         readString=""; //clears variable for new input
      }
    }  
    else {     
      readString += c; //makes the string readString
    }
  }
}

