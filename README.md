# IoT & Control Component – EMSIB

This module is responsible for:

- Telemetry ingestion  
- Device control  
- Optimization scenario application  
- MQTT communication (simulated)

## Endpoints implemented

### 1. POST /iot/telemetry
Stores real-time telemetry sent by sensors.

### 2. POST /iot/device-control/{deviceId}/command
Simulates device control through MQTT.

### 3. POST /iot/optimization/apply
Receives optimization scenarios and applies them.

## How to run

pip install -r requirements.txt
uvicorn src.main:app --reload

## Authors
- Aday García  
- Cristian Costa
