from .device_get_all_handler import get_all_devices_handler
from .device_get_by_id_handler import get_device_by_id_handler
from .device_update_handler import update_device_handler


class DeviceHandler:
    get_all = staticmethod(get_all_devices_handler)
    get_by_id = staticmethod(get_device_by_id_handler)
    update = staticmethod(update_device_handler)


deviceHandler = DeviceHandler()
