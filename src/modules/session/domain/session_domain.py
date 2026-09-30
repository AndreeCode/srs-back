from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Session:
    id: UUID
    user_id: UUID
    device_id: UUID
    token_hash: str
    expires_at: datetime
    ip_address: Optional[str] = None
    created_at: Optional[datetime] = None
    revoked: bool = False
    revoked_reason: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "Session":
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            device_id=row["device_id"],
            token_hash=row["token_hash"],
            expires_at=row["expires_at"],
            ip_address=str(row["ip_address"]) if row["ip_address"] is not None else None,
            created_at=row["created_at"],
            revoked=row["revoked"],
            revoked_reason=row["revoked_reason"],
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "device_id": str(self.device_id),
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat(),
            "revoked": self.revoked,
            "revoked_reason": self.revoked_reason,
        }
