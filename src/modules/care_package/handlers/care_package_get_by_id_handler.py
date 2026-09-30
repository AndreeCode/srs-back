from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.care_packages_service import carePackageService


async def get_care_package_by_id_handler(care_package_id: str):
    try:
        care_package_uuid = parse_uuid(care_package_id, "care_package_id")
        care_package = await carePackageService.get_by_id(care_package_uuid)

        if care_package is None:
            return error(404, "Paquete de atencion no encontrado", ValueError(f"care_package_id={care_package_id}"))

        return success(200, "Paquete de atencion obtenido correctamente", care_package.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener el paquete de atencion", err)
