from uuid import UUID

from fastapi import Request

from ....core.http.error import error
from ....core.http.succes import success
from ..domain.portal_errors import PortalAccessError
from ..services.portal_services import portalService


async def portal_overview_handler(request: Request):
    try:
        data = await portalService.overview(UUID(request.state.user["sub"]))
        return success(200, "Portal familiar obtenido correctamente", data)

    except PortalAccessError as err:
        return error(403, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener el portal familiar", err)
