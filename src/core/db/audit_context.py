from contextvars import ContextVar
from ipaddress import ip_address
from typing import Optional

_audit_context: ContextVar[dict[str, str]] = ContextVar("audit_context", default={})


def valid_ip(value: Optional[str]) -> Optional[str]:
    if not value:
        return None

    try:
        return str(ip_address(value))
    except ValueError:
        return None


def set_audit_context(
    user_id: Optional[str] = None,
    device_id: Optional[str] = None,
    ip: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> None:
    values = {
        "app.user_id": user_id,
        "app.device_id": device_id,
        "app.ip_address": valid_ip(ip),
        "app.user_agent": user_agent,
    }
    current = dict(_audit_context.get())
    current.update({key: value for key, value in values.items() if value})
    _audit_context.set(current)


def get_audit_context() -> dict[str, str]:
    return _audit_context.get()
