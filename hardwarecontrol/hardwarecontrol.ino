int light1Pin = 8;  // Relay connected to pin 8 for light1
int light2Pin = 9;  // Relay connected to pin 9 for light2

void setup() {
  Serial.begin(9600);  // Start serial communication
  pinMode(light1Pin, OUTPUT);
  pinMode(light2Pin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readString();  // Read the incoming command
    
    // Check for light control commands
    if (command == "light1_on") {
      digitalWrite(light1Pin, HIGH);  // Turn on light1
      Serial.println("Light 1 is ON");
    }
    else if (command == "light1_off") {
      digitalWrite(light1Pin, LOW);  // Turn off light1
      Serial.println("Light 1 is OFF");
    }
    else if (command == "light2_on") {
      digitalWrite(light2Pin, HIGH);  // Turn on light2
      Serial.println("Light 2 is ON");
    }
    else if (command == "light2_off") {
      digitalWrite(light2Pin, LOW);  // Turn off light2
      Serial.println("Light 2 is OFF");
    }
    else {
      Serial.println("Invalid Command");
    }
  }
}
