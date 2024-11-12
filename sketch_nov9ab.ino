#include <WiFi.h>
#include <HTTPClient.h>
#include <algorithm> // Include algorithm library for std::sort

// Wi-Fi credentials
const char* ssid = "TALKTALK51FE11";       // Replace with your Wi-Fi SSID
const char* password = "9Y4T4Y6T"; // Replace with your Wi-Fi password
const char* serverUrl = "http://http://127.0.0.1:8000/bpm"; // Replace with your FastAPI server's URL

// Heart rate monitoring variables
unsigned long lastBeatTime = 0;
unsigned long startTime = 0;
int beatCount = 0;
float bpm = 0; // Variable to store BPM value
float bpmValues[10]; // Array to hold the last 10 BPM values
int bpmIndex = 0; // Index for BPM values array
bool bpmStable = false; // Flag to indicate if BPM values are stable
bool isPeak = false;
int sensorValue = 0;
int previousSensorValue = 0;
const int numReadings = 10; // Number of readings for smoothing
int readings[numReadings]; // Array to hold sensor readings
int readIndex = 0; // Index of the current reading
int total = 0; // Sum of the readings
int average = 0; // Average sensor value

// Adaptive threshold variables
int threshold = 200; // Initial threshold
const float thresholdFactor = 0.79; // Factor to adjust threshold

void setup() {
    Serial.begin(9600);
    pinMode(10, INPUT); // Setup for leads off detection LO +
    pinMode(11, INPUT); // Setup for leads off detection LO -
    pinMode(LED_BUILTIN, OUTPUT); // Set the built-in LED pin as an output

    // Initialize the readings array to zero
    for (int i = 0; i < numReadings; i++) {
        readings[i] = 0;
    }

    // Initialize the BPM values array to zero
    for (int i = 0; i < 10; i++) {
        bpmValues[i] = 0;
    }

    startTime = millis();

    // Connect to Wi-Fi
    WiFi.begin(ssid, password); // Connect to Wi-Fi
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }

    Serial.println("Connected to WiFi");
}

float calculateMedian(float arr[], int size) {
    float temp[size];
    std::copy(arr, arr + size, temp);
    std::sort(temp, temp + size);
    if (size % 2 == 1) {
        return temp[size / 2];
    } else {
        return (temp[(size / 2) - 1] + temp[size / 2]) / 2.0;
    }
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

        // Adjust the threshold adaptively
        threshold = average * thresholdFactor;

        // Detect a beat based on changes in sensor values
        if (average > threshold && !isPeak && average > previousSensorValue) {
            isPeak = true;
            unsigned long currentTime = millis();

            if (currentTime - lastBeatTime > 400) { // Debounce time in ms
                beatCount++;

                // Calculate time between beats
                unsigned long beatInterval = currentTime - lastBeatTime;

                // Calculate BPM if the interval is within a reasonable range
                if (beatInterval > 375 && beatInterval < 1500) { // Corresponds to BPM range of 40 to 160
                    bpm = 60000.0 / beatInterval;

                    // Store the BPM value in the array
                    bpmValues[bpmIndex] = bpm;
                    bpmIndex = (bpmIndex + 1) % 10;

                    // Calculate the median of BPM values
                    float medianBPM = calculateMedian(bpmValues, 10);

                    // Check if the current BPM value is within the range of ±15 BPM of the median
                    if (bpm > medianBPM - 15 && bpm < medianBPM + 15) {
                        // Print stable BPM
                        Serial.print("BPM: ");
                        Serial.println(bpm);

                        // Send the BPM data to the FastAPI server
                        sendBPMToServer(bpm);
                    }
                }

                lastBeatTime = currentTime;

                // Blink LED to indicate a beat
                digitalWrite(LED_BUILTIN, HIGH); // Turn on the LED
                delay(50); // Keep the LED on for 50ms
                digitalWrite(LED_BUILTIN, LOW); // Turn off the LED
            }
        } else if (average < threshold || average < previousSensorValue) {
            isPeak = false;
        }
        previousSensorValue = average;
    }
    delay(1); // Minimal delay to prevent data saturation
}

// Function to send BPM data to the FastAPI server
void sendBPMToServer(float bpmValue) {
    HTTPClient http;
    http.begin(serverUrl); // Specify the server URL

    // Set the content type to JSON
    http.addHeader("Content-Type", "application/json");

    // Create the JSON payload with the BPM data
    String payload = "{\"bpm\": " + String(bpmValue) + "}";

    // Send a POST request with the JSON data
    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {
        Serial.println("Data sent successfully!");
    } else {
        Serial.println("Failed to send data");
    }

    http.end(); // Close the connection
}
