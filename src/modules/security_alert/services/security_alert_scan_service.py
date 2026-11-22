from uuid import UUID

from ....core.logger.logger import logger
from ..domain.security_alert_domain import (
    ACCOUNT_DEVICES,
    BRUTE_FORCE_ACCOUNT_FAILURES,
    BRUTE_FORCE_IP_FAILURES,
    BRUTE_FORCE_QUIET_DAYS,
    BRUTE_FORCE_WINDOW_MINUTES,
    QUIET_DAYS,
    SHARED_DEVICE_ACCOUNTS,
    WINDOW_DAYS,
)
from ..repositories.security_alert_repositories import securityAlertRepository


async def scan(device_hash: str | None = None, user_id: UUID | None = None) -> int:
    created = 0

    for found in await securityAlertRepository.find_shared_devices(SHARED_DEVICE_ACCOUNTS, WINDOW_DAYS, device_hash):
        created += await securityAlertRepository.save_alert("shared_device", found, QUIET_DAYS)

    for found in await securityAlertRepository.find_many_devices(ACCOUNT_DEVICES, WINDOW_DAYS, user_id):
        created += await securityAlertRepository.save_alert("many_devices", found, QUIET_DAYS)

    if device_hash is None and user_id is None:
        created += await scan_auth()

    return created


async def scan_auth(user_id: UUID | None = None) -> int:
    created = 0

    try:
        for found in await securityAlertRepository.find_brute_force_accounts(
            BRUTE_FORCE_ACCOUNT_FAILURES, BRUTE_FORCE_WINDOW_MINUTES, user_id
        ):
            if await securityAlertRepository.save_alert("brute_force_account", found, BRUTE_FORCE_QUIET_DAYS):
                created += 1
                logger.error(f"ALERTA DE SEGURIDAD: posible fuerza bruta contra la cuenta {found['detail']['username']}")

        for found in await securityAlertRepository.find_brute_force_ips(BRUTE_FORCE_IP_FAILURES, BRUTE_FORCE_WINDOW_MINUTES):
            if await securityAlertRepository.save_alert("brute_force_ip", found, BRUTE_FORCE_QUIET_DAYS):
                created += 1
                logger.error(f"ALERTA DE SEGURIDAD: {found['detail']['total']} logins fallidos desde la IP {found['subject']}")

    except Exception as err:
        logger.error(f"No se pudo revisar la fuerza bruta: {err}")

    return created
