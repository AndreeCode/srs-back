from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Guardian:
    id: UUID
    full_name: str
    dni: str
    phone: Optional[str] = None
    email: Optional[str] = None
    user_id: Optional[UUID] = None
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row) -> "Guardian":
        return cls(
            id=row["id"],
            full_name=row["full_name"],
            dni=row["dni"],
            phone=row["phone"],
            email=row["email"],
            user_id=row["user_id"],
            active=row["active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "full_name": self.full_name,
            "dni": self.dni,
            "phone": self.phone,
            "email": self.email,
            "user_id": str(self.user_id) if self.user_id else None,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
