from typing import Optional
from uuid import uuid4

from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ..domain.permission_catalog import PERMISSION_CODE_PATTERN
from ..domain.permission_domain import Permission
from ..services.permissions_service import permissionService


class PermissionCreateRequest(BaseModel):
    code: str = Field(max_length=100, pattern=PERMISSION_CODE_PATTERN)
    description: Optional[str] = None


async def create_permission_handler(body: PermissionCreateRequest):
    try:
        permission = Permission(id=uuid4(), code=body.code, description=body.description)
        created = await permissionService.create(permission)
        return success(201, "Permiso creado correctamente", created.to_dict())

    except UniqueViolationError as err:
        return error(409, "Ya existe un permiso con ese codigo", err)

    except Exception as err:
        return error(500, "Error al crear el permiso", err)
