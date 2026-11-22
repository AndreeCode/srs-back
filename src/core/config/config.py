from dotenv import load_dotenv
import hashlib
import hmac
import logging
import os

load_dotenv()

logger = logging.getLogger(__name__)


INSECURE_SECRETS = ("dev-secret-change-me", "cambia-esto-por-una-clave-larga")
JWT_ALGORITHMS = ("HS256", "HS384", "HS512")
SSL_MODES = ("disable", "prefer", "require", "verify-ca", "verify-full")
MSSQL_ENCRYPTION_MODES = ("off", "request", "require")
LOCAL_HOSTS = ("127.0.0.1", "localhost", "::1")


def is_local(host: str) -> bool:
    return host in LOCAL_HOSTS or host.startswith("/")


class Config:
    app_env: str = os.getenv("APP_ENV", "development").strip().lower()
    dbhost: str = os.getenv("DB_HOST", "localhost")
    dbname: str = os.getenv("DB_NAME", "sicna")
    dbuser: str = os.getenv("DB_USER", "postgres")
    dbpassword: str = os.getenv("DB_PASSWORD", "")
    db_sslmode: str = os.getenv("DB_SSLMODE", "prefer").strip().lower()

    jwt_secret: str = os.getenv("JWT_SECRET", "")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expire_minutes: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
    audit_chain_key_env: str = os.getenv("AUDIT_CHAIN_KEY", "").strip()
    cookie_secure: bool = (
        os.getenv("COOKIE_SECURE", "false").lower() == "true"
        or os.getenv("APP_ENV", "").strip().lower() == "production"
    )
    trusted_proxies: set[str] = {
        item.strip() for item in os.getenv("TRUSTED_PROXIES", "127.0.0.1,::1").split(",") if item.strip()
    }

    upload_dir: str = os.getenv("UPLOAD_DIR", "uploads")

    mssql_host: str = os.getenv("MSSQL_HOST", "127.0.0.1")
    mssql_port: int = int(os.getenv("MSSQL_PORT", "1433"))
    mssql_db: str = os.getenv("MSSQL_DB", "BDHIS_MINSA")
    mssql_user: str = os.getenv("MSSQL_USER", "")
    mssql_password: str = os.getenv("MSSQL_PASSWORD", "")
    mssql_encryption: str = os.getenv("MSSQL_ENCRYPTION", "require").strip().lower()

    public_registration: bool = os.getenv("PUBLIC_REGISTRATION", "false").lower() == "true"

    login_max_attempts: int = int(os.getenv("LOGIN_MAX_ATTEMPTS", "5"))
    login_lock_minutes: int = int(os.getenv("LOGIN_LOCK_MINUTES", "15"))
    login_rate_limit: int = int(os.getenv("LOGIN_RATE_LIMIT", "10"))

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def audit_chain_key(self) -> str:
        if self.audit_chain_key_env:
            return self.audit_chain_key_env
        return hmac.new(self.jwt_secret.encode(), b"audit-chain-v1", hashlib.sha256).hexdigest()

    def problems(self) -> list[str]:
        found = []
        if self.app_env not in ("development", "production"):
            found.append("APP_ENV debe ser 'development' o 'production'")
        if not self.jwt_secret or self.jwt_secret in INSECURE_SECRETS:
            found.append("JWT_SECRET no esta configurado")
        elif len(self.jwt_secret) < 32:
            found.append("JWT_SECRET debe tener al menos 32 caracteres")
        if not self.dbpassword:
            found.append("DB_PASSWORD no esta configurado")
        if self.jwt_algorithm not in JWT_ALGORITHMS:
            found.append(f"JWT_ALGORITHM debe ser uno de: {', '.join(JWT_ALGORITHMS)}")
        if self.db_sslmode not in SSL_MODES:
            found.append(f"DB_SSLMODE debe ser uno de: {', '.join(SSL_MODES)}")
        elif self.is_production and not is_local(self.dbhost) and self.db_sslmode in ("disable", "prefer"):
            found.append("DB_SSLMODE debe ser require, verify-ca o verify-full si la BD esta en otro servidor")
        if self.mssql_encryption not in MSSQL_ENCRYPTION_MODES:
            found.append(f"MSSQL_ENCRYPTION debe ser uno de: {', '.join(MSSQL_ENCRYPTION_MODES)}")
        elif self.is_production and not is_local(self.mssql_host) and self.mssql_encryption != "require":
            found.append("MSSQL_ENCRYPTION debe ser require si HIS-MINSA esta en otro servidor")
        if self.audit_chain_key_env and len(self.audit_chain_key_env) < 32:
            found.append("AUDIT_CHAIN_KEY debe tener al menos 32 caracteres")
        elif self.is_production and not self.audit_chain_key_env:
            found.append("AUDIT_CHAIN_KEY es obligatorio en produccion (clave del HMAC de la cadena de auditoria)")
        return found

    def ensure_valid(self) -> None:
        found = self.problems()
        if found:
            raise RuntimeError("Configuracion insegura o incompleta en el .env: " + "; ".join(found))


config = Config()

logger.info(
    "Variables de configuracion obtenidas: env=%s dbhost=%s dbname=%s dbuser=%s",
    config.app_env,
    config.dbhost,
    config.dbname,
    config.dbuser,
)
