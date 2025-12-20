# src/devices.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from .deps import get_store
from .models import (
    DeviceDetailsResponse,
    DeviceListItem,
    DeviceListResponse,
    DeviceRegisterRequest,
    DeviceRegisterResponse,
)
from .storage import InMemoryStore

router = APIRouter()


@router.post("/iot/devices/register", response_model=DeviceRegisterResponse)
def register_device(
    payload: DeviceRegisterRequest,
    store: InMemoryStore = Depends(get_store),
):
    store.register_device(
        device_id=payload.id,
        type_=payload.type,
        location=payload.location,
        capabilities=payload.capabilities,
    )
    return DeviceRegisterResponse(status="registered", deviceId=payload.id)


@router.get("/iot/devices", response_model=DeviceListResponse)
def list_devices(store: InMemoryStore = Depends(get_store)):
    devices = []
    for d in store.list_devices():
        devices.append(
            DeviceListItem(
                id=d.id,
                type=d.type,
                location=d.location,
                status=d.status,
                lastSeen=d.last_seen,
            )
        )
    return DeviceListResponse(devices=devices)


@router.get("/iot/devices/{deviceId}", response_model=DeviceDetailsResponse)
def device_details(deviceId: str, store: InMemoryStore = Depends(get_store)):
    dev = store.get_device(deviceId)
    if not dev:
        raise HTTPException(status_code=404, detail="Device not found")

    return DeviceDetailsResponse(
        id=dev.id,
        type=dev.type,
        model=dev.model,
        status=dev.status,
        location=dev.location,
        capabilities=dev.capabilities,
        lastTelemetry=dev.last_telemetry,
    )
