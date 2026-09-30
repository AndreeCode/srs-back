from typing import Optional

from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.region_domain import Region
from ..services.regions_service import regionService


class RegionUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=150)
    health_network: Optional[str] = Field(default=None, min_length=1, max_length=150)
    active: Optional[bool] = None


async def update_region_handler(region_id: str, body: RegionUpdateRequest):
    try:
        region_uuid = parse_uuid(region_id, "region_id")
        current = await regionService.get_by_id(region_uuid)

        if current is None:
            return error(404, "Micro red no encontrada", ValueError(f"region_id={region_id}"))

        region = Region(
            id=current.id,
            name=body.name if body.name is not None else current.name,
            health_network=body.health_network if body.health_network is not None else current.health_network,
            active=body.active if body.active is not None else current.active,
        )

        updated = await regionService.update(region)

        if updated is None:
            return error(404, "Micro red no encontrada", ValueError(f"region_id={region_id}"))

        return success(200, "Micro red actualizada correctamente", updated.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return error(409, "Ya existe una micro red con ese nombre", err)

    except Exception as err:
        return error(500, "Error al actualizar la micro red", err)
