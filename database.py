from flask import g
from flask_migrate import Migrate
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import POSTGRES_CONNECTION

NAMING_CONVENTION = {
    "pk": "%(table_name)s_pkey",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "uq": "%(table_name)s_%(column_0_name)s_key",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


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
