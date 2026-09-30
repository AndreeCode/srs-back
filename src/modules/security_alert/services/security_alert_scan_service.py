from uuid import UUID

from ..domain.security_alert_domain import ACCOUNT_DEVICES, QUIET_DAYS, SHARED_DEVICE_ACCOUNTS, WINDOW_DAYS
from ..repositories.security_alert_repositories import securityAlertRepository


async def scan(device_hash: str | None = None, user_id: UUID | None = None) -> int:
    created = 0

    for found in await securityAlertRepository.find_shared_devices(SHARED_DEVICE_ACCOUNTS, WINDOW_DAYS, device_hash):
        created += await securityAlertRepository.save_alert("shared_device", found, QUIET_DAYS)

    for found in await securityAlertRepository.find_many_devices(ACCOUNT_DEVICES, WINDOW_DAYS, user_id):
        created += await securityAlertRepository.save_alert("many_devices", found, QUIET_DAYS)

    return created
