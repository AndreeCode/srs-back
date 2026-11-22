from .session_create_repository import create_session
from .session_get_active_by_token_repository import get_active_session_by_token
from .session_get_all_repository import get_all_sessions
from .session_get_by_id_repository import get_session_by_id
from .session_revoke_by_token_repository import revoke_session_by_token
from .session_revoke_by_user_repository import revoke_sessions_of_user
from .session_revoke_repository import revoke_session


class SessionRepository:
    create = staticmethod(create_session)
    get_all = staticmethod(get_all_sessions)
    get_by_id = staticmethod(get_session_by_id)
    get_active_by_token = staticmethod(get_active_session_by_token)
    revoke = staticmethod(revoke_session)
    revoke_by_token = staticmethod(revoke_session_by_token)
    revoke_all_of_user = staticmethod(revoke_sessions_of_user)


sessionRepository = SessionRepository()
