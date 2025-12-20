# src/device_control.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from .deps import get_store
from .models import (
    CommandHistoryResponse,
    CommandLogItem,
    DeviceCommandRequest,
    DeviceCommandResponse,
)
from .storage import InMemoryStore

router = APIRouter()


@router.post("/iot/device-control/{deviceId}/command", response_model=DeviceCommandResponse)
def send_command(
    deviceId: str,
    payload: DeviceCommandRequest,
    store: InMemoryStore = Depends(get_store),
):
    """
    Sends a command to a device for immediate execution (demo behavior).
    Spec: POST /iot/device-control/{deviceId}/command
    """
    dev = store.get_device(deviceId)
    if not dev:
        raise HTTPException(status_code=404, detail="Device not found")

    # Save command log and return a commandId
    log = store.add_command(device_id=deviceId, command=payload.command, params=payload.params)

    # Demo behavior: assume the command executes immediately
    store.mark_command_executed(device_id=deviceId, command_id=log.command_id)

    return DeviceCommandResponse(status="sent", deviceId=deviceId, commandId=log.command_id)


@router.get("/iot/device-control/{deviceId}/commands", response_model=CommandHistoryResponse)
def command_history(deviceId: str, store: InMemoryStore = Depends(get_store)):
    """
    Returns a history of commands issued to the device.
    Spec: GET /iot/device-control/{deviceId}/commands
    """
    dev = store.get_device(deviceId)
    if not dev:
        raise HTTPException(status_code=404, detail="Device not found")

    logs = store.command_history(deviceId)
    items = [
        CommandLogItem(
            commandId=l.command_id,
            command=l.command,
            status=l.status,
            sentAt=l.sent_at,
            executedAt=l.executed_at,
        )
        for l in logs
    ]

    return CommandHistoryResponse(deviceId=deviceId, commands=items)
