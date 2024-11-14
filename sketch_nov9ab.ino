unsigned long lastBeatTime = 0;
unsigned long startTime = 0;
int beatCount = 0;
float bpm = 0; // Variable to store BPM value

bool isPeak = false;
int sensorValue = 0;
int previousSensorValue = 0;
const int numReadings = 10; // Number of readings for smoothing
int readings[numReadings]; // Array to hold sensor readings
int readIndex = 0; // Index of the current reading
int total = 0; // Sum of the readings
int average = 0; // Average sensor value

float bpmSum = 0; // Sum of BPM values for averaging
int bpmCount = 0; // Count of BPM values for averaging

// Adaptive threshold variables
int threshold = 200; // Initial threshold
float thresholdFactor = 0.75; // Factor to adjust threshold

void setup() {
  Serial.begin(9600);
  pinMode(10, INPUT); // Setup for leads off detection LO +
  pinMode(11, INPUT); // Setup for leads off detection LO -
  pinMode(LED_BUILTIN, OUTPUT); // Set the built-in LED pin as an output

  // Initialize the readings array to zero
  for (int i = 0; i < numReadings; i++) {
    readings[i] = 0;
  }
  startTime = millis();
}

void loop() {
  if ((digitalRead(10) == 1) || (digitalRead(11) == 1)) {
    Serial.println('!');
    digitalWrite(LED_BUILTIN, LOW); // Turn off LED when leads are off
  } else {
    // Subtract the last reading
    total = total - readings[readIndex];
    // Read the sensor value
    sensorValue = analogRead(A0);
    // Add the reading to the array
    readings[readIndex] = sensorValue;
    // Add the reading to the total
    total = total + readings[readIndex];
    // Advance to the next position in the array
    readIndex = readIndex + 1;

    // If we're at the end of the array, wrap around to the beginning
    if (readIndex >= numReadings) {
      readIndex = 0;
    }

    // Calculate the average
    average = total / numReadings;

    Serial.print("Smoothed Sensor Value: ");
    Serial.println(average);

    // Adjust the threshold adaptively
    threshold = average * thresholdFactor;

    // Detect a beat based on changes in sensor values
    if (average > threshold && !isPeak && average > previousSensorValue) {
      isPeak = true;
      unsigned long currentTime = millis();
      if (currentTime - lastBeatTime > 300) { // Debounce time in ms
        beatCount++;
        lastBeatTime = currentTime;

        // Blink LED to indicate a beat
        digitalWrite(LED_BUILTIN, HIGH); // Turn on the LED
        delay(50); // Keep the LED on for 50ms
        digitalWrite(LED_BUILTIN, LOW); // Turn off the LED

        // Debug beat detection
        Serial.print("Beat Count: ");
        Serial.println(beatCount);
      }
    } else if (average < threshold || average < previousSensorValue) {
      isPeak = false;
    }
    previousSensorValue = average;

    // Calculate BPM every 5 seconds
    if (millis() - startTime >= 5000) { // 5-second interval
      float timeInSeconds = (millis() - startTime) / 1000.0;
      if (timeInSeconds > 0) {
        bpm = (beatCount / timeInSeconds) * 60.0;
        // Add BPM to running average
        bpmSum += bpm;
        bpmCount++;
      }
      // Calculate running average BPM
      float avgBpm = bpmSum / bpmCount;
      Serial.print("BPM: ");
      Serial.println(avgBpm);

      // Reset variables for the next interval
      beatCount = 0;
      startTime = millis();
      bpmSum = 0; // Reset BPM sum
      bpmCount = 0; // Reset BPM count
    }
  }
  delay(1); // Minimal delay to prevent data saturation
}

