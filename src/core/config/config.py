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

    upload_dir: str = os.getenv("UPLOAD_DIR", "uploads")


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
