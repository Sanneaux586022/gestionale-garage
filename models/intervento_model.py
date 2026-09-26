from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Identity, Numeric, text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Intervento(Base):

    __tablename__ = "intervento"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    id_auto: Mapped[int] = mapped_column(ForeignKey("auto.id"), nullable=False)
    id_meccanico: Mapped[int] = mapped_column(
        ForeignKey("meccanico.id"), nullable=False
    )
    id_preventivo: Mapped[int | None] = mapped_column(ForeignKey("preventivo.id"))
    id_fattura: Mapped[int | None] = mapped_column(ForeignKey("fattura.id"))
    stato_intervento: Mapped[str] = mapped_column(nullable=False)
    ore_lavorate: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    tariffa_oraria_applicata: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    data_inizio_intervento: Mapped[date] = mapped_column(server_default=text("CURRENT_DATE"))
    data_fine_intervento: Mapped[date | None] = mapped_column()

    __table_args__ = (
        CheckConstraint(
            "stato_intervento in ('in_corso', 'completato', 'annullato')",
            name="check_stato_intervento",
        ),
    )
