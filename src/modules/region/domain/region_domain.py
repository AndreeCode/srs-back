from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class Region:
    id: UUID
    name: str
    health_network: Optional[str] = None
    active: bool = True

    @classmethod
    def from_row(cls, row) -> "Region":
        return cls(
            id=row["id"],
            name=row["name"],
            health_network=row["health_network"],
            active=row["active"],
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "health_network": self.health_network,
            "active": self.active,
        }
