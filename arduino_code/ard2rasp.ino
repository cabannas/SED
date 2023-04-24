

// Define communication variable
String command;

// Define pins
const int humAPin = A4;
const int humBPin = A5;
const int ledPin = 7;
const int ldrPin = A0;

int humAVal = 0;
int humBVal = 0;
int ldrVal = 0;

void setup() {

  Serial.begin(9600);

  // Initialize pins
  pinMode(humAPin, INPUT); 
  pinMode(humBPin, INPUT); 
  pinMode(ledPin, OUTPUT);
  pinMode(ldrPin, INPUT);

  delay(1000);  
}

void loop() {
  
  //read LDR  
  ldrVal = analogRead(ldrPin);

  //read Humidity Sensors
  humAVal = analogRead(humAPin);
  humBVal = analogRead(humBPin);

  // Send info to Raspi
  Serial.print("ldr");  // distinguish
  Serial.println(ldrVal);
  Serial.print("huma");
  Serial.println(humAVal);
  Serial.print("humb");
  Serial.println(humBVal);

  if(Serial.available()){

    // Read from Raspi
    command = Serial.readStringUntil('\n');
    command.trim(); // eliminates white spaces

    // Actions
    if (command.equals("dark")){

      digitalWrite(ledPin, HIGH);

    }else if (command.equals("light")){

      digitalWrite(ledPin, LOW);

    }else{

      // Default nothing

    }
  }

  delay(1000);
}
