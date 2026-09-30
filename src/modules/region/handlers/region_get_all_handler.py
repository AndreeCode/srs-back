from ....core.http.error import error
from ....core.http.list import list_response
from ..services.regions_service import regionService


async def get_all_regions_handler():
    try:
        regions = await regionService.get_all()
        data = [region.to_dict() for region in regions]
        return list_response(200, "Micro redes obtenidas correctamente", data, {"count": len(data)})

    except Exception as err:
        return error(500, "Error al obtener las micro redes", err)
