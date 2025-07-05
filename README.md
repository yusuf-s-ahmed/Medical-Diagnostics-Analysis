# Analysing Patient BPM for Medical Diagnostics Using Python, NumPy and C++

# HeartGuard: Real-Time Heart Diagnostics and Emergency Alert System

**HeartGuard** is a hardware-software system developed during a 48-hour health hackathon at City, University of London. It detects early signs of heart disease and autonomously alerts emergency responders during critical events, with a focus on supporting vulnerable and elderly patients.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Implementation Details](#implementation-details)
- [Challenges and Solutions](#challenges-and-solutions)
- [Lessons Learned](#lessons-learned)
- [Future Work](#future-work)


## Overview

At a 48-hour university health hackathon hosted by the City Robotics Society, I co-developed **HeartGuard**, a hardware-software system for real-time heart diagnostics and emergency response. The system was designed to detect early signs of heart disease and automatically notify responders in critical situations.


## Features

- **3-point ECG hardware integration** with Arduino Uno R4 Wi-Fi, achieving 15% higher accuracy over typical single-point devices.
- **C++ signal filtering algorithm** to remove voltage noise across over 300 test samples.
- **Python diagnostics platform** using NumPy and Plotly to simulate and visualise BPM data for over 20 users.
- **Automated alerting system** that uses Twilio Voice API and Webhooks to initiate phone calls and send GPS location during simulated heart emergencies.
- **AI-generated medical summaries** using OpenAI GPT-4 and 3.5 Turbo, reducing manual documentation workload by approximately 80%.


## System Architecture

```plaintext
[ECG Sensor] → [Arduino Uno R4] → [C++ Noise Filter] → [Python Diagnostics App] → 
→ [Threshold Detector] → [Twilio Webhook + Call] → [Emergency Contact]
                                 ↳ [GPT-4 Report Generator] → [Medical Output]
