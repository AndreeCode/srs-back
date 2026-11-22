from .auth_login_handler import login_handler
from .auth_logout_handler import logout_handler
from .auth_me_handler import get_me_handler
from .auth_login_handler import mfa_login_handler
from .auth_mfa_handler import (
    mfa_disable_handler,
    mfa_enable_handler,
    mfa_setup_handler,
    mfa_status_handler,
    my_sessions_handler,
    revoke_my_other_sessions_handler,
    revoke_my_session_handler,
)
from .auth_password_handler import change_password_handler
from .auth_register_handler import register_handler


class AuthHandler:
    login = staticmethod(login_handler)
    logout = staticmethod(logout_handler)
    me = staticmethod(get_me_handler)
    register = staticmethod(register_handler)
    change_password = staticmethod(change_password_handler)
    mfa_login = staticmethod(mfa_login_handler)
    mfa_status = staticmethod(mfa_status_handler)
    mfa_setup = staticmethod(mfa_setup_handler)
    mfa_enable = staticmethod(mfa_enable_handler)
    mfa_disable = staticmethod(mfa_disable_handler)
    my_sessions = staticmethod(my_sessions_handler)
    revoke_my_session = staticmethod(revoke_my_session_handler)
    revoke_my_other_sessions = staticmethod(revoke_my_other_sessions_handler)


authHandler = AuthHandler()
