# src/telemetry.py
from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query

from .deps import get_store
from .models import (
    TelemetryBulkRequest,
    TelemetryBulkResponse,
    TelemetryHistoryResponse,
    TelemetryIngestResponse,
    TelemetryPacket,
)
from .storage import InMemoryStore

router = APIRouter()


@router.post("/iot/telemetry", response_model=TelemetryIngestResponse)
def ingest_telemetry(payload: TelemetryPacket, store: InMemoryStore = Depends(get_store)):
    store.save_telemetry(payload.deviceId, payload.timestamp, payload.metrics)
    return TelemetryIngestResponse(status="ok", receivedAt=datetime.utcnow())


@router.post("/iot/telemetry/bulk", response_model=TelemetryBulkResponse)
def ingest_telemetry_bulk(payload: TelemetryBulkRequest, store: InMemoryStore = Depends(get_store)):
    for item in payload.batch:
        store.save_telemetry(item.deviceId, item.timestamp, item.metrics)
    return TelemetryBulkResponse(status="ok", itemsProcessed=len(payload.batch))


@router.get("/iot/telemetry/history", response_model=TelemetryHistoryResponse)
def telemetry_history(
    deviceId: str = Query(...),
    from_: datetime = Query(..., alias="from"),
    to: datetime = Query(...),
    store: InMemoryStore = Depends(get_store),
):
    if from_ > to:
        raise HTTPException(status_code=400, detail="'from' must be <= 'to'")

    rows = store.telemetry_history(deviceId, from_, to)
    return TelemetryHistoryResponse(
        deviceId=deviceId,
        timeRange={"from": from_, "to": to},
        telemetry=rows,
    )
