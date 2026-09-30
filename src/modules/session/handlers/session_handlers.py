from .session_get_all_handler import get_all_sessions_handler
from .session_get_by_id_handler import get_session_by_id_handler
from .session_revoke_handler import revoke_session_handler


class SessionHandler:
    get_all = staticmethod(get_all_sessions_handler)
    get_by_id = staticmethod(get_session_by_id_handler)
    revoke = staticmethod(revoke_session_handler)


sessionHandler = SessionHandler()
