from fastapi import FastAPI
from src.telemetry import TelemetryStorage
from src.device_control import DeviceController
from src.optimization import OptimizationEngine


app = FastAPI()

telemetry_db = TelemetryStorage()
controller = DeviceController()
optimizer = OptimizationEngine()

@app.post("/iot/telemetry")
def ingest_telemetry(payload: dict):
    telemetry_db.save(payload)
    return {"status": "ok"}

@app.post("/iot/device-control/{device_id}/command")
def send_command(device_id: str, command: dict):
    controller.execute(device_id, command)
    return {"status": "sent", "deviceId": device_id}

@app.post("/iot/optimization/apply")
def apply_optimization(payload: dict):
    optimizer.apply(payload)
    return {"status": "accepted", "scenarioId": payload.get("scenarioId")}
