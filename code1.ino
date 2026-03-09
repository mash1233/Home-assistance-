String command;

const int LED_PIN = 3;
const int BUZZER_PIN = 6;

bool blinkMode = false;
unsigned long previousMillis = 0;
const long interval = 2000;   // 2 seconds
bool ledState = LOW;

void setup() {
  Serial.begin(9600);

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {

  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "LED1_ON") {
      blinkMode = false;
      digitalWrite(LED_PIN, HIGH);
    }

    else if (command == "LED1_OFF") {
      blinkMode = false;
      digitalWrite(LED_PIN, LOW);
    }

    else if (command == "LED2_TOGGLE") {
      blinkMode = !blinkMode;  
    }

    else if (command == "BUZZER_ON") {
      digitalWrite(BUZZER_PIN, HIGH);
    }

    else if (command == "BUZZER_OFF") {
      digitalWrite(BUZZER_PIN, LOW);
    }
  }

  if (blinkMode) {
    unsigned long currentMillis = millis();

    if (currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;

      ledState = !ledState;
      digitalWrite(LED_PIN, ledState);
    }
  }
}
