#include <ESP32Servo.h>

Servo myServo;

const int servoPin = 18;    // PWM-capable pin for the servo
const int buttonPin = 4;    // GPIO D4 (button or object detection)
const int statusLED = 13;   // Optional LED pin to indicate status

void setup() {
  Serial.begin(115200);
  delay(1000);  // Wait for serial initialization
  
  myServo.setPeriodHertz(50);              // Standard 50 Hz servo
  myServo.attach(servoPin, 500, 2400);     // Min/max pulse width in microseconds

  pinMode(buttonPin, INPUT_PULLUP);        // GPIO D4 as input with pull-up
  pinMode(statusLED, OUTPUT);              // LED to indicate when servo is active
  digitalWrite(statusLED, LOW);            // Ensure LED is off initially
}

void loop() {
  // Check if the object is on the desk (buttonPin LOW)
  if (digitalRead(buttonPin) == LOW) {
    Serial.println("Object detected! now waiting for trigger...");
    if (Serial.available()) {
      String command = Serial.readStringUntil('\n');
      command.trim();  // Remove any extra spaces or newlines

      if (command == "TRIGGER") {
        Serial.println("Trigger received and object detected!");

        digitalWrite(statusLED, HIGH);  // Turn on the LED when triggered

        // Move the servo from 0 to 180 degrees
        for (int pos = 0; pos <= 180; pos += 3) {
          myServo.write(pos);
          delay(10);
        }

        delay(300);  // Pause at 180 degrees

        // Move the servo back from 180 to 0 degrees
        for (int pos = 180; pos >= 0; pos -= 3) {
          myServo.write(pos);
          delay(10);
        }

        delay(300);  // Pause at 0 degrees
        digitalWrite(statusLED, LOW);  // Turn off the LED after the action
      } else {
        Serial.println("Unknown command: " + command);
      }
    }
  } else {
    // Optionally, log when no object is detected (can be helpful for debugging)
    Serial.println("No object detected, waiting for trigger...");
  }
}
