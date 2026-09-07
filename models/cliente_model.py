from datetime import date

from sqlalchemy import Identity, text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Cliente(Base):

    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    cognome: Mapped[str] = mapped_column(nullable=False)
    telefono: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str | None] = mapped_column(unique=True)
    data_registrazione: Mapped[date] = mapped_column(
        server_default=text("CURRENT_DATE")
    )
