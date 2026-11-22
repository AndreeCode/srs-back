import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

AlertKind = Literal["shared_device", "many_devices", "brute_force_account", "brute_force_ip", "audit_chain_broken"]
AlertStatus = Literal["open", "resolved", "dismissed"]

SHARED_DEVICE_ACCOUNTS = 3
ACCOUNT_DEVICES = 3
WINDOW_DAYS = 30
QUIET_DAYS = 7
BRUTE_FORCE_ACCOUNT_FAILURES = 10
BRUTE_FORCE_IP_FAILURES = 20
BRUTE_FORCE_WINDOW_MINUTES = 60
BRUTE_FORCE_QUIET_DAYS = 1


@dataclass
class SecurityAlert:
    id: UUID
    kind: AlertKind
    subject: str
    user_id: Optional[UUID] = None
    device_hash: Optional[str] = None
    detail: dict = field(default_factory=dict)
    status: AlertStatus = "open"
    resolution: Optional[str] = None
    resolved_by: Optional[UUID] = None
    resolved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row) -> "SecurityAlert":
        detail = row["detail"]
        return cls(
            id=row["id"],
            kind=row["kind"],
            subject=row["subject"],
            user_id=row["user_id"],
            device_hash=row["device_hash"],
            detail=json.loads(detail) if isinstance(detail, str) else (detail or {}),
            status=row["status"],
            resolution=row["resolution"],
            resolved_by=row["resolved_by"],
            resolved_at=row["resolved_at"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "kind": self.kind,
            "user_id": str(self.user_id) if self.user_id else None,
            "browser": self.device_hash[:10] if self.device_hash else None,
            "detail": self.detail,
            "status": self.status,
            "resolution": self.resolution,
            "resolved_by": str(self.resolved_by) if self.resolved_by else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
