import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal, Optional
from uuid import UUID

AuditAction = Literal["INSERT", "UPDATE", "DELETE", "LOGIN", "LOGIN_FAILED", "LOGOUT", "PASSWORD_CHANGED", "ACCOUNT_LOCKED"]


@dataclass
class AuditLog:
    id: UUID
    action: str
    result: str
    created_at: datetime
    user_id: Optional[UUID] = None
    device_id: Optional[UUID] = None
    affected_table: Optional[str] = None
    record_id: Optional[UUID] = None
    record_key: Optional[Any] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Optional[Any] = None

    @classmethod
    def from_row(cls, row) -> "AuditLog":
        return cls(
            id=row["id"],
            action=row["action"],
            result=row["result"],
            created_at=row["created_at"],
            user_id=row["user_id"],
            device_id=row["device_id"],
            affected_table=row["affected_table"],
            record_id=row["record_id"],
            record_key=json.loads(row["record_key"]) if row["record_key"] else None,
            ip_address=str(row["ip_address"]) if row["ip_address"] is not None else None,
            user_agent=row["user_agent"],
            details=json.loads(row["details"]) if row["details"] else None,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "device_id": str(self.device_id) if self.device_id else None,
            "action": self.action,
            "affected_table": self.affected_table,
            "record_id": str(self.record_id) if self.record_id else None,
            "record_key": self.record_key,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "result": self.result,
            "details": self.details,
            "created_at": self.created_at.isoformat(),
        }
