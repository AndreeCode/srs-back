from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class HealthFacility:
    id: UUID
    name: str
    region_id: UUID
    active: bool = True
    created_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row) -> "HealthFacility":
        return cls(
            id=row["id"],
            name=row["name"],
            region_id=row["region_id"],
            active=row["active"],
            created_at=row["created_at"],
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "region_id": str(self.region_id),
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
