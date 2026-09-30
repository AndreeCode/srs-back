from .device_get_all_repository import get_all_devices
from .device_get_by_id_repository import get_device_by_id
from .device_register_repository import register_device
from .device_update_repository import update_device


class DeviceRepository:
    register = staticmethod(register_device)
    get_all = staticmethod(get_all_devices)
    get_by_id = staticmethod(get_device_by_id)
    update = staticmethod(update_device)


deviceRepository = DeviceRepository()
