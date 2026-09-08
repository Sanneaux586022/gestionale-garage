from datetime import date

from sqlalchemy import ForeignKey, Identity, Index, text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class StoricoProprietaAuto(Base):

    __tablename__ = "storico_proprieta_auto"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("cliente.id"), nullable=False)
    id_auto: Mapped[int] = mapped_column(ForeignKey("auto.id"), nullable=False)
    data_inizio: Mapped[date] = mapped_column(
        nullable=False, server_default=text("CURRENT_DATE")
    )
    data_fine: Mapped[date | None] = mapped_column()

    __table_args__ = (
        Index(
            "un_solo_proprietario_attivo",
            "id_auto",
            unique=True,
            postgresql_where=(data_fine.is_(None)),
        ),
    )
