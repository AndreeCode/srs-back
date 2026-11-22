from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field

from ....core.config.config import config
from ....core.db.sqlserver import SqlServerUnavailableError
from ....core.http.error import error
from ....core.http.succes import success
from ...guardian.domain.guardian_errors import (
    GuardianChildNotFoundError,
    GuardianConflictError,
    GuardianValidationError,
)
from ...guardian.services.guardians_service import guardianService

Relationship = Literal["Madre", "Padre", "Apoderado"]


class RegisterRequest(BaseModel):
    dni: str = Field(pattern=r"^\d{8}$")
    full_name: str = Field(min_length=3, max_length=150)
    phone: Optional[str] = Field(default=None, pattern=r"^\d{9}$")
    email: Optional[EmailStr] = None
    password: str = Field(min_length=8, max_length=128)
    child_identifier: str = Field(min_length=3, max_length=50)
    child_birth_date: date
    relationship: Relationship = "Madre"


async def register_handler(body: RegisterRequest):
    if not config.public_registration:
        return error(403, "El registro de padres lo hace por ahora tu establecimiento de salud (admin o coordinador)", PermissionError("PUBLIC_REGISTRATION=false"))

    try:
        if body.child_birth_date > date.today():
            return error(400, "La fecha de nacimiento del nino no puede ser futura", ValueError("future birth date"))

        data = await guardianService.register(
            dni=body.dni,
            full_name=" ".join(body.full_name.split()),
            phone=body.phone,
            email=str(body.email) if body.email else None,
            password=body.password,
            child_identifier=body.child_identifier,
            child_birth_date=body.child_birth_date,
            relationship=body.relationship,
        )
        return success(201, "Cuenta creada correctamente, ya puedes iniciar sesion", data)

    except GuardianConflictError as err:
        return error(409, str(err), err)

    except GuardianChildNotFoundError as err:
        return error(404, str(err), err)

    except GuardianValidationError as err:
        return error(400, str(err), err)

    except SqlServerUnavailableError as err:
        return error(503, f"{err}. No se pudo verificar al nino, intenta mas tarde", err)

    except Exception as err:
        return error(500, "Error al registrar la cuenta", err)
