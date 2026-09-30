from ....core.http.error import error
from ....core.http.list import list_response
from ..services.care_packages_service import carePackageService


async def get_all_care_packages_handler():
    try:
        care_packages = await carePackageService.get_all()
        data = [care_package.to_dict() for care_package in care_packages]
        return list_response(200, "Paquetes de atencion obtenidos correctamente", data, {"count": len(data)})

    except Exception as err:
        return error(500, "Error al obtener los paquetes de atencion", err)
