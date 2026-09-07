from flask import g
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import POSTGRES_CONNECTION


class Base(DeclarativeBase):
    pass


engine = create_engine(POSTGRES_CONNECTION)
SessionFactory = sessionmaker(engine)


def get_db_session():
    if "db_session" not in g:
        g.db_session = SessionFactory()

    return g.db_session


def close_db_session(exception=None):
    db_session = g.pop("db_session", None)
    if db_session is not None:
        db_session.close()


migrate = Migrate()