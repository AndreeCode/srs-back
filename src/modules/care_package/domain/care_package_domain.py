from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class CarePackage:
    id: UUID
    code: str
    name: str
    min_age_days: int
    max_age_days: int
    description: Optional[str] = None
    at_risk_newborn_only: bool = False
    sort_order: int = 1
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row) -> "CarePackage":
        return cls(
            id=row["id"],
            code=row["code"],
            name=row["name"],
            min_age_days=row["min_age_days"],
            max_age_days=row["max_age_days"],
            description=row["description"],
            at_risk_newborn_only=row["at_risk_newborn_only"],
            sort_order=row["sort_order"],
            active=row["active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "min_age_days": self.min_age_days,
            "max_age_days": self.max_age_days,
            "at_risk_newborn_only": self.at_risk_newborn_only,
            "sort_order": self.sort_order,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
