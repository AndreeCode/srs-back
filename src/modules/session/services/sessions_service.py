from .session_create_service import create
from .session_get_active_by_token_service import get_active_by_token
from .session_get_all_service import get_all
from .session_get_by_id_service import get_by_id
from .session_revoke_service import revoke, revoke_by_token


class SessionService:
    create = staticmethod(create)
    get_all = staticmethod(get_all)
    get_by_id = staticmethod(get_by_id)
    get_active_by_token = staticmethod(get_active_by_token)
    revoke = staticmethod(revoke)
    revoke_by_token = staticmethod(revoke_by_token)


sessionService = SessionService()
