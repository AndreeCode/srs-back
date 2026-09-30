from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class ChildGuardian:
    child_id: UUID
    guardian_id: UUID
    relationship: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "ChildGuardian":
        return cls(
            child_id=row["child_id"],
            guardian_id=row["guardian_id"],
            relationship=row["relationship"],
        )

    def to_dict(self) -> dict:
        return {
            "child_id": str(self.child_id),
            "guardian_id": str(self.guardian_id),
            "relationship": self.relationship,
        }
