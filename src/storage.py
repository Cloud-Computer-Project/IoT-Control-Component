# src/storage.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4


# -----------------------------
# Internal data structures
# -----------------------------
@dataclass
class Device:
    id: str
    type: str
    location: str
    capabilities: List[str] = field(default_factory=list)
    model: Optional[str] = None
    status: str = "online"
    last_seen: Optional[datetime] = None
    last_telemetry: Optional[Dict[str, Any]] = None


@dataclass
class CommandLog:
    command_id: str
    device_id: str
    command: str
    params: Dict[str, Any]
    status: str  # sent | executed | failed
    sent_at: datetime
    executed_at: Optional[datetime] = None


@dataclass
class OptimizationScenario:
    scenario_id: str
    generated_at: datetime
    total_actions: int
    actions_completed: int = 0
    status: str = "accepted"  # accepted | in-progress | completed | failed
    actions: List[Dict[str, Any]] = field(default_factory=list)


# -----------------------------
# In-memory "database"
# -----------------------------
class InMemoryStore:
    """
    Simple in-memory storage used for integration/demo purposes.
    In a real deployment, you would replace this with a DB layer.
    """

    def __init__(self) -> None:
        self.devices: Dict[str, Device] = {}
        self.telemetry: Dict[str, List[Dict[str, Any]]] = {}     # deviceId -> [{"timestamp": dt, "metrics": {...}}]
        self.commands: Dict[str, List[CommandLog]] = {}          # deviceId -> [CommandLog,...]
        self.optimizations: Dict[str, OptimizationScenario] = {} # scenarioId -> OptimizationScenario

    # -------------------------
    # Devices
    # -------------------------
    def register_device(self, device_id: str, type_: str, location: str, capabilities: List[str]) -> Device:
        dev = Device(id=device_id, type=type_, location=location, capabilities=capabilities)
        self.devices[device_id] = dev
        return dev

    def get_device(self, device_id: str) -> Optional[Device]:
        return self.devices.get(device_id)

    def list_devices(self) -> List[Device]:
        return list(self.devices.values())

    # -------------------------
    # Telemetry
    # -------------------------
    def save_telemetry(self, device_id: str, timestamp: datetime, metrics: Dict[str, Any]) -> None:
        self.telemetry.setdefault(device_id, []).append({"timestamp": timestamp, "metrics": metrics})

        # update device live snapshot if device is known
        dev = self.devices.get(device_id)
        if dev:
            dev.last_seen = timestamp
            dev.last_telemetry = metrics
            dev.status = "online"

    def telemetry_history(self, device_id: str, from_ts: datetime, to_ts: datetime) -> List[Dict[str, Any]]:
        rows = self.telemetry.get(device_id, [])
        # keep within range inclusive
        return [r for r in rows if from_ts <= r["timestamp"] <= to_ts]

    def live_state_all(self) -> List[Dict[str, Any]]:
        """
        Returns: [{"id": "...", "metrics": {...}}, ...] for devices with known last telemetry.
        """
        out: List[Dict[str, Any]] = []
        for dev in self.devices.values():
            if dev.last_telemetry is not None:
                out.append({"id": dev.id, "metrics": dev.last_telemetry})
        return out

    def live_state_one(self, device_id: str) -> Optional[Dict[str, Any]]:
        dev = self.devices.get(device_id)
        if not dev or dev.last_telemetry is None:
            return None
        return {"id": dev.id, "metrics": dev.last_telemetry}

    # -------------------------
    # Commands
    # -------------------------
    def add_command(self, device_id: str, command: str, params: Dict[str, Any]) -> CommandLog:
        cmd_id = f"cmd-{uuid4().hex[:8]}"
        now = datetime.utcnow()

        log = CommandLog(
            command_id=cmd_id,
            device_id=device_id,
            command=command,
            params=params,
            status="sent",
            sent_at=now,
            executed_at=None,
        )
        self.commands.setdefault(device_id, []).append(log)
        return log

    def mark_command_executed(self, device_id: str, command_id: str) -> None:
        logs = self.commands.get(device_id, [])
        now = datetime.utcnow()
        for l in logs:
            if l.command_id == command_id:
                l.status = "executed"
                l.executed_at = now
                return

    def command_history(self, device_id: str) -> List[CommandLog]:
        return list(self.commands.get(device_id, []))

    # -------------------------
    # Optimization scenarios
    # -------------------------
    def save_optimization(self, scenario_id: str, generated_at: datetime, actions: List[Dict[str, Any]]) -> OptimizationScenario:
        sc = OptimizationScenario(
            scenario_id=scenario_id,
            generated_at=generated_at,
            total_actions=len(actions),
            actions_completed=0,
            status="accepted",
            actions=actions,
        )
        self.optimizations[scenario_id] = sc
        return sc

    def get_optimization(self, scenario_id: str) -> Optional[OptimizationScenario]:
        return self.optimizations.get(scenario_id)

    def set_optimization_progress(self, scenario_id: str, actions_completed: int, status: Optional[str] = None) -> None:
        sc = self.optimizations.get(scenario_id)
        if not sc:
            return
        sc.actions_completed = max(0, min(actions_completed, sc.total_actions))
        if status:
            sc.status = status
        else:
            # auto status
            if sc.actions_completed == 0:
                sc.status = "accepted"
            elif sc.actions_completed < sc.total_actions:
                sc.status = "in-progress"
            else:
                sc.status = "completed"
