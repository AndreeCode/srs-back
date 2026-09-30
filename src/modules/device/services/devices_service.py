from .device_get_all_service import get_all
from .device_get_by_id_service import get_by_id
from .device_register_service import register
from .device_update_service import update


class DeviceService:
    register = staticmethod(register)
    get_all = staticmethod(get_all)
    get_by_id = staticmethod(get_by_id)
    update = staticmethod(update)


deviceService = DeviceService()
