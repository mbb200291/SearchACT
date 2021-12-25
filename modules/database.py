import pathlib
from os import path

from pydantic import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DBSettings(BaseSettings):
    DEBUG: bool = False
    ECHO: bool = False
    AUTOCOMMIT: bool = False
    AUTOFLUSH: bool = False
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URI: str = "sqlite+pysqlite:///data.db"

    class Config:
        env_file = path.join(pathlib.Path(__file__).parent.parent.resolve(), ".env")
        env_file_encoding = "utf-8"


SETTINGS = DBSettings()
DB_ENGINE = create_engine(
    SETTINGS.SQLALCHEMY_DATABASE_URI,
    echo=SETTINGS.ECHO,
    connect_args={"check_same_thread": False},
)
DB_SESSIONLOCAL = sessionmaker(
    autocommit=SETTINGS.AUTOCOMMIT,
    autoflush=SETTINGS.AUTOFLUSH,
    bind=DB_ENGINE,
)


def get_engine() -> Engine:
    return DB_ENGINE


def get_database_session() -> Session:
    db = DB_SESSIONLOCAL()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print(SETTINGS)
    # db = next(get_database_session())
    # print(db)
    # db = next(get_database_session())
    # print(db)
    # conn = get_database_session()
    # user = User(user_id=1, user_name = "rbuce")
    # conn.add(user)
    # conn.commit()
