
---

# 🕵️‍♂️🍽️ DishDetectiveAI – Smart ESP32 + AI-Powered Roommate Dish Tracking System

DishDetectiveAI is an IoT-driven, AI-enhanced kitchen monitoring project built using an ESP32-CAM, Arduino C/C++, and a Python-based computer vision server. The system continuously monitors the household sink, detects when dirty dishes appear, identifies which roommate was last seen at the sink, and logs the event automatically.

It is a clever mixture of embedded hardware, machine learning, and real-world roommate chaos brought together through clean engineering principles.

---

## 🌐 System Overview

DishDetectiveAI combines microcontroller firmware, wireless communication, and AI modeling into a single pipeline:

1. ESP32-CAM captures JPEG frames of the sink and sends them to a local server using Wi-Fi.
2. A Python Flask server receives each frame and runs computer vision analysis.
3. Face recognition and AI models determine
   • who was at the sink
   • whether dishes appeared (clean to dirty transition)
4. A minimal LCD interface (Arduino Uno with a 16×2 display) cycles through roommate names and dish counters.

This creates a lightweight but powerful home automation system that keeps your kitchen and roommates accountable.

---

## 🔧 Key Features

• Embedded ESP32-CAM firmware
Written in Arduino C/C++, handling image capture, JPEG compression, and HTTP uploads.

• AI-enhanced dish and face detection
The server uses Python, OpenCV, and optional YOLO or face-recognition models to determine both who visited the sink and whether dishes were left behind.

• Roommate rotation LCD display
An Arduino Uno with a 16×2 display cycles through the list of roommates, showing their current dish count in real time.

• Local smart-home architecture
Fully Wi-Fi enabled, runs purely on a private LAN, and does not rely on cloud services.

---

## 🎯 Purpose and Motivation

DishDetectiveAI was built to merge embedded programming, AI modeling, and IoT systems into a practical project with a fun real-world application. It demonstrates:

• Low-level firmware development
• Microcontroller to server communication
• Edge-device camera streaming
• Machine learning inference on streamed images
• State tracking and event logging
• User feedback through an LCD hardware interface

By turning a daily household annoyance into an engineering challenge, DishDetectiveAI shows how modern AI and IoT technology can automate even the pettiest roommate disputes.



By: Ish and Naiyar 