from uuid import UUID

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel

from ....core.http.error import error
from ....core.http.succes import success
from ..domain.user_region_domain import UserRegion
from ..domain.user_region_errors import UserRegionValidationError
from ..services.user_regions_service import userRegionService


class UserRegionCreateRequest(BaseModel):
    user_id: UUID
    region_id: UUID


async def create_user_region_handler(body: UserRegionCreateRequest):
    try:
        user_region = UserRegion(user_id=body.user_id, region_id=body.region_id)
        created = await userRegionService.create(user_region)
        return success(201, "Micro red asignada correctamente", created.to_dict())

    except UserRegionValidationError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return error(409, "El usuario ya tiene asignada esa micro red", err)

    except ForeignKeyViolationError as err:
        if err.constraint_name == "user_region_region_id_fkey":
            return error(400, "El region_id indicado no existe", err)
        return error(400, "El user_id indicado no existe", err)

    except Exception as err:
        return error(500, "Error al asignar la micro red", err)
