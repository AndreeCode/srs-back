import ipaddress

from starlette.requests import Request

from ..config.config import config


def normalize_ip(value: str | None) -> str | None:
    if not value:
        return None
    try:
        ip = ipaddress.ip_address(value.strip())
    except ValueError:
        return None
    mapped = getattr(ip, "ipv4_mapped", None)
    return str(mapped or ip)


def client_ip(request: Request) -> str | None:
    raw = request.client.host if request.client else None
    peer = normalize_ip(raw)
    if peer is not None and peer in config.trusted_proxies:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            candidate = normalize_ip(forwarded.split(",")[-1])
            if candidate is not None:
                return candidate
    return peer or raw
