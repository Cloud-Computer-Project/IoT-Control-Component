# src/models.py
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# -----------------------------
# Telemetry
# -----------------------------
class TelemetryPacket(BaseModel):
    deviceId: str = Field(..., min_length=1)
    timestamp: datetime
    metrics: Dict[str, Any]


class TelemetryIngestResponse(BaseModel):
    status: str = "ok"
    receivedAt: datetime


class TelemetryBulkRequest(BaseModel):
    batch: List[TelemetryPacket]


class TelemetryBulkResponse(BaseModel):
    status: str = "ok"
    itemsProcessed: int


class TelemetryHistoryItem(BaseModel):
    timestamp: datetime
    metrics: Dict[str, Any]


class TelemetryHistoryResponse(BaseModel):
    deviceId: str
    timeRange: Dict[str, datetime]  # {"from": ..., "to": ...}
    telemetry: List[TelemetryHistoryItem]


# -----------------------------
# Devices
# -----------------------------
class DeviceRegisterRequest(BaseModel):
    id: str = Field(..., min_length=1)
    type: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    capabilities: List[str] = []


class DeviceRegisterResponse(BaseModel):
    status: str = "registered"
    deviceId: str


class DeviceListItem(BaseModel):
    id: str
    type: str
    location: str
    status: str
    lastSeen: Optional[datetime] = None


class DeviceListResponse(BaseModel):
    devices: List[DeviceListItem]


class DeviceDetailsResponse(BaseModel):
    id: str
    type: str
    model: Optional[str] = None
    status: str
    location: str
    capabilities: List[str] = []
    lastTelemetry: Optional[Dict[str, Any]] = None


# -----------------------------
# Device control
# -----------------------------
class DeviceCommandRequest(BaseModel):
    command: str = Field(..., min_length=1)
    params: Dict[str, Any] = {}


class DeviceCommandResponse(BaseModel):
    status: str = "sent"
    deviceId: str
    commandId: str


class CommandLogItem(BaseModel):
    commandId: str
    command: str
    status: str  # sent | executed | failed
    sentAt: datetime
    executedAt: Optional[datetime] = None


class CommandHistoryResponse(BaseModel):
    deviceId: str
    commands: List[CommandLogItem]


# -----------------------------
# Optimization
# -----------------------------
class OptimizationAction(BaseModel):
    deviceId: str = Field(..., min_length=1)
    command: str = Field(..., min_length=1)
    params: Dict[str, Any] = {}
    executeAt: Optional[datetime] = None


class OptimizationApplyRequest(BaseModel):
    scenarioId: str = Field(..., min_length=1)
    generatedAt: datetime
    actions: List[OptimizationAction]


class OptimizationApplyResponse(BaseModel):
    status: str = "accepted"
    scenarioId: str


class OptimizationStatusResponse(BaseModel):
    scenarioId: str
    status: str  # accepted | in-progress | completed | failed
    actionsCompleted: int
    totalActions: int


# -----------------------------
# State
# -----------------------------
class LiveStateDeviceItem(BaseModel):
    id: str
    metrics: Dict[str, Any]


class LiveStateResponse(BaseModel):
    timestamp: datetime
    devices: List[LiveStateDeviceItem]
