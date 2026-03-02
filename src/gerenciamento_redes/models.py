from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

DeviceStatus = Literal["ativo", "manutencao", "inativo"]


@dataclass(slots=True)
class NetworkDevice:
    id: int | None
    name: str
    ip_address: str
    device_type: str
    status: DeviceStatus = "ativo"
    created_at: datetime | None = None
