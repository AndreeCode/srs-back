from .security_alert_detect_repository import (
    find_brute_force_accounts,
    find_brute_force_ips,
    find_many_devices,
    find_shared_devices,
    save_alert,
)
from .security_alert_get_all_repository import get_all_security_alerts
from .security_alert_get_by_id_repository import get_security_alert_by_id
from .security_alert_update_repository import update_security_alert


class SecurityAlertRepository:
    get_all = staticmethod(get_all_security_alerts)
    get_by_id = staticmethod(get_security_alert_by_id)
    update = staticmethod(update_security_alert)
    find_shared_devices = staticmethod(find_shared_devices)
    find_many_devices = staticmethod(find_many_devices)
    save_alert = staticmethod(save_alert)
    find_brute_force_accounts = staticmethod(find_brute_force_accounts)
    find_brute_force_ips = staticmethod(find_brute_force_ips)


securityAlertRepository = SecurityAlertRepository()
