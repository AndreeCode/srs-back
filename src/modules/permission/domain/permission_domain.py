from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class Permission:
    id: UUID
    code: str
    description: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "Permission":
        return cls(id=row["id"], code=row["code"], description=row["description"])

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "code": self.code,
            "description": self.description,
        }
