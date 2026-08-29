from sqlalchemy import Identity
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Cliente(Base):

    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    cognome: Mapped[str] = mapped_column(nullable=False)
    telefono: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str | None] = mapped_column(unique=True)
