from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Identity, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Preventivo(Base):

    __tablename__ = "preventivo"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("cliente.id"), nullable=False)
    id_auto: Mapped[int] = mapped_column(ForeignKey("auto.id"), nullable=False)
    descrizione_lavoro: Mapped[str] = mapped_column(nullable=False)
    importo_stimato: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stato_preventivo: Mapped[str] = mapped_column(nullable=False)
    data_preventivo: Mapped[date] = mapped_column(nullable=False)

    __table_args__ = (
        CheckConstraint(
            "stato_preventivo in ('in_attesa', 'accettato', 'rifiutato')",
            name="check_stato_preventivo",
        ),
    )
