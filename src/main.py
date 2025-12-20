# src/main.py
from __future__ import annotations

from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException

from .storage import InMemoryStore
from .models import LiveStateDeviceItem, LiveStateResponse
from .deps import get_store
from . import telemetry, devices, device_control, optimization

app = FastAPI(title="EMSIB IoT & Control Component", version="2.0")

# shared store for the whole app
app.state.store = InMemoryStore()

# routers
app.include_router(telemetry.router)
app.include_router(devices.router)
app.include_router(device_control.router)
app.include_router(optimization.router)


@app.get("/iot/state/live", response_model=LiveStateResponse)
def state_live(store: InMemoryStore = Depends(get_store)):
    snapshot = store.live_state_all()
    return LiveStateResponse(
        timestamp=datetime.utcnow(),
        devices=[LiveStateDeviceItem(id=d["id"], metrics=d["metrics"]) for d in snapshot],
    )


@app.get("/iot/state/{deviceId}")
def state_device(deviceId: str, store: InMemoryStore = Depends(get_store)):
    state = store.live_state_one(deviceId)
    if not state:
        raise HTTPException(status_code=404, detail="No state for this device (not found or no telemetry yet)")
    return state
