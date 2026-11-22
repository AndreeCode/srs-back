import hashlib
import hmac
from uuid import UUID

from ....core.config.config import config
from ....core.db.audit_context import valid_ip
from ..domain.guardian_errors import GuardianLinkRateLimitError
from ..repositories.guardian_repositories import guardianRepository

MAX_FAILURES_PER_CHILD = 5
MAX_FAILURES_PER_IP = 10
MAX_FAILURES_PER_ACCOUNT = 5


def identifier_hash(identifier: str) -> str:
    normalized = identifier.strip().upper()
    return hmac.new(config.jwt_secret.encode(), normalized.encode(), hashlib.sha256).hexdigest()


async def ensure_link_allowed(identifier: str, ip: str | None, user_id: UUID | None) -> None:
    failures = await guardianRepository.count_link_failures(identifier_hash(identifier), valid_ip(ip), user_id)

    if (
        failures["identifier"] >= MAX_FAILURES_PER_CHILD
        or failures["ip"] >= MAX_FAILURES_PER_IP
        or failures["account"] >= MAX_FAILURES_PER_ACCOUNT
    ):
        raise GuardianLinkRateLimitError(
            "Demasiados intentos fallidos para vincular a un nino. Intenta mas tarde o acercate a tu establecimiento de salud"
        )


async def record_link_attempt(identifier: str, ip: str | None, user_id: UUID | None, success: bool) -> None:
    await guardianRepository.record_link_attempt(identifier_hash(identifier), valid_ip(ip), user_id, success)
