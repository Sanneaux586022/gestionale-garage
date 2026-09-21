from datetime import date

from sqlalchemy import Identity, Index, text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Meccanico(Base):

    __tablename__ = "meccanico"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    cognome: Mapped[str] = mapped_column(nullable=False)
    telefono: Mapped[str] = mapped_column(nullable=False)
    specializzazione: Mapped[str | None] = mapped_column()
    data_assunzione: Mapped[date] = mapped_column(
        nullable=False, server_default=text("CURRENT_DATE")
    )
    data_fine_rapporto: Mapped[date | None] = mapped_column()

    __table_args__ = (
        Index(
            "un_solo_telefono_attivo",
            "telefono",
            unique=True,
            postgresql_where=(data_fine_rapporto.is_(None)),
        ),
    )
