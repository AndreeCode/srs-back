from ....core.http.error import error
from ....core.http.list import list_response
from ..services.children_service import childService


async def get_all_children_handler():
    try:
        children = await childService.get_all()
        data = [child.to_dict() for child in children]
        return list_response(200, "Ninos obtenidos correctamente", data, {"count": len(data)})

    except Exception as err:
        return error(500, "Error al obtener los ninos", err)
