from logging.config import dictConfig

from app.core import LogConfig
from app.database.initialise import initialise
from app.database.session import SessionLocal


dictConfig(LogConfig().dict())


def init() -> None:
    db = SessionLocal()
    initialise(db)


def main() -> None:
    init()


if __name__ == "__main__":
    main()
