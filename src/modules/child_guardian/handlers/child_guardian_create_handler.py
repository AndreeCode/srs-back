from typing import Optional
from uuid import UUID

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ..domain.child_guardian_domain import ChildGuardian
from ..domain.child_guardian_errors import ChildGuardianValidationError
from ..services.child_guardians_service import childGuardianService


class ChildGuardianCreateRequest(BaseModel):
    child_id: UUID
    guardian_id: UUID
    relationship: Optional[str] = Field(default=None, min_length=1, max_length=50)


async def create_child_guardian_handler(body: ChildGuardianCreateRequest):
    try:
        child_guardian = ChildGuardian(
            child_id=body.child_id,
            guardian_id=body.guardian_id,
            relationship=body.relationship,
        )

        created = await childGuardianService.create(child_guardian)
        return success(201, "Apoderado vinculado al nino correctamente", created.to_dict())

    except ChildGuardianValidationError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return error(409, "El apoderado ya esta vinculado a ese nino", err)

    except ForeignKeyViolationError as err:
        if err.constraint_name == "child_guardian_guardian_id_fkey":
            return error(400, "El guardian_id indicado no existe", err)
        return error(400, "El child_id indicado no existe", err)

    except Exception as err:
        return error(500, "Error al vincular el apoderado", err)
