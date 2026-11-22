from .security_alert_scan_service import scan, scan_auth
from ..repositories.security_alert_repositories import securityAlertRepository


class SecurityAlertService:
    get_all = staticmethod(securityAlertRepository.get_all)
    get_by_id = staticmethod(securityAlertRepository.get_by_id)
    update = staticmethod(securityAlertRepository.update)
    scan = staticmethod(scan)
    scan_auth = staticmethod(scan_auth)


securityAlertService = SecurityAlertService()
