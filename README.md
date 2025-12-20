# IoT & Control Component – EMSIB

This module is responsible for:
- Telemetry ingestion
- Device control
- Optimization scenario application
- MQTT communication (simulated)

---

## Features

- Register and list IoT devices
- Ingest real-time telemetry (single and bulk)
- View live device state
- Send control commands to devices
- Track command history per device
- Apply optimization scenarios
- Check optimization execution status
- REST API with Swagger UI

---

## Endpoints Implemented

### Telemetry
1. **POST `/iot/telemetry`**  
   Stores real-time telemetry sent by devices.

2. **POST `/iot/telemetry/bulk`**  
   Stores telemetry data in batch.

3. **GET `/iot/telemetry/history`**  
   Returns historical telemetry for a device.

---

### Device Management
4. **POST `/iot/devices/register`**  
   Registers a new device.

5. **GET `/iot/devices`**  
   Lists all registered devices.

---

### Device Control
6. **POST `/iot/device-control/{deviceId}/command`**  
   Simulates sending a command to a device (MQTT-like).

7. **GET `/iot/device-control/{deviceId}/commands`**  
   Returns command history for a device.

---

### Optimization
8. **POST `/iot/optimization/apply`**  
   Applies an optimization scenario.

9. **GET `/iot/optimization/status/{scenarioId}`**  
   Returns optimization execution status.

---

### System State
10. **GET `/iot/state/live`**  
    Returns the latest known state of all devices.

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
python -m uvicorn src.main:app --reload

# Open Swagger UI in your browser
http://127.0.0.1:8000/docs
```

## Docker
```bash
# Build the image
docker build -t iot-control-component .

# Run the container
docker run -d -p 8000:8000 iot-control-component
```

## Authors
 - Aday García López
- Cristian Costa