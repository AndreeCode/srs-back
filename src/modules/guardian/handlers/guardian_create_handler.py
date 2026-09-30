from typing import Optional
from uuid import UUID, uuid4

from asyncpg.exceptions import CheckViolationError, ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ..domain.guardian_domain import Guardian
from ..domain.guardian_errors import GuardianValidationError
from ..services.guardians_service import guardianService
from .guardian_errors_handler import unique_violation_error


class GuardianCreateRequest(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    dni: str = Field(pattern=r"^[0-9]{8}$")
    phone: Optional[str] = Field(default=None, max_length=50)
    email: Optional[str] = Field(default=None, max_length=255)
    user_id: Optional[UUID] = None
    account_username: Optional[str] = Field(default=None, min_length=3, max_length=100)
    account_password: Optional[str] = Field(default=None, min_length=6, max_length=100)


async def create_guardian_handler(body: GuardianCreateRequest):
    try:
        with_account = bool(body.account_username and body.account_password)

        if with_account:
            if body.user_id is not None:
                return error(400, "Elige una cuenta existente o crea una nueva, no ambas", ValueError("user_id+account"))
            await guardianService.check_account(None, body.account_username)

        guardian = Guardian(
            id=uuid4(),
            full_name=body.full_name,
            dni=body.dni,
            phone=body.phone,
            email=body.email,
            user_id=body.user_id,
        )

        created = await guardianService.create(guardian)

        if with_account:
            created = await guardianService.create_account(created, body.account_username, body.account_password)
            return success(201, "Padre registrado con su cuenta del portal", created.to_dict())

        return success(201, "Apoderado creado correctamente", created.to_dict())

    except GuardianValidationError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return unique_violation_error(err)

    except ForeignKeyViolationError as err:
        return error(400, "El user_id indicado no existe", err)

    except CheckViolationError as err:
        return error(400, "El usuario vinculado debe tener el rol guardian", err)

    except Exception as err:
        return error(500, "Error al crear el apoderado", err)
