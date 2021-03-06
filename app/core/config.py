import secrets
import os
from pydantic import BaseSettings, BaseModel
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Incedo"
    URL: str
    URL_FE: str

    # Database related
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('DATABASE_URL').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///./sql_app.db'

    # Hashing & Security related
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # API's
    MAX_PASS_RESET_ATTEMPTS: int = 5
    PASS_RESET_MINUTES: int = 10

    # Workers
    REMOVE_PASS_RESETS_INTERVAL: int = 60 * 60

    REMOVE_UNVERIFIED_INTERVAL: int = 60 * 60
    MAX_UNVERIFIED_TIME: int = 60 * 60 * 24

    # User related
    AVATAR_PATH: str = 'assets/images/default_avatar.jpg'
    AVATAR_SIZE: int = 256
    MAX_AVATAR_SIZE: int = 2000000       # 2MB

    USERNAME_MIN_LENGTH: int = 3
    USERNAME_MAX_LENGTH: int = 32
    EMAIL_MAX_LENGTH: int = 256
    PASSWORD_MIN_LENGTH: int = 6
    PASSWORD_MAX_LENGTH: int = 256

    class Config:
        env_file = ".env"


class JWTSettings(BaseSettings):
    authjwt_secret_key: str
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = True
    authjwt_access_token_expires: int = 60 * 60
    authjwt_cookie_csrf_protect: bool = True
    authjwt_cookie_domain: str = 'incedo.me'

    class Config:
        env_file = '.env'


class MailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    class Config:
        env_file = ".env"


class FirstAccount(BaseModel):
    username: str = os.environ.get('username')
    email: str = os.environ.get('email')
    password: str = os.environ.get('password')
    password2: str = os.environ.get('password')
    is_admin: bool = True
    is_verified: bool = True


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "main"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "main": {"handlers": ["default"], "level": LOG_LEVEL},
    }


first_account = FirstAccount()
settings = Settings()
mail_settings = MailSettings()
