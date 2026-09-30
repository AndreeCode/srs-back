from ....core.http.error import error
from ....core.http.list import list_response
from ..services.guardians_service import guardianService


async def get_all_guardians_handler():
    try:
        guardians = await guardianService.get_all()
        data = [guardian.to_dict() for guardian in guardians]
        return list_response(200, "Apoderados obtenidos correctamente", data, {"count": len(data)})

    except Exception as err:
        return error(500, "Error al obtener los apoderados", err)
