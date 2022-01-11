import secrets
import os
from pydantic import BaseSettings, BaseModel


class Settings(BaseSettings):
    PROJECT_NAME: str = "Incedo"
    URL: str

    # Database related
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///./sql_app.db'

    # Hashing & Security related
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # User related
    AVATAR_PATH: str = 'assets/images/default_avatar.jpg'
    MAX_AVATAR_SIZE: int = 256000       # 256kb
    USERNAME_MIN_LENGTH: int = 3
    USERNAME_MAX_LENGTH: int = 32
    EMAIL_MAX_LENGTH: int = 256
    PASSWORD_MIN_LENGTH: int = 6
    PASSWORD_MAX_LENGTH: int = 256

    class Config:
        env_file = ".env"


class JWTSettings(BaseSettings):
    authjwt_secret_key: str
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}
    # Only allow JWT cookies to be sent over https
    authjwt_cookie_secure: bool = False
    # Enable csrf double submit protection. default is True
    authjwt_cookie_csrf_protect: bool = True
    # Change to 'lax' in production to make your website more secure from CSRF Attacks, default is None
    #authjwt_cookie_samesite: str = 'lax'

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


class DefaultTheme(BaseModel):
    name: str = 'nebula'
    bg: str = '#212135'
    main: str = '#be3c88'
    sub: str = '#19b3b8'
    info: str = '#78c729'
    text: str = '#838686'
    error: str = '#ca4754'


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


settings = Settings()
mail_settings = MailSettings()
default_theme = DefaultTheme()
