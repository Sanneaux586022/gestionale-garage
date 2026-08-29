from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from config import POSTGRES_CONNECTION


class Base(DeclarativeBase):
    pass


engine = create_engine(POSTGRES_CONNECTION , echo=True)
