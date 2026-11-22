from dotenv import load_dotenv
import logging
import os

load_dotenv()

logger = logging.getLogger(__name__)


class Config:
    dbhost: str = os.getenv("DB_HOST", "localhost")
    dbname: str = os.getenv("DB_NAME", "sicna")
    dbuser: str = os.getenv("DB_USER", "postgres")
    dbpassword: str = os.getenv("DB_PASSWORD", "postgres")

    jwt_secret: str = os.getenv("JWT_SECRET", "dev-secret-change-me")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expire_minutes: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
    cookie_secure: bool = os.getenv("COOKIE_SECURE", "false").lower() == "true"
    trusted_proxies: set[str] = {
        item.strip() for item in os.getenv("TRUSTED_PROXIES", "127.0.0.1,::1").split(",") if item.strip()
    }

    upload_dir: str = os.getenv("UPLOAD_DIR", "uploads")

    mssql_host: str = os.getenv("MSSQL_HOST", "127.0.0.1")
    mssql_port: int = int(os.getenv("MSSQL_PORT", "1433"))
    mssql_db: str = os.getenv("MSSQL_DB", "BDHIS_MINSA")
    mssql_user: str = os.getenv("MSSQL_USER", "")
    mssql_password: str = os.getenv("MSSQL_PASSWORD", "")

    public_registration: bool = os.getenv("PUBLIC_REGISTRATION", "false").lower() == "true"


config = Config()

logger.info(
    "Variables de configuracion obtenidas: dbhost=%s dbname=%s dbuser=%s dbpassword=%s",
    config.dbhost,
    config.dbname,
    config.dbuser,
    config.dbpassword,
)

if config.jwt_secret == "dev-secret-change-me":
    logger.error("JWT_SECRET no esta configurado en el .env, usando un valor inseguro de desarrollo")
