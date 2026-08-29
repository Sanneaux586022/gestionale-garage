from sqlalchemy import Identity
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Auto(Base):

    __tablename__ = "auto"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    targa: Mapped[str] = mapped_column(unique=True, nullable=False)
    modello: Mapped[str] = mapped_column(nullable=False)
    anno: Mapped[int] = mapped_column(nullable=False)
