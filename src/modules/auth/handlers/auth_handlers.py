from .auth_login_handler import login_handler
from .auth_logout_handler import logout_handler
from .auth_me_handler import get_me_handler


class AuthHandler:
    login = staticmethod(login_handler)
    logout = staticmethod(logout_handler)
    me = staticmethod(get_me_handler)


authHandler = AuthHandler()
