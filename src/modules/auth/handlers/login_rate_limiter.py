import time
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone

from ....core.config.config import config

_attempts: dict[str, deque[float]] = defaultdict(deque)
WINDOW_SECONDS = 60


def allow_login_attempt(ip: str | None) -> bool:
    key = ip or "unknown"
    now = time.monotonic()
    bucket = _attempts[key]
    while bucket and now - bucket[0] > WINDOW_SECONDS:
        bucket.popleft()
    if len(bucket) >= config.login_rate_limit:
        return False
    bucket.append(now)
    if len(_attempts) > 10000:
        for stale in [k for k, v in _attempts.items() if not v or now - v[-1] > WINDOW_SECONDS]:
            _attempts.pop(stale, None)
    return True


_unknown_logins: dict[str, list] = {}
MAX_TRACKED_LOGINS = 10000


def _login_key(login: str) -> str:
    return login.strip().lower()


def _prune_unknown(now: datetime) -> None:
    if len(_unknown_logins) <= MAX_TRACKED_LOGINS:
        return
    for key in [k for k, (_, until, seen) in _unknown_logins.items() if (until is None or until <= now) and now - seen > timedelta(minutes=config.login_lock_minutes)]:
        _unknown_logins.pop(key, None)
    while len(_unknown_logins) > MAX_TRACKED_LOGINS:
        _unknown_logins.pop(next(iter(_unknown_logins)))


def unknown_login_locked_until(login: str) -> datetime | None:
    entry = _unknown_logins.get(_login_key(login))
    if entry is None or entry[1] is None:
        return None
    if entry[1] <= datetime.now(timezone.utc):
        _unknown_logins.pop(_login_key(login), None)
        return None
    return entry[1]


def register_unknown_login_failure(login: str) -> datetime | None:
    now = datetime.now(timezone.utc)
    key = _login_key(login)
    attempts, _, _ = _unknown_logins.get(key, [0, None, now])
    attempts += 1
    locked_until = now + timedelta(minutes=config.login_lock_minutes) if attempts >= config.login_max_attempts else None
    _unknown_logins[key] = [0 if locked_until else attempts, locked_until, now]
    _prune_unknown(now)
    return locked_until
