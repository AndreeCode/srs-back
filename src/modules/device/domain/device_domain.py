from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

BlockScope = Literal["account", "browser"]


@dataclass
class Device:
    id: UUID
    user_id: UUID
    device_hash: str
    user_agent: Optional[str] = None
    first_seen_at: Optional[datetime] = None
    last_seen_at: Optional[datetime] = None
    trusted: bool = True
    block_scope: Optional[BlockScope] = None
    blocked_reason: Optional[str] = None
    blocked_at: Optional[datetime] = None
    blocked_by: Optional[UUID] = None

    @classmethod
    def from_row(cls, row) -> "Device":
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            device_hash=row["device_hash"],
            user_agent=row["user_agent"],
            first_seen_at=row["first_seen_at"],
            last_seen_at=row["last_seen_at"],
            trusted=row["trusted"],
            block_scope=row["block_scope"],
            blocked_reason=row["blocked_reason"],
            blocked_at=row["blocked_at"],
            blocked_by=row["blocked_by"],
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "browser": self.device_hash[:10],
            "user_agent": self.user_agent,
            "first_seen_at": self.first_seen_at.isoformat() if self.first_seen_at else None,
            "last_seen_at": self.last_seen_at.isoformat() if self.last_seen_at else None,
            "trusted": self.trusted,
            "block_scope": self.block_scope,
            "blocked_reason": self.blocked_reason,
            "blocked_at": self.blocked_at.isoformat() if self.blocked_at else None,
            "blocked_by": str(self.blocked_by) if self.blocked_by else None,
        }
