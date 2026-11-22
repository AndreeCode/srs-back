from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

DOCUMENT_TYPES = {1: "DNI", 6: "CNV"}

EARLY_TOLERANCE_DAYS = 7

LOW_WEIGHT_CODES = ("P070", "P071")
PREMATURE_CODES = ("P072", "P073")


def as_date(value) -> Optional[date]:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def clean(value) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def measure(value) -> Optional[str]:
    if value is None:
        return None
    number = Decimal(str(value))
    return None if number == 0 else f"{number.normalize():f}"


@dataclass
class HisChild:
    document_number: str
    document_type: str
    birth_date: date
    gender: Optional[str] = None
    facility_name: Optional[str] = None
    micro_red: Optional[str] = None
    red: Optional[str] = None
    patient_ids: list[str] = field(default_factory=list)

    @property
    def portal_id(self) -> str:
        return f"his-{self.document_number}"

    @classmethod
    def from_rows(cls, rows: list[dict]) -> "HisChild":
        first = rows[0]
        gender = clean(first["Id_Genero"])
        return cls(
            document_number=clean(first["Numero_Documento_Paciente"]),
            document_type=DOCUMENT_TYPES.get(first["Id_Tipo_Documento_Paciente"], "OTRO"),
            birth_date=as_date(first["Fecha_Nacimiento_Paciente"]),
            gender=gender if gender in ("M", "F") else None,
            facility_name=clean(first["Nombre_Establecimiento"]),
            micro_red=clean(first["MicroRed"]),
            red=clean(first["Red"]),
            patient_ids=[row["Id_Paciente"] for row in rows],
        )

    def to_dict(self) -> dict:
        return {
            "document_number": self.document_number,
            "document_type": self.document_type,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "gender": self.gender,
            "facility_name": self.facility_name,
            "micro_red": self.micro_red,
            "red": self.red,
        }


@dataclass
class HisAttention:
    patient_id: str
    attention_date: date
    code: str
    description: Optional[str]
    dose_id: Optional[int]
    dose: Optional[str]
    lab_value: Optional[str]
    batch: Optional[str]
    page: Optional[str]
    record: Optional[str]
    weight: Optional[str]
    height: Optional[str]
    hemoglobin: Optional[str]
    facility_name: Optional[str]

    @classmethod
    def from_row(cls, row: dict) -> "HisAttention":
        return cls(
            patient_id=row["Id_Paciente"],
            attention_date=as_date(row["Fecha_Atencion"]),
            code=clean(row["Codigo_Item"]) or "",
            description=clean(row["Descripcion_Item"]),
            dose_id=row["Id_Dosis"],
            dose=clean(row["Dosis"]),
            lab_value=clean(row["Valor_Lab"]),
            batch=clean(row["Lote"]),
            page=clean(row["Num_Pag"]),
            record=clean(row["Num_Reg"]),
            weight=measure(row["Peso"]),
            height=measure(row["Talla"]),
            hemoglobin=measure(row["Hemoglobina"]),
            facility_name=clean(row["Nombre_Establecimiento"]),
        )

    def notes(self) -> str:
        parts = [f"HIS {self.code}" + (f" · {self.description}" if self.description else "")]
        if self.dose:
            parts.append(self.dose)
        if self.lab_value:
            parts.append(f"Lab {self.lab_value}")
        if self.weight:
            parts.append(f"Peso {self.weight} kg")
        if self.height:
            parts.append(f"Talla {self.height} cm")
        if self.hemoglobin:
            parts.append(f"Hb {self.hemoglobin} g/dL")
        return " · ".join(parts)

    def to_dict(self) -> dict:
        return {
            "attention_date": self.attention_date.isoformat() if self.attention_date else None,
            "code": self.code,
            "description": self.description,
            "dose": self.dose,
            "lab_value": self.lab_value,
            "batch": self.batch,
            "page": self.page,
            "record": self.record,
            "weight": self.weight,
            "height": self.height,
            "hemoglobin": self.hemoglobin,
            "facility_name": self.facility_name,
        }


@dataclass
class HisRule:
    his_code: str
    service_id: UUID
    dose_id: Optional[int] = None
    lab_value: Optional[str] = None
    priority: int = 0

    @classmethod
    def from_row(cls, row) -> "HisRule":
        return cls(
            his_code=row["his_code"],
            service_id=row["service_id"],
            dose_id=row["dose_id"],
            lab_value=row["lab_value"],
            priority=row["priority"],
        )


def birth_condition(attentions: list[HisAttention]) -> str:
    codes = {attention.code.upper() for attention in attentions}
    low = any(code.startswith(LOW_WEIGHT_CODES) for code in codes)
    premature = any(code.startswith(PREMATURE_CODES) for code in codes)
    if low and premature:
        return "premature_low_weight"
    if premature:
        return "premature"
    if low:
        return "low_weight"
    return "none"
