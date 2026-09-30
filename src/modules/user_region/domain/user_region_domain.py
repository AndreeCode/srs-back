from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserRegion:
    user_id: UUID
    region_id: UUID

    @classmethod
    def from_row(cls, row) -> "UserRegion":
        return cls(user_id=row["user_id"], region_id=row["region_id"])

    def to_dict(self) -> dict:
        return {
            "user_id": str(self.user_id),
            "region_id": str(self.region_id),
        }
