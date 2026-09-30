from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal, Optional
from uuid import UUID

BirthCondition = Literal["none", "premature", "low_weight", "premature_low_weight"]
Gender = Literal["M", "F"]


@dataclass
class Child:
    id: UUID
    padron_code: str
    first_names: str
    last_names: str
    birth_date: date
    health_facility_id: UUID
    medical_record_code: Optional[str] = None
    dni: Optional[str] = None
    gender: Optional[Gender] = None
    birth_condition: BirthCondition = "none"
    mother_name: Optional[str] = None
    mother_dni: Optional[str] = None
    address: Optional[str] = None
    contact_phone: Optional[str] = None
    insurance: Optional[str] = None
    active: bool = True
    registered_by: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row) -> "Child":
        return cls(
            id=row["id"],
            padron_code=row["padron_code"],
            first_names=row["first_names"],
            last_names=row["last_names"],
            birth_date=row["birth_date"],
            health_facility_id=row["health_facility_id"],
            medical_record_code=row["medical_record_code"],
            dni=row["dni"],
            gender=row["gender"],
            birth_condition=row["birth_condition"],
            mother_name=row["mother_name"],
            mother_dni=row["mother_dni"],
            address=row["address"],
            contact_phone=row["contact_phone"],
            insurance=row["insurance"],
            active=row["active"],
            registered_by=row["registered_by"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "padron_code": self.padron_code,
            "medical_record_code": self.medical_record_code,
            "dni": self.dni,
            "first_names": self.first_names,
            "last_names": self.last_names,
            "birth_date": self.birth_date.isoformat(),
            "gender": self.gender,
            "birth_condition": self.birth_condition,
            "mother_name": self.mother_name,
            "mother_dni": self.mother_dni,
            "address": self.address,
            "contact_phone": self.contact_phone,
            "insurance": self.insurance,
            "health_facility_id": str(self.health_facility_id),
            "active": self.active,
            "registered_by": str(self.registered_by) if self.registered_by else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
