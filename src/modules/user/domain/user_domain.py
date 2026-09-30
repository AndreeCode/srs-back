from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class User:
    id: UUID
    username: str
    password_hash: str
    role_id: UUID
    full_name: str
    dni: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    terms_accepted: bool = False
    terms_version: Optional[str] = None
    terms_accepted_at: Optional[datetime] = None
    active: bool = True
    blocked: bool = False
    blocked_reason: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    region_ids: list[UUID] = field(default_factory=list)

    @classmethod
    def from_row(cls, row) -> "User":
        return cls(
            id=row["id"],
            username=row["username"],
            password_hash=row["password_hash"],
            role_id=row["role_id"],
            full_name=row["full_name"],
            dni=row["dni"],
            phone=row["phone"],
            email=row["email"],
            terms_accepted=row["terms_accepted"],
            terms_version=row["terms_version"],
            terms_accepted_at=row["terms_accepted_at"],
            active=row["active"],
            blocked=row["blocked"],
            blocked_reason=row["blocked_reason"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            region_ids=list(row.get("region_ids") or []),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "username": self.username,
            "role_id": str(self.role_id),
            "full_name": self.full_name,
            "dni": self.dni,
            "phone": self.phone,
            "email": self.email,
            "terms_accepted": self.terms_accepted,
            "terms_version": self.terms_version,
            "terms_accepted_at": self.terms_accepted_at.isoformat() if self.terms_accepted_at else None,
            "active": self.active,
            "blocked": self.blocked,
            "blocked_reason": self.blocked_reason,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "region_ids": [str(region_id) for region_id in self.region_ids],
        }
