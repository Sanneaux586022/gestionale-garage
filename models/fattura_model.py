from datetime import date

from sqlalchemy import ForeignKey, Identity, text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Fattura(Base):

    __tablename__ = "fattura"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("cliente.id"), nullable=False)
    data_emissione: Mapped[date] = mapped_column(server_default=text("CURRENT_DATE"))
    data_scadenza: Mapped[date] = mapped_column(nullable=False)
    data_pagamento: Mapped[date | None] = mapped_column()
