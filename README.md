# Analysing Patient BPM for Medical Diagnostics Using Python, NumPy and C++

**HeartGuard** is a hardware-software system developed during a 48-hour health hackathon at City, University of London. It detects early signs of heart disease and autonomously alerts emergency responders during critical events, with a focus on supporting vulnerable and elderly patients.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Implementation Details](#implementation-details)
- [Challenges and Solutions](#challenges-and-solutions)
- [Impact](#impact)

## Overview

At a 48-hour university health hackathon hosted by the City Robotics Society, I co-developed **HeartGuard**, a hardware-software system for real-time heart diagnostics and emergency response. The goal was to detect early signs of heart disease and autonomously notify responders in critical events, especially for vulnerable or elderly patients.

## Features

- 3-point ECG hardware integration with Arduino Uno R4 Wi-Fi, achieving 15% higher accuracy over typical single-point devices.
- Custom C++ signal filtering algorithm to clean noisy voltage spikes across over 300 test samples.
- Python diagnostics platform using NumPy and Plotly to simulate and visualise BPM data for 20+ users.
- Automated emergency alert system using Twilio Voice API and Webhooks to initiate phone calls and transmit GPS location during critical BPM events.
- AI-generated medical summaries and recommendations using OpenAI GPT-4 and 3.5 Turbo, reducing manual documentation workload by approximately 80%.


## Technology Stack

| Component         | Tools and Libraries                       |
|------------------|--------------------------------------------|
| Hardware          | Arduino Uno R4 Wi-Fi, 3-Point ECG Sensor   |
| Signal Processing | C++                                       |
| Web Application   | Python, Flask, Plotly, NumPy               |
| AI Integration    | OpenAI GPT-4                               |
| Communication     | Twilio Voice API, Webhook URLs             |

## Implementation Details

After a team alignment session with hardware and backend contributors, I led the development of the diagnostics and alerting pipeline.

On the hardware side:
- Integrated a 3-point ECG sensor with an Arduino Uno R4 Wi-Fi to capture patient BPM data.
- Improved BPM detection accuracy by approximately 15% compared to single-point consumer devices like Apple Watches.
- Developed a custom signal processing algorithm in C++ to remove voltage spikes and filter noisy input across more than 300 test samples.

On the software side:
- Built a Python-based diagnostics platform to simulate and monitor over 20 user BPM streams.
- Used NumPy for real-time BPM calculations and Plotly for live visualisation.
- Designed a threshold-based triggering system that identified anomalous heart activity in real time.
- Integrated Twilio’s Voice API to automatically initiate phone calls and used Webhook URLs to transmit simulated GPS location data during critical events. This reduced average emergency response time in simulations by around 2 minutes.

AI reporting:
- Used OpenAI GPT-4 and 3.5 Turbo to generate structured medical reports based on individual BPM patterns and events.
- Optimised prompt structure and system roles to ensure consistent report output across various test scenarios.
- Reduced documentation effort by approximately 80%, enabling rapid triage and response during simulations.

## Challenges and Solutions

| Challenge                              | Solution                                                   |
|---------------------------------------|------------------------------------------------------------|
| Noisy ECG signals                     | Built a C++ filtering algorithm to smooth input data       |
| Inconsistent GPT report formatting    | Defined a structured prompt format and refined model roles |
| Real-time data visualisation bottlenecks | Limited simulation user pool and optimised Plotly updates |
| API coordination and rate limits      | Throttled Twilio calls and used pre-registered numbers     |

## Impact

This project taught me how to combine embedded hardware signal processing with real-time data analytics and AI automation under tight time and hardware constraints. It also gave me experience working on multi-modal systems where cloud APIs, frontend logic, and low-level hardware signals directly influence critical system behaviour.

