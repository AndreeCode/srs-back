from typing import Optional
from uuid import UUID

from asyncpg.exceptions import CheckViolationError, ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.guardian_domain import Guardian
from ..domain.guardian_errors import GuardianValidationError
from ..services.guardians_service import guardianService
from .guardian_errors_handler import unique_violation_error


class GuardianUpdateRequest(BaseModel):
    full_name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    dni: Optional[str] = Field(default=None, pattern=r"^[0-9]{8}$")
    phone: Optional[str] = Field(default=None, max_length=50)
    email: Optional[str] = Field(default=None, max_length=255)
    user_id: Optional[UUID] = None
    active: Optional[bool] = None
    account_username: Optional[str] = Field(default=None, min_length=3, max_length=100)
    account_password: Optional[str] = Field(default=None, min_length=6, max_length=100)


async def update_guardian_handler(guardian_id: str, body: GuardianUpdateRequest):
    try:
        guardian_uuid = parse_uuid(guardian_id, "guardian_id")
        current = await guardianService.get_by_id(guardian_uuid)

        if current is None:
            return error(404, "Apoderado no encontrado", ValueError(f"guardian_id={guardian_id}"))

        sent = body.model_fields_set

        guardian = Guardian(
            id=current.id,
            full_name=body.full_name if body.full_name is not None else current.full_name,
            dni=body.dni if body.dni is not None else current.dni,
            phone=body.phone if "phone" in sent else current.phone,
            email=body.email if "email" in sent else current.email,
            user_id=body.user_id if "user_id" in sent else current.user_id,
            active=body.active if body.active is not None else current.active,
        )

        with_account = bool(body.account_username and body.account_password)

        if with_account:
            await guardianService.check_account(guardian, body.account_username)

        updated = await guardianService.update(guardian, current)

        if updated is None:
            return error(404, "Apoderado no encontrado", ValueError(f"guardian_id={guardian_id}"))

        if with_account:
            updated = await guardianService.create_account(updated, body.account_username, body.account_password)
            return success(200, "Datos actualizados y cuenta del portal creada", updated.to_dict())

        return success(200, "Apoderado actualizado correctamente", updated.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except GuardianValidationError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return unique_violation_error(err)

    except ForeignKeyViolationError as err:
        return error(400, "El user_id indicado no existe", err)

    except CheckViolationError as err:
        return error(400, "El usuario vinculado debe tener el rol guardian", err)

    except Exception as err:
        return error(500, "Error al actualizar el apoderado", err)
