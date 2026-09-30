from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from fastapi import Request
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ..domain.child_domain import BirthCondition, Child, Gender
from ..domain.child_errors import ChildValidationError
from ..services.children_service import childService
from .child_errors_handler import foreign_key_violation_error, unique_violation_error


class ChildCreateRequest(BaseModel):
    padron_code: str = Field(min_length=1, max_length=50)
    medical_record_code: Optional[str] = Field(default=None, max_length=100)
    dni: Optional[str] = Field(default=None, pattern=r"^[0-9]{8}$")
    first_names: str = Field(min_length=1, max_length=150)
    last_names: str = Field(min_length=1, max_length=150)
    birth_date: date
    gender: Optional[Gender] = None
    birth_condition: BirthCondition = "none"
    mother_name: Optional[str] = Field(default=None, max_length=200)
    mother_dni: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=300)
    contact_phone: Optional[str] = Field(default=None, max_length=50)
    insurance: Optional[str] = Field(default=None, max_length=100)
    health_facility_id: UUID


async def create_child_handler(request: Request, body: ChildCreateRequest):
    try:
        child = Child(
            id=uuid4(),
            padron_code=body.padron_code,
            medical_record_code=body.medical_record_code,
            dni=body.dni,
            first_names=body.first_names,
            last_names=body.last_names,
            birth_date=body.birth_date,
            gender=body.gender,
            birth_condition=body.birth_condition,
            mother_name=body.mother_name,
            mother_dni=body.mother_dni,
            address=body.address,
            contact_phone=body.contact_phone,
            insurance=body.insurance,
            health_facility_id=body.health_facility_id,
            registered_by=UUID(request.state.user["sub"]),
        )

        created = await childService.create(child)
        return success(201, "Nino registrado correctamente", created.to_dict())

    except ChildValidationError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return unique_violation_error(err)

    except ForeignKeyViolationError as err:
        return foreign_key_violation_error(err)

    except Exception as err:
        return error(500, "Error al registrar el nino", err)
