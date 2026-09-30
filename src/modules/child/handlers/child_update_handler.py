from datetime import date
from typing import Optional
from uuid import UUID

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.child_domain import BirthCondition, Child, Gender
from ..domain.child_errors import ChildValidationError
from ..services.children_service import childService
from .child_errors_handler import foreign_key_violation_error, unique_violation_error


class ChildUpdateRequest(BaseModel):
    padron_code: Optional[str] = Field(default=None, min_length=1, max_length=50)
    medical_record_code: Optional[str] = Field(default=None, max_length=100)
    dni: Optional[str] = Field(default=None, pattern=r"^[0-9]{8}$")
    first_names: Optional[str] = Field(default=None, min_length=1, max_length=150)
    last_names: Optional[str] = Field(default=None, min_length=1, max_length=150)
    birth_date: Optional[date] = None
    gender: Optional[Gender] = None
    birth_condition: Optional[BirthCondition] = None
    mother_name: Optional[str] = Field(default=None, max_length=200)
    mother_dni: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=300)
    contact_phone: Optional[str] = Field(default=None, max_length=50)
    insurance: Optional[str] = Field(default=None, max_length=100)
    health_facility_id: Optional[UUID] = None
    active: Optional[bool] = None


async def update_child_handler(child_id: str, body: ChildUpdateRequest):
    try:
        child_uuid = parse_uuid(child_id, "child_id")
        current = await childService.get_by_id(child_uuid)

        if current is None:
            return error(404, "Nino no encontrado", ValueError(f"child_id={child_id}"))

        sent = body.model_fields_set

        child = Child(
            id=current.id,
            padron_code=body.padron_code if body.padron_code is not None else current.padron_code,
            medical_record_code=body.medical_record_code if "medical_record_code" in sent else current.medical_record_code,
            dni=body.dni if "dni" in sent else current.dni,
            first_names=body.first_names if body.first_names is not None else current.first_names,
            last_names=body.last_names if body.last_names is not None else current.last_names,
            birth_date=body.birth_date if body.birth_date is not None else current.birth_date,
            gender=body.gender if "gender" in sent else current.gender,
            birth_condition=body.birth_condition if body.birth_condition is not None else current.birth_condition,
            mother_name=body.mother_name if "mother_name" in sent else current.mother_name,
            mother_dni=body.mother_dni if "mother_dni" in sent else current.mother_dni,
            address=body.address if "address" in sent else current.address,
            contact_phone=body.contact_phone if "contact_phone" in sent else current.contact_phone,
            insurance=body.insurance if "insurance" in sent else current.insurance,
            health_facility_id=body.health_facility_id if body.health_facility_id is not None else current.health_facility_id,
            active=body.active if body.active is not None else current.active,
            registered_by=current.registered_by,
        )

        updated = await childService.update(child, current)

        if updated is None:
            return error(404, "Nino no encontrado", ValueError(f"child_id={child_id}"))

        return success(200, "Nino actualizado correctamente", updated.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except ChildValidationError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return unique_violation_error(err)

    except ForeignKeyViolationError as err:
        return foreign_key_violation_error(err)

    except Exception as err:
        return error(500, "Error al actualizar el nino", err)
