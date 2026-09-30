from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class CareService:
    id: UUID
    package_id: UUID
    code: str
    name: str
    min_age_days: int
    max_age_days: int
    group_name: str = "DIRECT"
    group_order: int = 1
    sort_order: int = 1
    min_interval_days: int = 0
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row) -> "CareService":
        return cls(
            id=row["id"],
            package_id=row["package_id"],
            code=row["code"],
            name=row["name"],
            min_age_days=row["min_age_days"],
            max_age_days=row["max_age_days"],
            group_name=row["group_name"],
            group_order=row["group_order"],
            sort_order=row["sort_order"],
            min_interval_days=row["min_interval_days"],
            active=row["active"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "package_id": str(self.package_id),
            "code": self.code,
            "name": self.name,
            "group_name": self.group_name,
            "group_order": self.group_order,
            "sort_order": self.sort_order,
            "min_age_days": self.min_age_days,
            "max_age_days": self.max_age_days,
            "min_interval_days": self.min_interval_days,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
