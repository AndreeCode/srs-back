from dataclasses import dataclass, field
from typing import Literal
from uuid import UUID

RoleName = Literal["guardian", "health_staff", "admin"]


@dataclass
class Role:
    id: UUID
    name: RoleName
    is_active: bool = True
    permission_ids: list[UUID] = field(default_factory=list)

    @classmethod
    def from_row(cls, row) -> "Role":
        return cls(
            id=row["id"],
            name=row["name"],
            is_active=row["is_active"],
            permission_ids=list(row.get("permission_ids") or []),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "is_active": self.is_active,
            "permission_ids": [str(permission_id) for permission_id in self.permission_ids],
        }
